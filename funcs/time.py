import time

week = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

#标准时间存储类
class Time:
    '''读取时间戳或特定格式的字符串，储存为时间戳，默认输出为UTC+8的字符串'''

    __stamp = int()
    
    def __init__(self, Input = 000):
        '''初始化函数，若传入参数为字符串则进行解析，默认为当前时间戳'''
        if Input==000:Input=time.time()
        if type(Input)==float or type(Input)==int:
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
        '''
        按指定格式输出该时间戳在指定时区下的时间字符串，默认为UTC+8
        flag: [Y]year [M]month [D]day [h]hour [m]minute [s]second [W]week [Z]timezone
        '''
        temp = time.gmtime(self.__stamp+3600*time_zone)
        if flag=='default':
            return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} [{}]".format( temp[0],temp[1],temp[2],temp[3],temp[4],temp[5] , time_zone)
        else:
            if time_zone>0: time_zone = f"+{time_zone}"
            result = flag.replace("[Y]",f"{temp[0]:04d}").replace("[M]",f"{temp[1]:02d}").replace("[D]",f"{temp[2]:02d}").replace("[h]",f"{temp[3]:02d}").replace("[m]",f"{temp[4]:02d}").replace("[s]",f"{temp[5]:02d}").replace("[W]",week[temp[6]]).replace("[Z]",str(time_zone))
            return result

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