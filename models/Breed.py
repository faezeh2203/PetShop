from extensions.extensions import db
from sqlalchemy import Integer, String, Column

class Breed(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    image_url = Column(String(256))