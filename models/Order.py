from extensions.extensions import db
from sqlalchemy import Integer, Column, ForeignKey, DateTime
from datetime import datetime

class Order(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    breed_id = Column(Integer, ForeignKey('breed.id'))
    quantity = Column(Integer)
    order_date = Column(DateTime, default=datetime.utcnow)