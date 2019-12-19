import nonebot
import re
from nonebot.typing import Context_T

bot = nonebot.get_bot()

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):
    
    #如果消息为纯文本
    if is_only_text(ctx):
        msg=ctx.get('raw_message')
        print(msg)



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