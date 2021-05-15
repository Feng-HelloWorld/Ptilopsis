from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.config.settings import settings
#导入api
from app.api.v1 import user
from app.api.v1 import token
#导入插件
from app.models.base import db

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerException()

class Flask(_Flask):
    json_encoder = JSONEncoder

app = Flask(__name__)

def register_blueprint(app):
    app.register_blueprint(user.api)
    app.register_blueprint(token.api)

def register_plugin(app):
    db.init_app(app)

def creat_app(env='devl'):
    app.config.from_object(settings[env])
    #注册蓝图
    register_blueprint(app)
    #注册插件
    register_plugin(app)
    return app