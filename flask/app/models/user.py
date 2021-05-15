from app.models.base import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), unique=True, nullable=False)
    _password = Column("password",String(100), nullable=False)

    def __init__(self,name=None, password=None):
        self.name = name
        self._password = generate_password_hash(password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def keys(self):
        return ('id','name')

    def check_password(self, raw):
        return check_password_hash(self._password, raw)