'''
包含了Ptilopsis运行所需的一些全局函数
'''
import time
import json

#标准时间存储类
class Time:
    '''读取时间戳或特定格式的字符串，储存为时间戳，默认输出为UTC+8的字符串'''

    __stamp = int()
    
    def __init__(self, Input = 000):
        '''初始化函数，若传入参数为字符串则进行解析，默认为当前时间戳'''
        if Input==000:Input=time.time()
        if type(Input)==float:
            self.__stamp = Input  
        elif type(Input)==str:
            time_zone = float( Input[21:-1] )
            temp = time.strptime(Input[:19],'%Y-%m-%d %H:%M:%S')
            self.__stamp = time.mktime(temp)-3600*time_zone-time.timezone+time.daylight*3600
    
    def __str__(self):
        '''默认输出为形如2000-01-01 01:00:00 [8]的字符串'''
        temp = time.gmtime(self.__stamp+3600*8)
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} [8]".format( temp[0],temp[1],temp[2],temp[3],temp[4],temp[5])

    def __add__(self, num:int):return Time(self.__stamp + num)
    def __sub__(self, value):
        if type(value)==Time:return self.__stamp - value.__stamp
        else:return self.__stamp - value
    def __lt__(self, cmp):return self.__stamp < cmp.__stamp
    def __gt__(self, cmp):return self.__stamp > cmp.__stamp
    def __le__(self, cmp):return self.__stamp <= cmp.__stamp
    def __ge__(self, cmp):return self.__stamp >= cmp.__stamp
    def __eq__(self, cmp):return self.__stamp == cmp.__stamp
    def __ne__(self, cmp):return not self.__stamp == cmp.__stamp

    def print(self, time_zone:float = 8, flag:str = 'default'):
        '''按指定格式输出该时间戳在指定时区下的时间字符串，默认为UTC+8'''
        temp = time.gmtime(self.__stamp+3600*time_zone)
        if flag=='default':
            return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} [{}]".format( temp[0],temp[1],temp[2],temp[3],temp[4],temp[5] , time_zone)
        elif flag=='s':
            return "{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(temp[1],temp[2],temp[3],temp[4],temp[5])

    def isSameDay(self, cmp, refresh:int=0, time_zone:float=8):
        '''根据自定义时间（默认凌晨0点）和时区（默认UTC+8）判断两个时间是否是同一天'''
        t1 = time.gmtime(self.__stamp+3600*(time_zone-refresh))
        t2 = time.gmtime(cmp.__stamp+3600*(time_zone-refresh))
        if (t1[0]==t2[0]) and (t1[1]==t2[1]) and (t1[2]==t2[2]):
            return True
        return False

    def stamp(self):
        '''查看时间戳'''
        return self.__stamp

#自定义日界线时间查询函数
def timeS(time_zone:float = 8, day_switch:int = 4):
    '''输入UTC时区（默认为UTC+8）和每日刷新时间（默认为凌晨0点），返回该时区当前时间下的时间元组'''
    return time.gmtime(time.time()+3600*(time_zone-day_switch))

#标准文件名生成函数
def fileName(key_word:str, day = timeS()):
    '''根据传入的关键字，时区（默认为UTC+8）和每日刷新时间（默认为凌晨0点）生成并返回形如[key] 2000-01-01的文件名'''
    return "[{}] {}".format(key_word, time.strftime("%Y-%m-%d",day) )


class CD:
    '''用于判断指令冷却时间的类'''

    __cd = int()#冷却时间间隔，单位为秒
    __mode = str()#CD模式
    __last_time = dict()#上一次触发指令的时间

    def __init__(self, cd:int=0, mode:str='D'):
        ''''''
        self.__cd = cd
        self.__mode = mode
        if 'D' in mode:
            self.__last_time['Default']=Time('2012-12-12 12:12:12 [8]')        

    def cd(self):
        return self.__cd

    def check(self):
        ''''''
        now = Time()
        if 'D' in self.__mode:
            if now-self.__last_time['Default']>self.__cd:
                self.__last_time['Default']=now
                return (True,'Proved')
            else:
                return (False,str(self.__last_time['Default']+self.__cd))


def loadSettings(file_path:str):
    '''读取返回指定路径下的json数据文件'''
    fp = open(file_path, 'r',encoding="utf-8") 
    cfg = json.load(fp)
    fp.close()
    return cfg

async def saveSettings(file_path:str, cfg:dict):
    '''将内存中的json数据存入指定文件'''
    fp = open(file_path, 'w',encoding="utf-8") 
    json.dump(cfg,fp,indent=4,ensure_ascii=False)
    fp.close()

async def writeLog(file_path:str, record:str):
    '''在指定日志文件中追加记录'''
    fp = open(file_path, 'a', encoding="utf-8")
    fp.write(record+'\n')
    fp.close()