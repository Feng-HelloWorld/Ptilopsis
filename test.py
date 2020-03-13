import re
import time

#群消息处理

def handle_group_message(ctx):
    #消息返回值
    msg={'pub':[],'pri':[]}
    print('START')
    #如果消息为纯文本
    if is_only_text(ctx):
        #消息文本
        txt = ctx['raw_message']
        print('raw text: ',txt)
        if txt=='aasdfg123':
            msg['pub'].append('asdf')
            msg['pub'].append('ghjk')
            msg['pri'].append('rfvtgb')
        
        #rd指令
        elif re.match('^\.r\d*d*',txt,re.I):
            print("!!!!!!!!!!!!")








        #发送消息
        test_msg(msg,ctx)
    

def test_msg(msg:dict, ctx):
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
        print("===Public:"+str(ctx['group_id'])+"===")
        print(reply)
        print("#"*20)
    #要发送给私人的列表，每个元素之间增加空格
    if len(msg['pri'])>0:
        reply=""
        for item in msg['pri']:
            reply = reply+item+'\n'
        reply = reply + "GMT-4 " + t
        print("===Private:"+str(ctx['user_id'])+"===")
        print(reply)
        print("#"*20)



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


txt='.r1234d3456'
user=1150640066


ctx={'anonymous': None, 
'font': 7973472, 
'group_id': 596404376, 
'message': [{'type': 'text', 'data': {'text': txt}}], 
'message_id': 877, 
'message_type': 'group', 
'post_type': 'message', 
'raw_message': txt, 
'self_id': 1803983079, 
'sender': {'age': 0, 'area': '', 'card': '', 'level': '冒泡', 'nickname': '萌新', 'role': 'admin', 'sex': 'unknown', 'title': '', 'user_id': user}, 
'sub_type': 'normal', 
'time': 1576539737, 
'user_id': user}

handle_group_message(ctx)