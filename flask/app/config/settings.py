class EnvBase:
    DEBUG = False
    TESTING = False

    # 数据库
    SQLALCHEMY_ECHO = True # 显示原始SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Z9mysql9318@35.185.112.117:3307/DnD?charset=utf8mb4'

    # Token
    SECRET_KEY = '123'
    EXPIRES_IN = 3600


class Develope(EnvBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Z9mysql9318@35.185.112.117:3307/DnD?charset=utf8mb4'

class Test(EnvBase):
    pass

class Production(EnvBase):
    pass

settings = {
    "devl":Develope,
    "test":Test,
    "prod":Production
}