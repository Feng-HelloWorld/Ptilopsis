import json
import time
import pprint

import sys
sys.path.append('./pcr')

from reply import Reply

cfg = dict()

def loadSettings():
    fp = open('./pcr/pcr_team.json', 'r',encoding="utf-8") 
    global cfg
    cfg = json.load(fp)

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
            print("!!!",self.term,self.boss,self.hp_left)
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
            string = "[修正0] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]将第{}周目Boss[{}]剩余血量设置为[{:>9d}]\n".format(log.name, log.id, t[3], t[4], log.time,log.term, log.boss, log.fix)
            fp.write( string )
            print(string)
            self.hp_left = log.fix
        else:
            string = "[{}{}] {:<10s} [{:<12d}] 在{:0>2d}:{:0>2d}[{}]对第{}周目Boss[{}]造成了[{:>9d}]点伤害 剩余血量[{:>9d}]\n".format(log.log_type[0], log.log_type[1], log.name, log.id, t[3], t[4],log.time ,log.term, log.boss, log.damage, log.hp_left)
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
    if reply.group_id() in cfg["on_group"]:
        if damage==0:damage=log_board.hp_left
        if damage>log_board.hp_left and fix==-1:
            reply.add_group_msg("* 伤害值大于boss剩余血量\n- 如果击杀boss，使用“尾刀”指令\n- 如果剩余血量和实际血量不符，联系管理员")
        else: 
            log = Log(reply.user_name(), reply.user_id(), reply.time(), damage, fix)
            if log.log_type[1]==0:
                if reply.user_id() in cfg["admin"]:
                    log_board.add(log)
                    reply.add_group_msg("* {}已将第{}周目Boss{}剩余血量修正为{:,}".format(log.name, log.term, log.boss, log.fix) )
                else:
                    reply.add_group_msg("* ERRO：需要管理员权限")
            else:
                log_board.add(log)
                reply.add_group_msg("* {}的今日第{}刀 {}\n- 对第{}周目Boss{}造成{:,}点伤害，boss剩余血量{:,}".format(log.name, log.log_type[1], log.log_type[0], log.term, log.boss, log.damage, log.hp_left) )
            if log.hp_left==0:reply.add_group_msg("* 当前Boss已被击败，进入下一阶段\n- 第{}周目Boss{} 血量[{:,}]".format(log_board.term, log_board.boss, log_board.hp_left))

def checkStatus(reply:Reply):
    reply.add_group_msg("* 当前第{}周目Boss{} 剩余血量[{:,}]".format(log_board.term, log_board.boss, log_board.hp_left))
    
    