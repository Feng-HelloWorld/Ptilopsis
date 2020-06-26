from reply import Reply
from funcs import *
import random

cfgPath = './Mods/other/jrrp.json'
logPath = './Mods/other/jrrp.log'
cfg = loadSettings(cfgPath)

async def jrrp(reply:Reply, text:str):
    '''今日运势指令'''
    if reply.group_id() in cfg['bot_on']:
        await dayChange(reply.time())
        if str(reply.user_id()) not in cfg['record'].keys():
            cfg['record'][str(reply.user_id())]=rollJrrp()
            await saveSettings(cfgPath, cfg)
            await writeLog(logPath,"* {}[{}]今日人品值为[{}]".format(reply.user_name(),reply.user_id(),cfg['record'][str(reply.user_id())]))
        rp = cfg['record'][str(reply.user_id())]
        reply.add_group_msg( "* {}今日运势指数为[{}]\n{:=<20s}\n- 结果仅供参考".format(reply.user_name(),rp,'>'*int(rp/5)) )
        await reply.send()
    else:
        print('[ERRO] jrrp指令未在此群开启')

async def dayChange(time_now:Time):
    print(time_now,Time( cfg['today']))
    if not time_now.isSameDay(Time(cfg['today']), refresh=4):
        cfg['today']=time_now.print()
        cfg['record']=dict()
        await saveSettings(cfgPath, cfg)
        await writeLog(logPath,"=={}====================".format(cfg['today']))

def rollJrrp():
    """按照2:6:12:8的比例返回1-20/21-50/51-80/81-100的jrrp"""
    scale = random.randint(1,28)
    if scale<=2:
        final = random.randint(1,20)
    elif scale<=8:
        final = random.randint(21,50)    
    elif scale<=20:
        final = random.randint(51,80)
    else:
        final = random.randint(81,100)
    return final
