from reply import Reply
from funcs import *
from dice import dice
import json
import random
import re

cfg = dict()

cfgPath = './Mods/coc/roll.json'
logPath = './Mods/coc/roll.log'
cfg = loadSettings(cfgPath)

word_list_1 = ['光明正大','大摇大摆','嚣张至极','信心十足','不慌不忙','镇定自若','一本正经','不置可否','心平气和','张扬跋扈','吊儿郎当','心高气傲','一反常态','装模做样','颤颤巍巍','做贼心虚']

async def rd(reply:Reply, text:str):
    ''''''
    if reply.group_id() in cfg['bot_on']:
        temp = re.match('^\.r(h?)(\d*d\d*[^ ]*)( \S+)?$',text)
        try:
            hide = temp.group(1)
            cmds = '+'+temp.group(2)
            comment = temp.group(3)
            if not comment==None:comment='名为'+comment[1:]+'的'#删掉注释前面的空格并修改格式
            else:comment=''
            cmd_list = re.findall('[\+\-]\d*d?\d*',cmds)#拆分指令串
            result = dice(cmd_list)
            if hide=='h':
                reply.add_group_msg('* {}悄咪咪地扔了一次{}骰子'.format(reply.user_name(), comment))
                reply.add_private_msg('* 悄悄告诉你，投掷{}骰子的结果为[{}]'.format(comment,result))
                await writeLog(logPath, '[rh]{} {}[{}]在群[{}]投掷了一次{}骰子({})，出目[{}]'.format(reply.time().print(),reply.user_name(),reply.user_id(),reply.group_id(),comment,cmds,result))
            else:
                reply.add_group_msg('* {}{}地扔了一次{}骰子\n- {} 出目[{}]'.format(reply.user_name(), random.choice(word_list_1),comment,cmds[1:],result))
                await writeLog(logPath, '[rd]{} {}[{}]在群[{}]投掷了一次{}骰子({})，出目[{}]'.format(reply.time().print(),reply.user_name(),reply.user_id(),reply.group_id(),comment,cmds,result))
            await reply.send()
        except:
            reply.add_group_msg('你说这些谁懂啊？\n[CQ:image,file=exc.jpg]')




async def ra(reply:Reply, text:str):
    ''''''
    if reply.group_id() in cfg['bot_on']:
        pass
    else:
        print('[ERRO] ra指令未在此群开启')

async def rc(reply:Reply, text:str):
    ''''''
    if reply.group_id() in cfg['bot_on']:
        pass
    else:
        print('[ERRO] rc指令未在此群开启')