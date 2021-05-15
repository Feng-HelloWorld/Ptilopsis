from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500
    msg = 'Error!'
    error_code = 'E00-0000'

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

class UnknownError(APIException):
    msg = "Unknown error!"
    error_code = 'E00-0001'

class AuthError(APIException):
    msg = 'Auth Error'
    error_code = 'E00-0002'

class ParameterException(APIException):
    code = 400
    error_code = 'E00-0003'
    