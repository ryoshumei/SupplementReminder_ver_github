#CAUSION:
#THIS FILE IS ONLY FOR DEBUG TO CHECK THE DATABASE. DO NOT RUN ON A PUBLIC SERVER!
from app import app
from app import app, db, Database
from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy 
import os

with app.app_context():
    
    
    @app.route("/", methods=['POST', 'GET'])
    def test():
    #The codes below is only for test before deploy
        reminds = Database.query.all()
        print(reminds)
        return render_template('index.html',reminds=reminds)
    
    
    if __name__ == "__main__":
        port = int(os.getenv("PORT", 5000))
        
        app.run(host="0.0.0.0", port=port)
