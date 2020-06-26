import sys
sys.path.append('./logs')

import time
from datetime import datetime

def filePath(group_id):
    '''根据当前时间和群号返回日志文件所在路径'''
    t = Time(8)
    print(time.strftime("%Y-%m-%d %H:%M:%S",t))

def Time(timeZone:float):
    '''输入UTC时区，返回该时区的时间元组'''
    return time.gmtime(time.time()+3600*timeZone)