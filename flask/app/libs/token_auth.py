from flask import current_app, jsonify
from flask_httpauth import HTTPTokenAuth

from itsdangerous import TimedJSONWebSignatureSerializer as serializer, BadSignature, SignatureExpired

from app.libs.error import AuthError

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    s = serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['EXPIRES_IN'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthError(msg = "Bad Signature")
    except SignatureExpired:
        raise AuthError(msg = "Signature Expired")
    return True