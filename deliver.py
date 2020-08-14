import nonebot
import re
from nonebot.typing import Context_T
from random import choice, randint
import json
import asyncio
import sys
import os
import importlib
from reply import Reply

cfg = dict()

def loadSettings():
    fp = open('./deliver.json', 'r',encoding="utf-8") 
    global cfg
    cfg = json.load(fp)

def saveSettings():
    fp = open('./deliver.json', 'w',encoding="utf-8") 
    global cfg
    cfg = json.dump(fp,indent=4,ensure_ascii=True)

loadSettings()

################
#模块导入代码
################
sys.path.append('./Mods')
dirList = os.listdir('./Mods/')
cmds = dict()
for name in dirList:
    if '.' not in name:
        print('==Import mod: {:=<10s}========'.format(name))
        sys.path.append('./Mods/'+name)
        mod = importlib.import_module(name+'.Cmd-'+name)
        for regex, func in mod.cmdList.items():
            print('* Success:',regex,func)
        cmds.update(mod.cmdList)
        print('='*32)
################

bot = nonebot.get_bot()

#消息处理
@bot.on_message('private') 
async def handle_group_message(ctx:Context_T):
    text = ctx['raw_message']
    sender = ctx.get('sender').get('user_id')
    print(text, sender)
    if sender in [3426285834,1051835124]:
        print(text, sender)
        if re.match('^\.unban[0-9]+$', text):
            group = text[6:]
            print(group)
            await bot.set_group_ban(group_id=group,user_id=sender,duration=0)

reply_dict = dict()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx:Context_T):
    
    group_id = ctx.get('group_id')
    if group_id in cfg['bot_on']:
        text = ctx['raw_message']
        global cmds
        for key, func in cmds.items():
            if re.match(key, text):
                reply = Reply(ctx.get('sender').get('user_id'), __getName(ctx), group_id)
                await func(reply, text)

def __text_only(ctx):
    '''检查此消息是否只含有文本'''
    msg=ctx['message']
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False

def __getName(ctx):
    """获取昵称, 没有就返回用户名"""
    nick = ctx['sender']['card']
    name = ctx['sender']['nickname']
    if nick=='': return name
    else: return nick

