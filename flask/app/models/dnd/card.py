from app.models.base import Base

from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

class Card(Base):
    __tablename__='dnd_card'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    player = Column(String(15), nullable=False)
    _password = Column('password',String(100), nullable=False)
    battleid = Column(Integer)

    def __init__(self, name, player, password, battleid=None):
        self.name = name
        self.player = player
        self._password = generate_password_hash(password)
        self.battleid = battleid

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def varifyPW(self, pw):
        return check_password_hash(self._password,pw)

    def keys(self):
        return ('id','name','player','battleid')