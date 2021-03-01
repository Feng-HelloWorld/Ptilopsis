from nonebot.default_config import *
from datetime import timedelta

#管理员账号
SUPERUSERS = {3426285834,1506101516,1150640066}
#指令起始符
COMMAND_START = {''}
#Debug
DEBUG = False
#参数解析失败默认回复
DEFAULT_VALIDATION_FAILURE_EXPRESSION = '[ERRO] 参数错误'
#会话超时
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=1)

HOST = '0.0.0.0'
PORT = 8080