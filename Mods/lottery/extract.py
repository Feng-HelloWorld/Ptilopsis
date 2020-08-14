from reply import Reply
from funcs import *
from user import *
import json
import random
import re
from event import Event, Level

cfg = dict()

cfgPath = './Mods/lottery/extract.json'
logPath = './Mods/lottery/extract.log'
cfg = loadSettings(cfgPath)



ruling_cd = CD(60,'E4')
ruling_event = Event()
ruling1 = Level([1,2,3,5,6,7,8,9,10,12,13,14,23,24,25,26,27])#Q群截图
#ruling1.setUpItem([23,24,25,26,27])
#ruling1.setUpProbability(7000)
ruling2 = Level([4,15,16,17,18,19,20,21])#桃源文学出版社
ruling3 = Level([11,22])#残魂无语（概率down），泠乙己完整版
ruling3.setUpItem([11])
ruling3.setUpProbability(6000)
ruling_event.addLevel(ruling1,60)
ruling_event.addLevel(ruling2,35)
ruling_event.addLevel(ruling3,5)
async def ruling(reply:Reply, text:str):
    ''''''
    if reply.group_id() in cfg['ruling_on']:
        cd = ruling_cd.check(str(reply.user_id()))
        if cd[0]:
            reply.add_group_msg('[CQ:image,file=001-{}.jpg]'.format( ruling_event.extract() ) )
            await reply.send()
        else:
            Name = reply.user_name()
            ID = reply.user_id()
            left = await get_user(Name,ID,'Coin')
            if left<300:
                reply.add_group_msg('[WARN] 余额不足\n- 600合成玉/次' )
                await reply.send()
            else:
                reply.add_group_msg('[CQ:image,file=001-{}.jpg]'.format( ruling_event.extract() ) )
                await set_user(Name,ID,'Coin',left-300)
                await reply.send()       
    else:
        print('[ERRO] 一键乳泠指令未在此群开启')

async def balance(reply:Reply, text:str):
    ''''''
    Name = reply.user_name()
    ID = reply.user_id()
    Name = await get_user(Name,ID,'Name')
    left = await get_user(Name,ID,'Coin')
    reply.add_group_msg("* {}的钱包里还剩{}合成玉".format(Name, left))
    await reply.send()



async def redeem(reply:Reply, text:str):
    ''''''
    Name = reply.user_name()
    ID = reply.user_id()
    if text[0:2]=='兑换':
        code = text[2:]
    else:
        code = text[8:]

    if reply.group_id() in cfg['redeem_on']:
        
        if not code=='XT68KE3P00':
            reply.add_group_msg('[ERRO] 无效的兑换码[{}]'.format( code ) )
            await reply.send()
        else:
            codes = await get_user(Name, ID, 'Redeem')
            Name = await get_user(Name, ID, 'Name')
            if code not in codes:
                left = await get_user(Name,ID,'Coin')
                await set_user(Name,ID,'Coin',left+6000)
                codes.append(code)
                await set_user(Name,ID,'Redeem',codes)
                reply.add_group_msg('* {}成功领取合成玉*6000'.format( Name ) )
                await reply.send()
            else:
                reply.add_group_msg('[ERRO] 已使用过此兑换码' )
                await reply.send()   
    else:
        print('[ERRO] 兑换指令未在此群开启')
    
async def changeName(reply:Reply, text:str):
    ''''''
    Name = reply.user_name()
    new_name = text[3:]
    ID = reply.user_id()
    left = await get_user(Name,ID,'Coin')
    if left<6000:
        reply.add_group_msg('[WARN] 余额不足, 修改ID需要消耗6000合成玉' )
        await reply.send()
    elif len(new_name)>10:
        reply.add_group_msg('[ERRO] ID长度限制在10个字符以内' )
        await reply.send()
    else:
        await set_user(Name,ID,'Coin',left-6000)
        await set_user(Name,ID,'Name',new_name)
        reply.add_group_msg('* 支付完成:6000合成玉\n- 当前ID已修改为[{}]'.format(new_name) )
        await reply.send()
