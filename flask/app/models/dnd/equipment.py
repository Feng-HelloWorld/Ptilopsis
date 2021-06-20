from app.models.base import Base

from sqlalchemy import Column, Integer, String

class Equipment(Base):
    __tablename__='dnd_equipment'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(2000), nullable=False)
    cardid = Column(Integer)
    battleid = Column(Integer)

    def __init__(self, name, description, cardid, battleid):
        self.name = name
        self.description = description
        self.cardid = cardid
        self.battleid = battleid

    def keys(self):
        return ('id','name','description','cardid','battleid')