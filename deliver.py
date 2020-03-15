import nonebot
import re
from nonebot.typing import Context_T
import sys
sys.path.append('./coc')
from coc.rd import rd
from jrrp import jrrp, first_jrrp


bot = nonebot.get_bot()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):
    #消息返回值
    pub=[]
    pri=[]
    msg=(pub,pri)
    #如果消息为纯文本
    if is_only_text(ctx):
        #消息文本
        txt = ctx['raw_message']



        if txt=='wwssaaddabab':
            msg[0].append('输出测试')
            msg[0].append('copyright@2020 Ptilposis')
            msg[1].append('输出测试')
        #rd指令
        elif re.match('^\.r\d*d\d*.*$',txt,re.I):
            rd(txt,ctx,msg)
        #jrrp指令
        elif txt==".jrrp":
            jrrp(ctx,msg)
        else:
            #每日首次发非指令消息时自动执行jrrp
            first_jrrp(ctx,msg)

        #发送消息
        await send_msg(msg,ctx)

async def send_msg(msg:tuple, ctx: Context_T):
    """
    发送消息 \n
    msg: 消息列表\n
    ctx: 用于查询群号和用户QQ\n
    Return: 无
    """
    #要发送到群里的列表，每个元素之间增加空格
    if len(msg[0])>0:
        reply=connect(msg[0])
        await bot.send_group_msg(group_id=ctx.get('group_id'),message=reply)
    #要发送给私人的列表，每个元素之间增加空格
    if len(msg[1])>0:
        reply=connect(msg[1])
        await bot.send_private_msg(user_id=ctx.get('sender').get('user_id'),message=reply)

def connect(l:list):
    """
    把一个list拼接成一个带换行的string
    """
    result=str()
    for i in range(len(l)):
        result+=l[i]
        if i<len(l)-1:
            result+="\n"
    return result

def is_only_text(ctx: Context_T):
    '''
    检查此消息是否只含有文本 \n
    Return: 布尔值
    '''
    msg=ctx['message']
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False