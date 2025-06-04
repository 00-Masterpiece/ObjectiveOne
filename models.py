from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    days = db.Column(db.String(50))
    color = db.Column(db.String(20))
    badge_color = db.Column(db.String(20))
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))

class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    date = db.Column(db.String(10))