from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500
    msg = 'DnD Api Error!'
    error_code = 'E01-0000'

    def __init__(self, code=None, msg=None, error_code=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        super(APIException, self).__init__(msg,None)

    def get_body(self, environ=None):
        body = dict(msg=self.msg,error_code=self.error_code,request=request.method + " " + request.path)
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json; charset=utf-8")]
    

class DnDCardNotExist(APIException):
    code = 404
    msg = '找不到此id对应的人物卡数据'
    error_code = 'E01-0001'

class DnDInvalidCardIDorPassword(APIException):
    code = 400
    msg = 'ID或密码错误'
    error_code = 'E01-0002'

class DnDAuthFailed(APIException):
    code = 403
    msg = '令牌无效或已过期'
    error_code = 'E01-0003'

class DnDPermissionDeny(APIException):
    code = 403
    msg = '此令牌为只读权限'
    error_code = 'E01-0004'