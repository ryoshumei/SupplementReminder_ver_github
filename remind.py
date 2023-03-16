from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os
from app import app, db, Database
from datetime import datetime, date,time,timedelta

#need CHANNEL_ACCESS_TOKEN below
line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')

def pushmessage(user_id = str, messages = str):
    
    #remind user
    message_to_send = TextSendMessage(text=messages)
    print(message_to_send)
    line_bot_api.push_message(user_id, messages=message_to_send)

def make_all_db_true():
    reminds = Database.query.all()
    print(reminds)
    for row in reminds:
        row.if_remind = True
        #print('DONE True')
    try:
        db.session.commit()
    except:
        print('There was a issue.') 


if __name__ == "__main__":

    with app.app_context():
        
        DIFF_JST_FROM_UTC = 9
        now = datetime.utcnow() + timedelta(hours=DIFF_JST_FROM_UTC)
        hour_to_compare = int(now.hour)
        
        #test
        #hour_to_compare = 0
        
        if(hour_to_compare == 0):
            make_all_db_true()
            
        now = time(hour_to_compare,0,0,0)
        
        #test with time = 18,10,12
        #now = time(12,0,0,0)
        
        results = db.session.execute(db.select(Database).where(Database.time == now,Database.if_remind == True).order_by(Database.db_id)).scalars()
        #print(results)
        for row in results:
            
            
            user_id_to_send = row.user_id
            message_to_send = "It's time to take " + str(row.supplement_name)
            pushmessage(user_id_to_send, message_to_send)
            
            #print(message_to_send)
            
    

    