from reply import Reply
from funcs import *
from random import randint
import time

cfg = dict()

cfgPath = './Mods/other/daily.json'
logPath = './Mods/other/daily.log'
cfg = loadSettings(cfgPath)


async def majang(reply:Reply, text:str):
    reply.add_group_msg('https://game.maj-soul.com/1/')
    await reply.send()

async def qikongshi(reply:Reply, text:str):
    reply.add_group_msg('到处都是骑空士的陷阱')
    await reply.send()

ruling_cd = time.time()-20

async def ruling(reply:Reply, text:str):
    if reply.group_id() in cfg['ruling_on']:
        now = time.time()
        global ruling_cd
        separate = now-ruling_cd
        if separate>15:
            #reply.add_group_msg('[CQ:image,file=001-{}.jpg]'.format( randint(1,8) ) )
            reply.add_group_msg('[ERRO] 功能维护中，预计开放时间:2020.08' )
            await reply.send()
            ruling_cd=now
        else:
            #reply.add_group_msg('[CD] 技能冷却中，剩余{}秒'.format( 15-int(separate) ) )
            reply.add_group_msg('[ERRO] 功能维护中，预计开放时间:2020.08' )
            await reply.send()            