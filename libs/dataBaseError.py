import re

class DBError(Exception):
    error_code="d1001"
    error_msg="Data Base Error"
    addition_msg=""

    def __init__(self, error_code=None, error_msg=None, addition_msg=None):
        if error_code:self.error_code = error_code
        if error_msg:self.error_msg = error_msg
        if addition_msg:self.addition_msg = addition_msg

    def __str__(self):
        return f"[{self.error_code}] {self.error_msg} {self.addition_msg}"

class ConnectFaild(DBError):
    error_code="d1002"
    error_msg="无法连接至数据库"

class TypeNotSupport(DBError):
    error_code="d1003"
    error_msg="选择的数据类型不受支持"

class OperationalError(DBError):
    def __init__(self, error_msg=None):
        if re.match('duplicate column name: .+',error_msg):
            temp = re.match('duplicate column name: (.+)',error_msg).group(1)
            self.error_code = 'd1004-01'
            self.error_msg = f"重复的列标题：{temp}"
        elif re.match('table [^ ]+ already exists',error_msg):
            temp = re.match('table ([^ ]+) already exists',error_msg).group(1)
            self.error_code = 'd1004-02'
            self.error_msg = f"重复的表标题：{temp}" 
        elif re.match('UNIQUE constraint failed: [^ ]+\.[^ ]+',error_msg):
            temp = re.match('UNIQUE constraint failed: ([^ ]+)\.([^ ]+)',error_msg)
            self.error_code = 'd1004-03'
            self.error_msg = f"表{temp.group(1)}中列{temp.group(2)}的值出现重复"
        else:
            self.error_code = 'd1004-00'
            self.error_msg = error_msg

class ArgsError(DBError):
    error_code="d1005"
    error_msg="传入的参数有误"

class TableNotExist(DBError):
    error_code="d1006"
    error_msg="查询的表单不存在"