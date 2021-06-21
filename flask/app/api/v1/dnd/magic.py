from flask import Blueprint, request
from flask_cors import CORS

from app.models.dnd.magic import Magic
from app.libs.dnd.token import auth

from app.libs.success import CheckSuccess, SuccessResponse
from app.libs.error import UnknownError

api = Blueprint('magic',__name__,url_prefix='/api/v1/dnd/magic')
CORS(api,origins='*')

# 查(根据id)
@api.route('/<int:id>',methods=['GET'])
def checkMagicByID(id):
    magic = Magic.query.get(id)
    if magic:
        return CheckSuccess(magic)
    else:
        return UnknownError()

# 查(根据用户)
@api.route('/bycardid/<int:cardid>',methods=['GET'])
def checkMagicByCardid(cardid):
    magic = Magic.query.filter(Magic.cardid==cardid).all()
    if magic:
        return CheckSuccess(magic)
    else:
        return UnknownError()

# 增
@api.route('/',methods=['POST'])
@auth.login_required
def addMagic():
    cnname = request.json['cnname']
    description = request.json['description']
    level = request.json['level']
    cardid = request.json['cardid']
    timecost = request.json['timecost']
    concentrate = request.json['concentrate']
    magic = Magic(cnname,description,level,cardid,timecost,concentrate)
    magic.create()
    return CheckSuccess(magic)

# 删
@api.route('/<int:id>',methods=['DELETE'])
@auth.login_required
def deleteMagic(id):
    magic = Magic.query.get(id)
    if magic:
        magic.delete()
        return CheckSuccess(magic)
    else:
        return UnknownError()

# 改
@api.route('/<int:id>',methods=['PUT'])
@auth.login_required
def fixMagic(id):
    magic = Magic.query.get(id)
    if magic:
        magic.cnname = request.json['cnname']
        magic.description = request.json['description']
        magic.level = request.json['level']
        magic.cardid = request.json['cardid']
        magic.timecost = request.json['timecost']
        magic.concentrate = request.json['concentrate']
        magic.update()
        return CheckSuccess(magic)
    else:
        return UnknownError()