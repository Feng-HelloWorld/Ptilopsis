from flask import Blueprint
#导入用户表
from app.models.user import User

from app.libs.success import CheckSuccess, SuccessResponse
from app.libs.error import UnknownError

from app.libs.token_auth import auth

api = Blueprint('user',__name__,url_prefix='/api/v1')


@api.route("/test",methods=['GET'])
# @auth.login_required
def test():
    return 'Success'

@api.route('/user/<int:id>',methods=['GET'])
def user(id):
    user  = User.query.get(id)
    if user:
        print("FOUND!!!!!!!!")
    #return f"Looking for user: {id}\n Name: {name}\nPassword Hash: {pwh}"
        return CheckSuccess(user)
    #return user
    #(data=user)
    else:
        print("NOT FOUND!!!!!!!!")
        return UnknownError()