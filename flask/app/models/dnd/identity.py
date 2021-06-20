from app.models.base import Base

from sqlalchemy import Column, Integer, String

class Identity(Base):
    __tablename__='dnd_identity'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(2000), nullable=False)
    cardid = Column(Integer, nullable=False)
    counter = Column(String(500))

    def __init__(self, name, description, cardid, counter):
        self.name = name
        self.description = description
        self.cardid = cardid
        self.counter = counter

    def keys(self):
        return ('id','name','description','cardid','counter')