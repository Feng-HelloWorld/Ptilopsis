import nonebot
import re
from nonebot.typing import Context_T
import time



bot = nonebot.get_bot()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):
    #消息返回值
    msg={'pub':[],'pri':[]}
    print('START')
    #如果消息为纯文本
    if is_only_text(ctx):
        #消息文本
        txt = ctx.get('raw_message')
        print('raw text: ',txt)
        if txt=='aasdfg123':
            msg['pub'].append('asdf')
            msg['pub'].append('ghjk')
            msg['pri'].append('rfvtgb')
        
        #发送消息
        await send_msg(msg,ctx)
    

async def send_msg(msg:dict, ctx: Context_T):
    """
    发送消息 \n
    msg: 消息列表\n
    ctx: 用于查询群号和用户QQ\n
    Return: 无
    """
    #获取时间戳
    t = time.strftime("%H:%M:%S", time.localtime()) 
    #要发送到群里的列表，每个元素之间增加空格
    if len(msg['pub'])>0:
        reply=""
        for item in msg['pub']:
            reply = reply+item+'\n'
        reply = reply + "GMT-4 " + t
        print('pub: ',reply)
        await bot.send_group_msg(group_id=ctx.get('group_id'),message=reply)
    #要发送给私人的列表，每个元素之间增加空格
    if len(msg['pri'])>0:
        reply=""
        for item in msg['pri']:
            reply = reply+item+'\n'
        reply = reply + "GMT-4 " + t
        print('pri: ',reply)
        await bot.send_private_msg(user_id=ctx.get('sender').get('user_id'),message=reply)

def is_only_text(ctx: Context_T):
    '''
    检查此消息是否只含有文本 \n
    Return: 布尔值
    '''
    msg=ctx.get('message')
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False