
from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, date,time
from dateutil.parser import parse
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent,
)
import os

app = Flask(__name__)

#database: sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_to_remind.db'
db = SQLAlchemy(app)

class Database(db.Model):
    db_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(200),nullable = False)
    supplement_name = db.Column(db.String(200), nullable = False)
    time = db.Column(db.Time,nullable = False)
    today = db.Column(db.DateTime, default = date.today())
    if_remind = db.Column(db.Boolean, default = True)
    def __repr__(self):
        return '<Database %r>' % self.db_id


#need CHANNEL_ACCESS_TOKEN below
line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
#need CHANNEL_SECRET bleow
handler = WebhookHandler('CHANNEL_SECRET')

user_ids = []
user_ids_waiting_for_name = []
user_ids_waiting_for_time = []
user_to_remind_dic = {}
user_ids_waiting_for_deleteid = []

#@app.route("/", methods=['POST', 'GET'])
#def index():
    #codes below is only for test delete before deploy
    #tasks = Database.query.all()
    #return render_template('index.html',tasks=tasks)

    #return 'ok'
    

    

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#@handler.add()

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text="Plz enter 'add' to add a new reminder\nEnter 'show' to show your reminders\n Enter 'delete' to delete a reminder."))
    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text=event.message.text
    text = text.lower()
    
    if(take_supplement(user_id, event.message.text)):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Good Job! We will not remind you today."))  
    elif(text == 'add'):
        user_ids_waiting_for_name.append(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Plz enter the name you want to add to the reminder"))
    elif(text == 'delete' or user_id in user_ids_waiting_for_deleteid):
        #show all reminder and ask for number to delete
        delete(event)
    elif(text == 'show'):
        show(event)
        
        
        
    elif(user_id in user_ids_waiting_for_name):
        user_ids_waiting_for_time.append(user_id)
        user_to_remind_dic[user_id] = text
        user_ids_waiting_for_name.remove(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Plz enter time 1 ~ 23 integer you want to be remind"))
    elif(user_id in user_ids_waiting_for_time):
        text_return = ''
        if(text.isdigit()):
            time_to_set = int(text)
            if(1 <= time_to_set and 23 >= time_to_set):
                new_reminder = Database(user_id=user_id,supplement_name=user_to_remind_dic[user_id],time=time(time_to_set,0,0,0))
        
                try:
                    db.session.add(new_reminder)
                    db.session.commit()

                except:
                    print('There was an issue adding your reminder')
                print('complete')
                user_ids_waiting_for_time.remove(user_id)
                del user_to_remind_dic[user_id]
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Complete."))
                
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wrong time format, enter 1 ~ 23 integer you want to be reminded"))
            
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="You can enter 'add' to add a new reminder, or 'delete' to delete a reminder." ))
        
def take_supplement(user_id = str, text = str):
    if(text.find(' : ') >= 0):
        take_supplement_strs = text.split(' : ')
        if(is_datetime(take_supplement_strs[1]) == True and is_supplement_added(user_id, take_supplement_strs[0]) == True):
            return True
    
    return False

    
               
def is_supplement_added(user_id = str, name = str):
    
    reminders = Database.query.all()
    value_return = False
    for row in reminders:
        #print(row.supplement_name == name)
        #print(row.user_id == user_id)
        if(row.supplement_name == name and row.user_id == user_id):
            value_return = True
            row.if_remind = False
    
    try:
        db.session.commit()
    except:
        print('There was a issue.')
    return value_return
    
               
     
def is_datetime(string_to_check = str):
    try: 
        parse(string_to_check, fuzzy=False)
        return True
    except:
        return False        
    
def add(new_task = Database):
    try:
        db.session.add(new_task)
        db.session.commit()
        return 'complete'
    except:
        return 'There was an issue adding your task'
    
def delete(event = MessageEvent):
    user_id = event.source.user_id
    text=event.message.text
    text = text.lower()
    if(user_id in user_ids_waiting_for_deleteid):
        if(text.isdigit()):
            id_to_delete = int(text)
            remind_to_delete = Database.query.get(id_to_delete)
            if(remind_to_delete is not None):
                try:
                    db.session.delete(remind_to_delete)
                    db.session.commit()
                    user_ids_waiting_for_deleteid.remove(user_id)
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="The reminder has been deleted."))

                    

                except:
                    print("deleting from database went wrong.") 
            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Wrong number, enter a number you want to delete."))
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wrong number, enter a number you want to delete."))

    elif(text == 'delete'):
        #show all added information 
        
        results = db.session.execute(db.select(Database).where(Database.user_id == user_id).order_by(Database.db_id)).scalars()
        messages = ""
        for row in results:
            
            message = (str(row.db_id) +'  ' + row.supplement_name + '         ' + row.time.strftime("%H:%M:%S") + "\n" )
            messages += message
            #print(row.user_id)
        if(messages == ""):
            messages = 'No reminder exist.'
            
        else:
            messages += 'Plz reply the number you need to delete.'
            user_ids_waiting_for_deleteid.append(user_id)
        
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=messages))
        
        #print(messages)
            
        
        
    
def show(event = MessageEvent):
    user_id = event.source.user_id
    #text=event.message.text
    results = db.session.execute(db.select(Database).where(Database.user_id == user_id).order_by(Database.db_id)).scalars()
    messages = ""
    for row in results:
        #setup message
        message = (str(row.db_id) +'  ' + row.supplement_name + '         ' + row.time.strftime("%H:%M:%S") + "\n" )
        messages += message
        #print(row.user_id)
    if(messages == ""):
        messages = 'No reminder exist.'
        
       
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=messages))


    


if __name__ == "__main__":

    
    port = int(os.getenv("PORT", 4000))
    #app.debug = True
    app.run(host="0.0.0.0", port=port)

    

