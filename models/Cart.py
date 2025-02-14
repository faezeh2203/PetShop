from extensions.extensions import db
from sqlalchemy import Integer, Column, ForeignKey
from datetime import datetime

class Cart(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    breed_id = Column(Integer, ForeignKey('breed.id'))
    quantity = Column(Integer, default=1)