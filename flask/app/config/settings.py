class EnvBase:
    DEBUG = False
    TESTING = False

    # 数据库
    SQLALCHEMY_ECHO = True # 显示原始SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Z9mysql9318@47.98.229.41:3307/ptilopsis?charset=utf8mb4'

    # DnD-Token
    DND_SECRET_KEY = '2259'
    DND_EXPIRES_IN = 7200


class Develope(EnvBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Z9mysql9318@47.98.229.41:3307/ptilopsis?charset=utf8mb4'

class Test(EnvBase):
    pass

class Production(EnvBase):
    pass

settings = {
    "devl":Develope,
    "test":Test,
    "prod":Production
}