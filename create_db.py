from app import app, db, Database

with app.app_context():
    db.create_all()