from datetime import datetime

from piatrix_app.app import db


class Payment(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    currency = db.Column(db.String(120))
    amount = db.Column(db.INTEGER)
    desc = db.Column(db.String(120))
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, currency, amount, desc):
        self.currency = currency
        self.amount = amount
        self.desc = desc

    def __str__(self):
        return f'{self.id}, {self.currency}, {self.amount}, {self.desc}, {self.created}'
