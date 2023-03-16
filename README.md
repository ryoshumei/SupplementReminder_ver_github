# SupplementReminder
A SupplementReminder LineBot with Flask,Heroku,Line-sdk

You can 'add', 'check', 'delete' the reminders, add use nfc tagsrecord Record supplement or medication doses.

## Requirement

### line-bot-sdk
To connect with line server.
### Flask, Flask-SQLAlchemy
This project uses Flask to run the app and Flask-SQLAlchemy to creates a sqlite database and manipulates it.
### And for more details, plz check the requirements.txt

### <br>

### You alse need environment below :
### Heroku 
To deploy the app and receive message from line users via webhook.Set your heroku domains + '/callback' to your channel Webhook URL in Line Developers.
For example 
'https://yourherokuappname.herokuapp.com/callback'
### A Line Messaging API Account and a channel
Get you CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET, and replace in app.py and remind.py 

### NFC Tag and iOS automation function
You can setup a automation function with iOS and a NFC tag to tell the line-bot your doses(Refer to the image below).And then the line-bot will stop today's reminder.This automation will be triggered when your iPhone touch the NFC tag.
<br>
Caution: The text you setup to the automation function should be 'SupplementName : CurentDateTime'.There is a ' '(space) between 'SupplementName' and ':', and between ':' and CurentDateTime.
For CurentDateTime you can use the built-in function of iOS.

    ![This is an image](/images_for_readme/nfcsetting.png)

## Run the app
1. Get you CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET from your Line Messaging API Account channel. And replace them in app.py and remind.py.
<br>
2. Run create_db.py to create a blank SQlite database.
<br>
Caution : As Heroku is a ephemeral platform, any change in your SQlite database during runtime will be erased. For public use, you need to switch to  other database such as Heroku Postgres. For personal use, you need to change your SQLite file locally and deploy to Heroku.
<br>
3. Deploy to Your Heroku Project 
<br>
<br>
Caution : check_db.py and relative html,css files are for checking database when testing. Do NOT DEPLOY TO HEROKU AND ANY OTHER PUBLIC SERVER.
<br>
<br>
4. Set your heroku domains + '/callback' to your channel Webhook URL in Line Developers.

5. Add job to Heroku Scheduler. Run remind.py onece every hour at :00

## Features
![This is an image](/images_for_readme/1.png)

### Add a reminder by sending 'Add' (Upper and lower case is fine)
![This is an image](/images_for_readme/2.png)

### Show your reminders by sending 'Show'
![This is an image](/images_for_readme/3.png)

### Delete your reminder by sending 'delete'
![This is an image](/images_for_readme/4.png)

### Remind you ono time
![This is an image](/images_for_readme/5.png)

### Stop today's reminder by touch the setted up NFC tag
![This is an image](/images_for_readme/6.png)



