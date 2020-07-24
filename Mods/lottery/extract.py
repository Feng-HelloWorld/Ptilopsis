from reply import Reply
from funcs import *
import json
import random
import re
from event import Event, Level

cfg = dict()

cfgPath = './Mods/lottery/extract.json'
logPath = './Mods/lottery/extract.log'
cfg = loadSettings(cfgPath)


ruling_cd = CD(2,'P')
ruling_event = Event()
ruling1 = Level([1,2,3,5,6,7,8,9,10,12,13,14])#Q群截图
ruling2 = Level([4,15,16,17,18,19,20,21])#桃源文学出版社
ruling3 = Level([11])#残魂无语
ruling_event.addLevel(ruling1,60)
ruling_event.addLevel(ruling2,39)
ruling_event.addLevel(ruling3,1)
async def ruling(reply:Reply, text:str):
    ''''''
    if reply.group_id() in cfg['ruling_on']:
        cd = ruling_cd.check(str(reply.user_id()))
        if cd[0]:
            reply.add_group_msg('[CQ:image,file=001-{}.jpg]'.format( ruling_event.extract() ) )
            await reply.send()
        else:
            reply.add_group_msg('[CD] 技能冷却中，剩余{}秒'.format( cd[1] ) )
            await reply.send()   
    else:
        print('[ERRO] 一键乳泠指令未在此群开启')