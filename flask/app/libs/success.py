from flask import Response, json

class SuccessResponse(Response):
    code = 200
    msg = "Success Response"
    data = None
    default_mimetype = 'application/json;charset=utf-8'

    def __init__(self, code=None, msg=None, data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        print(self.data)
        result = json.dumps({'code':self.code,'msg':self.msg,'data':self.data})
        Response.__init__(self,result,status=self.code)

class CheckSuccess(SuccessResponse):
    msg = "Check Successfuly"
    def __init__(self,result):
        self.data = {"result":result}
        SuccessResponse.__init__(self)

class CreateSuccess(SuccessResponse):
    msg = 'Here is your token'
    code = 201