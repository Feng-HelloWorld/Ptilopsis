from data.database.Base import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'USER'

    # id，主键、自增
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    # QQ
    qq = Column(String(12),unique=True, nullable=False )
    # 用户名，唯一，非空
    name = Column(String(18), unique=True, nullable=False)
    # 金币
    gender = Column(Integer, nullable=False)
    # 密码
    _password = Column('password', String(100))

    def __init__(self, username=None, password=None, gender=None):
        self.username = username
        self._password = generate_password_hash(password)
        self.gender = gender