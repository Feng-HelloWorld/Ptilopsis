from funcs.dataBase import DataBase
from libs.dataBaseError import *
from libs.battleSkills import *
from funcs.msgPack import gMsgP
from funcs.time import Time
import time
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At


#数据库导入
try:
    db_log = DataBase('./data/battle.db3')
    db_log.creat_table('USER',[('user_id','INT','UNIQUE'),('name','TEXT'),('level','TEXT'),('gold','INT'),('hp','TEXT'),('action','TEXT'),('mp','TEXT'),('skill_point','INT'),('arm','TEXT'),('skill','TEXT'),('buff','TEXT')])
except OperationalError as e:
    print(e)
#用户表单对象
user = db_log['USER'] 

keywords = {}

def cmd_group(mp:gMsgP):
    ats = mp.msg.get(At)
    texts = mp.msg.get(Plain)
    if len(ats)==1 and len(texts)==1:
        at = ats[0].target
        text = texts[0].text
        print(f'aa{text}aa')
        ori = User(mp.sender.id, mp.sender.name)
        tar = User(at, f'{at}')
        if re.search('破颜拳',text):
            return MessageChain.create([Plain(B01(ori, tar))])
        elif re.search('初级治愈术',text):
            return MessageChain.create([Plain(C01(ori, tar))])         
        elif re.search('火球术',text):
            return MessageChain.create([Plain(D01(ori, tar))])
        elif re.search('斯卑修姆光线',text):
            return MessageChain.create([Plain(D02(ori, tar))])
        elif re.match('^[ ]?技能录入:.*', text) and at==1803983079:
            text = text.strip(' ')
            return MessageChain.create([Plain(add(text[5:]))])        
        else:
            for key in keywords.keys():
                # print(f'DIY aa{key}aaaa{text}aa', str(key) in str(text))
                if key in text:
                    print('match!')
                    return MessageChain.create([Plain(diy(ori, tar,keywords[key]))])
            return False

def add(text):
    try:
        temp = text.split('/')
        keywords[temp[0]]=temp[1]
        return '* 录入成功'
    except:
        return '[!] 似乎哪里不对，检查一下格式吧'




class User:
    id:int
    name:str

    def __init__(self,user_id, user_name):
        self.id = user_id
        self.name = user_name
        result = self.check()
        print(result)
        if result==[]:
            user.add([self.id,self.name,'1/0/150',20,'0/100/0','0/10/0','0/10/0',0,'','',''])
        elif not result[0]['name'].isdecimal():
            self.name = result[0]['name']

    def __analysis(self,s:str):
        temp = s.split('/')
        return int(now), int(max), int(time)



    def hp(self, value:int=None):
        '''对hp进行查询或修改，返回修改后的hp'''
        #查询值，并执行随时间恢复函数
        temp = self.check(['hp'])[0]['hp'].split('/')
        hp_now = int(temp[0])
        hp_max = int(temp[1])
        hp_time = int(temp[2])
        time_now = int(Time().stamp())
        speed = 300
        cur = int((time_now-hp_time)/speed)
        print("!!!",hp_now, time_now,cur)
        time_now = hp_time + int(speed*cur)
        hp_now = cur+hp_now
        print("!!!",hp_now,time_now,cur)
        if hp_now>hp_max:hp_now=hp_max
        if value:
            hp_now += value
            if hp_now>hp_max:hp_now=hp_max
        hp_now = int(hp_now)
        print("!!!",hp_now,time_now,cur)
        data = '/'.join([str(int(hp_now)),str(hp_max),str(time_now)])
        self.update('hp',data)
        return hp_now

    def action(self, value:int=None):
        '''对actionp进行查询或修改，返回修改后的action'''
        #查询值，并执行随时间恢复函数
        temp = self.check(['action'])[0]['action'].split('/')
        hp_now = int(temp[0])
        hp_max = int(temp[1])
        hp_time = int(temp[2])
        time_now = int(Time().stamp())
        speed = 3600
        cur = int((time_now-hp_time)/speed)
        time_now = hp_time + int(speed*cur)
        hp_now = cur+hp_now
        if hp_now>hp_max:hp_now=hp_max
        if value:
            hp_now += value
            if hp_now>hp_max:hp_now=hp_max
        hp_now = int(hp_now)
        data = '/'.join([str(int(hp_now)),str(hp_max),str(time_now)])
        self.update('action',data)
        return hp_now

    def check(self,keys:list=['*']):
        '''数据库查询函数'''
        return user.check(requirements=[f"user_id = {self.id}"],keys=list(keys))

    def update(self, key, value):
        return user.update([f"user_id = {self.id}"], key, value)

