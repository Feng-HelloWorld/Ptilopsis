from flask import Blueprint, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as serializer, BadSignature, SignatureExpired

from app.models.user import User
from app.libs.error import AuthError
from app.libs.success import CreateSuccess

from app.validators.form import TokenForm


api = Blueprint('token',__name__,url_prefix='/api/v1')

@api.route('/getToken',methods=['POST'])
def get_tokne():

    #data = request.get_json()
    form = TokenForm().validate()
    #user = User.query.filter_by(name=data['username']).first()
    user = User.query.filter_by(name=form.username.data).first()
    if user is None:
        raise AuthError(msg = 'User not found')
    #if not user.check_password(data['password']):
    if not user.check_password(form.password.data):
        raise AuthError(msg = 'Wrong password')
    s = serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['EXPIRES_IN'])
    token = s.dumps({'id':user.id,'username':user.name})
    return CreateSuccess(data={'token':token.decode('ascii')})