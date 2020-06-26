import json
import time
import copy
import sys
from operator import itemgetter
sys.path.append('./pcr')

from reply import Reply, checkUserInfo
from pcr.pcr_pic import thank

cfg = dict()
data = dict()

def loadSettings():
    fp = open('./pcr/pcr_team.json', 'r',encoding="utf-8") 
    global cfg
    cfg = json.load(fp)
    fp.close()
    fp2 = open('./pcr/pcr_data.json', 'r',encoding="utf-8") 
    global data
    data = json.load(fp2)
    fp2.close()

def saveSettings():
    fp2 = open('./pcr/pcr_data.json', 'w',encoding="utf-8") 
    global data
    json.dump(data,fp2)

loadSettings()

class Log:

    name = str()
    id = int()
    time = int()
    log_type = tuple()
    term = int()
    boss = int()
    damage = int()
    fix = int()
    hp_left = int()

    def __init__(self, name, id, time, damage=0, fix=-1):
        self.name = name
        self.id = id
        self.time = time
        self.term = log_board.term
        self.boss = log_board.boss
        self.damage = damage
        self.fix = fix
        self.hp_left = log_board.hp_left - damage
        start_time = time-(time-cfg["start_time"])%(3600*24)
        end_time = cfg["end_time"]
        user_logs = log_board.getUserLogs(id,start_time,end_time)
        if len(user_logs)>0:
            log = user_logs[-1]
            if log.log_type[0]=="尾刀":
                self.log_type = ("补刀",log.log_type[1])
            elif self.hp_left==0:
                self.log_type = ("尾刀",log.log_type[1]+1)
            else:
                self.log_type = ("整刀",log.log_type[1]+1)
        else:
            if self.hp_left==0:
                self.log_type = ("尾刀",1)
            else:
                self.log_type = ("整刀",1)
        if fix>-1:
            self.log_type = ("修正",0)
        if self.damage==0 and fix==-1:
            self.log_type = ("掉刀",self.log_type[1])

    
    def import_from_str(self,s:str):
        self.name = s[6:16]
        self.id = int(s[18:30].strip())
        self.time = float(s[39:51])
        self.term = int(s[54:55])
        self.boss = int(s[62:63])
        self.log_type = (s[1:3],int(s[3:4]))
        if s[1:3]=="修正":
            self.fix = int(s[72:81].strip())
            self.hp_left = int(s[72:81].strip())
        else:
            self.damage = int(s[68:77].strip())
            self.hp_left = int(s[87:96].strip())
        


    
    def __str__(self):
        t = time.gmtime(self.time-3600*5)
        if self.log_type[1]==0:
            return "[修正0] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]将第{}周目Boss[{}]剩余血量设置为[{:>9d}]\n".format(self.name, self.id, t[3], t[4],self.time, self.term, self.boss, self.fix)
        else:
            return "[{}{}] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]对第{}周目Boss[{}]造成了[{:>9d}]点伤害 剩余血量[{:>9d}]\n".format(self.log_type[0], self.log_type[1], self.name, self.id, t[3], t[4],self.time, self.term, self.boss, self.damage, self.hp_left)


class LogBoard:
    logs = list()
    term = int()
    boss = int()
    hp_left = int()

    def __init__(self):
        self.term = 1
        self.boss = 1
        self.hp_left = 6000000

    def import_logs(self):
        fp = open("./pcr/pcr_team_log.txt","r",encoding="utf-8")
        for line in fp:
            if len(line)>20:
                log = Log("name",123,123,1,0)
                log.import_from_str(line)
                self.logs.append(log)
                print("* 已录入日志：{}".format(log))    
                self.hp_left = log.hp_left
                if self.hp_left==0:self.nextBoss()

    def getUserLogs(self, user_id, start_time=10, end_time=100000000000):
        result = list()
        for log in self.logs:
            if log.time>start_time and log.time<end_time:
                if log.id==user_id and log.log_type[1]>0:
                    result.append(log)    
        return result
    
    def add(self,log:Log):
        self.logs.append(log)
        fp = open("./pcr/pcr_team_log.txt","a",encoding="utf-8")
        t = time.gmtime(log.time-3600*5)
        if log.log_type[1]==0:
            string = "[修正0] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]将第{}周目Boss[{}]剩余血量设置为[{:>9d}]\n".format(log.name[0:10], log.id, t[3], t[4], log.time,log.term, log.boss, log.fix)
            fp.write( string )
            print(string)
            self.hp_left = log.fix
        else:
            string = "[{}{}] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]对第{}周目Boss[{}]造成了[{:>9d}]点伤害 剩余血量[{:>9d}]\n".format(log.log_type[0], log.log_type[1], log.name[0:10], log.id, t[3], t[4],log.time ,log.term, log.boss, log.damage, log.hp_left)
            fp.write( string )
            print(string)
            self.hp_left = log.hp_left
        if self.hp_left==0:self.nextBoss()
        fp.close()

    
    def nextBoss(self):
        self.boss +=1
        if self.boss==6:
            self.term += 1
            self.boss = 1
        self.hp_left = cfg["boss"][self.boss-1]


log_board = LogBoard()
log_board.import_logs()

def addLog(reply:Reply, damage:int=0, fix:int=-1):
    if (reply.group_id() in cfg["on_group"]) and (reply.time() > cfg['end_time']):
        start_time = reply.time()-(reply.time()-cfg["start_time"])%(3600*24)
        if start_time>data['member_refresh_time']:
            data['member']=copy.deepcopy(data['member_init'])
            data['member_refresh_time']=start_time
            print("* 剩余出刀数已更新")
        if damage==-1:damage=log_board.hp_left
        if damage>log_board.hp_left and fix==-1:
            reply.add_group_msg("* 伤害值大于boss剩余血量\n- 如果击杀boss，使用“尾刀”指令\n- 如果剩余血量和实际血量不符，联系管理员")
        elif damage>700000 and fix==-1:
            reply.add_group_msg("* ERRO：数值异常(>700,000)\n- 请检查输入的伤害值是否正确\n- 本记录未存档")
        else: 
            log = Log(reply.user_name(), reply.user_id(), reply.time(), damage, fix)
            if log.log_type[1]==0:
                if reply.user_id() in cfg["admin"]:
                    log_board.add(log)
                    reply.add_group_msg("* {}已将第{}周目Boss{}剩余血量修正为{:,}".format(log.name, log.term, log.boss, log.fix) )
                else:
                    reply.add_group_msg("* ERRO：需要管理员权限")
            elif data["member"][str(log.id)]==0:
                reply.add_group_msg("* ERRO: 今日出刀次数已用完\n- 如有错误请联系管理员")
            else:
                log_board.add(log)
                reply.add_group_msg("* {}的今日第{}刀 {}\n- 对第{}周目Boss{}造成{:,}点伤害，boss剩余血量{:,}".format(log.name, log.log_type[1], log.log_type[0], log.term, log.boss, log.damage, log.hp_left) )
                userDataRecord(log)
                if data["member"][str(log.id)]==0:
                    end_time = cfg["end_time"]
                    logs = log_board.getUserLogs(log.id, start_time, end_time)
                    sum = 0
                    for log in logs:
                        sum += log.damage
                    name = log.name
                    if len(name)>10:name=name[0:9]+"..."
                    thank(name, log.id, sum) 
                    reply.add_group_msg('[CQ:image,file=thank_out.jpg]')
            if (log.hp_left==0 and log.fix==-1) or (log.fix==0):
                reply.add_group_msg("* 当前Boss已被击败，进入下一阶段\n- 第{}周目Boss{} 血量[{:,}]".format(log_board.term, log_board.boss, log_board.hp_left))
                if len(data['subscribe'][log_board.boss-1])>0:
                    string = "* [预约通知]"
                    for people in data['subscribe'][log_board.boss-1]:
                        string += ' [CQ:at,qq={}] '.format(people)
                    data['subscribe'][log_board.boss-1].clear()
                    saveSettings()
                    reply.add_group_msg(string)

def userDataRecord(log:Log):
    if log.log_type[0]=="整刀" or log.log_type[0]=="补刀" or log.log_type[0]=="掉刀":
        data["member"][str(log.id)]-=1
        saveSettings()
        print("* 已修改用户[{}]的剩余次数为[{}]".format(log.name, data["member"][str(log.id)]))

def checkStatus(reply:Reply):
    reply.add_group_msg("* 当前第{}周目Boss{} 剩余血量[{:,}]".format(log_board.term, log_board.boss, log_board.hp_left))

def takeFirst(elem):
    return elem[0]
def takeSecond(elem):return elem[1]


async def memberSum(reply:Reply):
    if reply.user_id() in cfg["admin"]:
        temp = dict()
        result = list()
        for id in cfg['user_list']:
            temp[str(id)] = 0
        for log in log_board.logs:
            if log.log_type[0]=="整刀" or log.log_type[0]=="补刀" or log.log_type[0]=="掉刀":
                temp[str(log.id)] += 1
        for key, value in temp.items():
            t = (key,value)
            result.append(t)
        result.sort(key=takeFirst,reverse=False)
        result.sort(key=takeSecond,reverse=True)
        string = "* 本次会战总计出刀数据统计:"
        for t in result:
            user_info = await checkUserInfo(459888770, t[0])
            name = user_info["card"] 
            if name=='':name = user_info["nickname"]
            string += "\n- {}合计出刀[{}]次".format(name,t[1])
        reply.add_group_msg(string)

    
async def checkAttendence(reply:Reply,start_time=10, end_time=100000000000):
    start_time = reply.time()-(reply.time()-cfg["start_time"])%(3600*24)
    end_time = cfg["end_time"]
    result = "* 今日未出刀列表:"
    for item in cfg["user_list"]:
        left = data["member"][str(item)]
        if left >0:
            print("[{}]未出完刀".format(item))
            user_info = await checkUserInfo(459888770, item)
            name = user_info["card"]
            if name=='':name = user_info["nickname"]
            result+="\n- {} 缺[{}]刀".format(name,left)   
    reply.add_group_msg(result) 

def makeSubscribe(reply:Reply, boss:int):
    if reply.user_id() not in data['subscribe'][boss]:data['subscribe'][boss].append(reply.user_id())
    saveSettings()
    reply.add_group_msg("* [{}]已预约Boss[{}]，将在下次轮替到此Boss时收到通知".format(reply.user_name(), boss+1))