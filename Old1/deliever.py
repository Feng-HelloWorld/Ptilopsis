import nonebot
import re
from nonebot.typing import Context_T

import sys
sys.path.append('./coc')

import coc_main

bot = nonebot.get_bot()

#私聊消息处理
@bot.on_message('private') 
async def handle_private_message(ctx: Context_T):
    print("start","="*30)
    print(ctx)
    print("end","="*30)




#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):
    public_reply=[]
    private_reply=[]
    #如果消息为纯文本
    if is_only_text(ctx):
        raw=ctx.get('raw_message')
        print(raw)
        if raw=='33445566f':
            await bot.send_group_msg(group_id=ctx.get('group_id'),message=coc_main.printCard())
        elif re.match('^\.card$',raw,re.I):
            coc_main.parse(raw,ctx)
            await bot.send_group_msg(group_id=ctx.get('group_id'),message='[CQ:image,file=card_out.jpg]')
        elif re.match('^\.HP[\+\-]\d*',raw,re.I):
            origin, now = coc_main.parse(raw,ctx)
            msg='当前HP: {} -> {}'.format(origin,now)
            await bot.send_group_msg(group_id=ctx.get('group_id'),message=msg)
        elif re.match('^\.SAN[\+\-]\d*',raw,re.I):
            origin, now = coc_main.parse(raw,ctx)
            msg='当前SAN: {} -> {}'.format(origin,now)
            await bot.send_group_msg(group_id=ctx.get('group_id'),message=msg)
        elif re.match('^\.MP[\+\-]\d*',raw,re.I):
            origin, now = coc_main.parse(raw,ctx)
            msg='当前MP: {} -> {}'.format(origin,now)
            await bot.send_group_msg(group_id=ctx.get('group_id'),message=msg)
        elif re.match('^\.rc[\+\-]?\d? .+$',raw,re.I):
            result=coc_main.parse(raw,ctx)
            await bot.send_group_msg(group_id=ctx.get('group_id'),message=result)

def send_msg(pub, pri, ctx):
    """
    发送消息 \n
    pub: 要发送到群里的列表，每个元素之间增加空格\n
    pri: 要发送给私人的列表，每个元素之间增加空格\n
    ctx: 用于查询群号和用户QQ\n
    Return: 无
    """
    if len(pub)>0:
        reply=""
        for item in pub:
            reply = reply+item+'\n'
        await bot.send_group_msg(group_id=ctx.get('group_id'),message=reply)
    if len(pri)>0:
        reply=""
        for item in pri:
            reply = reply+item+'\n'
        #await bot.send_private_msg(group_id=ctx.get('group_id'),message=msg)

def is_only_text(ctx):
    '''
    检查此消息是否只含有文本 \n
    Return: 布尔值
    '''
    msg=ctx.get('message')
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False