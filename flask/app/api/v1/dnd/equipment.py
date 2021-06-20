from flask import Blueprint, request
from flask_cors import CORS
#导入装备表
from app.models.dnd.equipment import Equipment
from app.libs.success import CheckSuccess, SuccessResponse
from app.libs.error import UnknownError

from app.libs.dnd.token import auth

api = Blueprint('equipment',__name__,url_prefix='/api/v1/dnd/equipment')
CORS(api,origins='*')


# 查(根据id)
@api.route('/<int:id>',methods=['GET'])
def checkEquipmentByID(id):
    equipment = Equipment.query.get(id)
    if equipment:
        return CheckSuccess(equipment)
    else:
        return UnknownError()

# 查(根据用户)
@api.route('/bycardid/<int:cardid>',methods=['GET'])
def checkEquipmentByCardid(cardid):
    equipment = Equipment.query.filter(Equipment.cardid==cardid).all()
    if equipment:
        return CheckSuccess(equipment)
    else:
        return UnknownError()

# 查(根据战局)
@api.route('/bybattleid/<int:battleid>',methods=['GET'])
def checkEquipmentByBattleid(battleid):
    equipment = Equipment.query.filter(Equipment.battleid==battleid).all()
    if equipment:
        return CheckSuccess(equipment)
    else:
        return UnknownError()

# 查(根据用户和战局)
@api.route('/comprehensive',methods=['GET'])
def checkEquipmentComprehensive():
    cardid = request.json['cardid']
    battleid = request.json['battleid']
    equipment = Equipment.query.filter(Equipment.cardid==cardid).filter(Equipment.battleid==battleid).all()
    if equipment:
        return CheckSuccess(equipment)
    else:
        return UnknownError()

# 增
@api.route('/',methods=['POST'])
@auth.login_required
def addEquipment():
    name = request.json['name']
    description = request.json['description']
    cardid = request.json['cardid']
    battleid = request.json['battleid']
    equipment = Equipment(name,description,cardid,battleid)
    equipment.create()
    return CheckSuccess(equipment)

# 删
@api.route('/<int:id>',methods=['DELETE'])
@auth.login_required
def deleteEquipment(id):
    equipment = Equipment.query.get(id)
    if equipment:
        equipment.delete()
        return CheckSuccess(equipment)
    else:
        return UnknownError()

# 改
@api.route('/<int:id>',methods=['PUT'])
@auth.login_required
def fixEquipment(id):
    equipment = Equipment.query.get(id)
    if equipment:
        equipment.name = request.json['name']
        equipment.description = request.json['description']
        equipment.cardid = request.json['cardid']
        equipment.battleid = request.json['battleid']
        equipment.update()
        return CheckSuccess(equipment)
    else:
        return UnknownError()

