from app import db
from datetime import datetime

class Record(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return f'<Record {self.name} - {self.date}>'