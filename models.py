from app import db
from datetime import datetime


class Task(db.Model):

    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created

    def __repr__(self):
        return '<Task %r>' % self.id