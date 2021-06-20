from flask import current_app, jsonify, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as serializer, BadSignature, SignatureExpired
from collections import namedtuple

from app.libs.dnd.error import DnDAuthFailed, DnDPermissionDeny

auth = HTTPTokenAuth()

# 用户信息，命名元组：(类名,　字段名)
UserInfo = namedtuple('UserInfo', ['cardid', 'name','player'])

@auth.verify_token
def verify_token(token):
    # 校验令牌
    s = serializer(current_app.config['DND_SECRET_KEY'],
                   expires_in=current_app.config['DND_EXPIRES_IN'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise DnDAuthFailed(msg='令牌无效或被篡改')
    except SignatureExpired:
        raise DnDAuthFailed(msg='令牌过期')
    if data['permission']=='read_only':
        raise DnDPermissionDeny()

    # 获取令牌中的存储的用户信息，并存储到全局变量 g 中
    cardid = data['cardid']
    name = data['name']
    player = data['player']
    g.user = UserInfo(cardid, name, player)

    # 返回 True 表明令牌校验通过
    return True