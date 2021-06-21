from app.models.base import Base

from sqlalchemy import Column, Integer, String

class Magic(Base):
    __tablename__='dnd_magic'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    cnname = Column(String(50), nullable=False)
    description = Column(String(2000), nullable=False)
    level = Column(Integer, nullable=False)
    cardid = Column(Integer, nullable=False)
    timecost = Column(String(20), nullable=False)
    concentrate = Column(Integer, nullable=False)

    def __init__(self, cnname, description, level, cardid, timecost, concentrate):
        self.cnname = cnname
        self.description = description
        self.level = level
        self.cardid = cardid
        self.timecost = timecost
        self.concentrate = concentrate

    def keys(self):
        return ('id','cnname','description','level','cardid','timecost','concentrate')