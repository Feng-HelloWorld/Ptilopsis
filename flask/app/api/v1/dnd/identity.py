from flask import Blueprint, request
from flask_cors import CORS

from app.models.dnd.identity import Identity
from app.libs.dnd.token import auth

from app.libs.success import CheckSuccess, SuccessResponse
from app.libs.error import UnknownError

api = Blueprint('identity',__name__,url_prefix='/api/v1/dnd/identity')
CORS(api,origins='*')

# 查(根据id)
@api.route('/<int:id>',methods=['GET'])
def checkIdentityByID(id):
    identity = Identity.query.get(id)
    if identity:
        return CheckSuccess(identity)
    else:
        return UnknownError()

# 查(根据用户)
@api.route('/bycardid/<int:cardid>',methods=['GET'])
def checkIdentityByCardid(cardid):
    identity = Identity.query.filter(Identity.cardid==cardid).all()
    if identity:
        return CheckSuccess(identity)
    else:
        return UnknownError()

# 增
@api.route('/',methods=['POST'])
@auth.login_required
def addIdentity():
    name = request.json['name']
    description = request.json['description']
    cardid = request.json['cardid']
    counter = request.json['counter']
    identity = Identity(name,description,cardid,counter)
    identity.create()
    return CheckSuccess(identity)

# 删
@api.route('/<int:id>',methods=['DELETE'])
@auth.login_required
def deleteIdentity(id):
    identity = Identity.query.get(id)
    if identity:
        identity.delete()
        return CheckSuccess(identity)
    else:
        return UnknownError()

# 改
@api.route('/<int:id>',methods=['PUT'])
@auth.login_required
def fixIdentity(id):
    identity = Identity.query.get(id)
    if identity:
        identity.name = request.json['name']
        identity.description = request.json['description']
        identity.cardid = request.json['cardid']
        identity.counter = request.json['counter']
        identity.update()
        return CheckSuccess(identity)
    else:
        return UnknownError()