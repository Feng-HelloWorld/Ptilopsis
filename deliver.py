import nonebot
import re
from nonebot.typing import Context_T
import time
from random import choice

import sys
sys.path.append('./coc')
from coc.rd import rd
from jrrp import jrrp, first_jrrp

bot = nonebot.get_bot()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):

    print("\n===NEW MESSAGE INCOME=================")
    time_num = time.mktime( time.gmtime( time.time() ) ) + 3600*8
    time_str = time.strftime( "%b %d %a %H:%M:%S", time.gmtime( time.time()+ 3600*8 ) )
    print( "* TIME(GMT+8) {}   {}".format(time_num, time_str) )
    user_id = ctx.get('sender').get('user_id')
    user_name = __getName(ctx)
    group_id = ctx.get('group_id')
    print("* GROUP [{}]   USER {} [{}]".format(group_id, user_name, user_id))
    text = ctx['raw_message']
    print(text)
    msg = Reply(user_id, user_name, group_id)


    #如果消息为纯文本
    if __text_only(ctx):
        #消息文本
        if text=='wwssaaddabab':
            msg.add_group_msg("输出测试1",596404376)
            msg.add_group_msg("shuchuceshi2\nsss")
            msg.add_private_msg("???")
            msg.add_private_msg("!!!",3426285834)
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

class Reply:

    #Protected var
    _messages_for_group = list()
    _messages_for_private = list()
    _user_id = int()
    _user_name = str()
    _group_id = int()
    _time = float()

    def __init__(self, user_id:int, user_name:str, group_id:int, time:float):
        self._user_id = user_id
        self._user_name = user_name
        self._group_id = group_id
        self._time = time

    def add_group_msg(self, msg:str, id=000):
        if id==000:id=self._group_id
        self._messages_for_group.append( (msg,id) )

    def add_private_msg(self, msg:str, id=000):
        if id==000:id=self._user_id
        self._messages_for_private.append( (msg,id) )

    def user_name(self):
        return self._user_name

    def time(self):
        return self._time

    async def send(self):
        for message in self._messages_for_group:
            msg = message[0]
            id = message[1]
            print("="*15,"\n* REPLY IN GROUP [{}]\n{}".format(id,msg))
            await bot.send_group_msg(group_id=id,message=msg)
        for message in self._messages_for_private:
            msg = message[0]
            id = message[1]
            print("="*15,"\n* REPLY TO [{}]\n{}".format(id,msg))
            await bot.send_private_msg(user_id=id,message=msg)

