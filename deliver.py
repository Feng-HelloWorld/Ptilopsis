import nonebot
import re
from nonebot.typing import Context_T
import time
from random import choice
import json

import sys
sys.path.append('./coc')
sys.path.append('./pcr')
from reply import Reply
from pcr_team import loadSettings, addLog, checkStatus
from webGet import bvSearch, biliSearch
from jrrp import jrrp, first_jrrp
from voice import sing, sleep

cfg = dict()

def loadSettings():
    fp = open('./deliver.json', 'r',encoding="utf-8") 
    global cfg
    cfg = json.load(fp)

loadSettings()



bot = nonebot.get_bot()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):

    print("\n===NEW MESSAGE INCOME=================")
    time_num = time.mktime( time.gmtime( time.time() ) ) + 3600*8 #GMT+8
    time_str = time.strftime( "%b %d %a %H:%M:%S", time.gmtime( time.time()+ 3600*8 ) )
    print( "* TIME(GMT+8) {}   {}".format(time_num, time_str) )
    user_id = ctx.get('sender').get('user_id')
    user_name = __getName(ctx)
    group_id = ctx.get('group_id')
    print("* GROUP [{}]   USER {} [{}]".format(group_id, user_name, user_id))
    text = ctx['raw_message']
    print(text)
    msg = Reply(user_id, user_name, group_id, time_num)

    #如果消息为纯文本
    if __text_only(ctx):
        #消息文本
        if text=='wwssaaddabab':
            #msg.add_group_msg("输出测试1",596404376)
            msg.add_group_msg("Test success.",596404376)
            #msg.add_private_msg("???")
            #msg.add_private_msg("!!!",3426285834)
            await msg.send()
        elif re.match("^报刀[0-9]+$",text):
            addLog(msg, int(text[2:]))
            await msg.send()
        elif re.match("^尾刀$",text):
            addLog(msg)
            await msg.send()
        elif re.match("^修正[0-9]+$",text):
            addLog(msg,0,int(text[2:]))
            await msg.send()
        elif re.match("^状态$",text):
            checkStatus(msg)
            await msg.send()
        elif re.match("^\.jrrp$",text,re.I):
            jrrp(msg)
            await msg.send()
        elif re.match("^\.sleep$",text,re.I):
            sleep(msg)
            await msg.send()
        else:
            #混沌语音
            sing(text,msg)
            #检测bv号
            bvSearch(text,msg)
            #每日首次发非指令消息时自动执行jrrp
            if msg.group_id() in cfg["first_jrrp_on"]:
                first_jrrp(msg)
            await msg.send()

    #如果是bilibili小程序分享
    elif(is_bili_share(ctx)):
        name = is_bili_share(ctx)
        biliSearch(name, msg)
        await msg.send()
        

    del msg
    print("===FINISH=============================\n")

def __text_only(ctx:Context_T):
    '''检查此消息是否只含有文本'''
    msg=ctx['message']
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False

def __getName(ctx:Context_T):
    """获取昵称, 没有就返回用户名"""
    nick = ctx['sender']['card']
    name = ctx['sender']['nickname']
    if nick=='': return name
    else: return nick

def is_bili_share(ctx: Context_T):
    """检查此消息是否为哔哩哔哩小程序"""
    try:
        if(ctx['message'][0]["data"]["title"]=="&#91;QQ小程序&#93;哔哩哔哩"):
            msg = ctx['message'][0]["data"]["content"]
            return re.search('desc":"[^}]*"',msg).group()[7:-1]
        else:
            return False
    except:
        return False