import re

import time
import sys
sys.path.append('./coc')
from coc.rd import rd
from jrrp import jrrp, first_jrrp, rollJrrp

#群消息处理

def handle_group_message(ctx):
    #消息返回值
    pub=[]
    pri=[]
    msg=(pub,pri)
    print('START')
    #如果消息为纯文本
    if is_only_text(ctx):
        #消息文本
        txt = ctx['raw_message']
        print('raw text: ',txt)
        if txt=='wwssaaddabab':
            msg[0].append('输出测试')
            msg[0].append('copyright@2020 Ptilposis')
            msg[1].append('输出测试')
        
        #rd指令
        elif re.match('^\.r\d*d\d*.*$',txt,re.I):
            rd(txt,ctx,msg)
        elif txt==".jrrp":
            jrrp(ctx,msg)

        #发送消息
        test_msg(msg,ctx)
    
def test_msg(msg:tuple, ctx):
    """
    发送消息 \n
    msg: 消息列表\n
    ctx: 用于查询群号和用户QQ\n
    Return: 无
    """
    #要发送到群里的列表，每个元素之间增加空格
    if len(msg[0])>0:
        reply=connect(msg[0])
        print("===Public:"+str(ctx['group_id'])+"===")
        print(reply)
        print("#"*20)
    #要发送给私人的列表，每个元素之间增加空格
    if len(msg[1])>0:
        reply=connect(msg[1])
        print("===Private:"+str(ctx['user_id'])+"===")
        print(reply)
        print("#"*20)

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

def is_only_text(ctx):
    '''
    检查此消息是否只含有文本 \n
    Return: 布尔值
    '''
    msg=ctx['message']
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False


txt='.jrrp'
user=1150640067


ctx={'anonymous': None, 
'font': 7973472, 
'group_id': 596404376, 
'message': [{'type': 'text', 'data': {'text': txt}}], 
'message_id': 877, 
'message_type': 'group', 
'post_type': 'message', 
'raw_message': txt, 
'self_id': 1803983079, 
'sender': {'age': 0, 'area': '', 'card': 'Miko', 'level': '冒泡', 'nickname': '萌新', 'role': 'admin', 'sex': 'unknown', 'title': '', 'user_id': user}, 
'sub_type': 'normal', 
'time': 1576539737, 
'user_id': user}

handle_group_message(ctx)

sum1 = 0
for i in range(20):
    #print(i,"-------",rollJrrp())
    sum1 += rollJrrp()
print(sum1/20)
print(time.time())