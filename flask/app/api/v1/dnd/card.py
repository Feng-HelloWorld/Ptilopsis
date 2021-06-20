from flask import Blueprint, request
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask_cors import CORS

#导入人物卡表
from app.models.dnd.card import Card
from app.libs.success import CheckSuccess, SuccessResponse



from app.libs.dnd.error import DnDCardNotExist, DnDInvalidCardIDorPassword
from app.libs.dnd.success import LoginSuccess

api = Blueprint('card',__name__,url_prefix='/api/v1/dnd/card')
CORS(api,origins='*')

# 查(根据id)
@api.route('/<int:id>',methods=['GET'])
def checkCardByID(id):
    card = Card.query.get(id)
    if card:
        return CheckSuccess(card)
    else:
        return DnDCardNotExist()

# # 查(根据用户)
# @api.route('/byplayer/<int:player>',methods=['GET'])
# def checkCardByPlayer(player):
#     card = Card.query.filter(Card.player==player).all()
#     if card:
#         return CheckSuccess(card)
#     else:
#         return UnknownError()

# # 查(根据名称)
# @api.route('/byname/<str:name>',methods=['GET'])
# def checkCardByName(name):
#     card = Card.query.filter(Card.name==name).all()
#     if card:
#         return CheckSuccess(card)
#     else:
#         return UnknownError()

# # 查(根据用户和战局)
# @api.route('/comprehensive',methods=['GET'])
# def checkEquipmentComprehensive():
#     player = request.json['player']
#     battleid = request.json['battleid']
#     card = Card.query.filter(Card.player==player).filter(Card.battleid==battleid).all()
#     if card:
#         return CheckSuccess(card)
#     else:
#         return UnknownError()

# 增
@api.route('/',methods=['POST'])
def addEquipment():
    name = request.json['name']
    player = request.json['player']
    battleid = request.json['battleid']
    password = request.json['password']
    card = Card(name,player,password,battleid)
    card.create()
    return CheckSuccess(card)

#登录
@api.route('/login',methods=['POST'])
def login():
    cardid = request.json['cardid']
    password = request.json['password']
    card = Card.query.get(cardid)
    if card and card.varifyPW(password):  
        return LoginSuccess(data=TimedJSONWebSignatureSerializer(current_app.config['DND_SECRET_KEY'],expires_in=current_app.config['DND_EXPIRES_IN']).dumps({"cardid":card.id,"name":card.name,"player":card.player,"permission":"full"}).decode('ascii'))
    elif password=='':
        return LoginSuccess(data=TimedJSONWebSignatureSerializer(current_app.config['DND_SECRET_KEY'],expires_in=current_app.config['DND_EXPIRES_IN']).dumps({"cardid":card.id,"name":card.name,"player":card.player,"permission":"read_only"}).decode('ascii'))
    else:
        return DnDInvalidCardIDorPassword()




from app.libs.dnd.token import auth
from flask import current_app, jsonify, g

@api.route('/tokenlogin',methods=['POST'])
@auth.login_required
def tokenlogin():
    return LoginSuccess(data=TimedJSONWebSignatureSerializer(current_app.config['DND_SECRET_KEY'],expires_in=current_app.config['DND_EXPIRES_IN']).dumps({"cardid":g.user.cardid,"name":g.user.name,"player":g.user.player,"permission":"full"}).decode('ascii'))
