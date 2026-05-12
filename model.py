from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_name = db.Column(db.String(30))
    rub_sum = db.Column(db.Integer)
    pieces_num = db.Column(db.Integer)
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))

class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_name = db.Column(db.String(30))
    total_sum = db.Column(db.Integer)
    goal = db.Column(db.Integer)
    
    
