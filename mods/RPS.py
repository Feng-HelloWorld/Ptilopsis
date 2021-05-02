from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At, Quote
from funcs.msgPack import gMsgP
from random import choice, randint
key = ['石头','剪刀','布']
kind = {'石头':'布','剪刀':'石头','布':'剪刀'}


def cmd_group(mp:gMsgP):
    try:
        at = mp.msg.get(At)
        msg = mp.msg.get(Plain)
        print(at,msg)
        if len(msg)==1:
            text = msg[0].text.strip(' ')
            if len(at) == 1 and at[0].target == 1803983079 and text in key:
                return rps(text, mp)
        return False
    except:
        raise
        return False

def cmd_friend():
    pass

def rps(user:str, mp:gMsgP):
    ptilopsis = choice(key)
    if mp.sender.id == 407670050:
        if randint(1,100)>50:
            ptilopsis == kind[user]
    print(ptilopsis)
    message = f"* 结果检定\n- {mp.sender.name}:{user}\n- 咕咕:{ptilopsis}"
    if ptilopsis == user:
        return MessageChain.create([Plain(message+'\n* 唔，好像平局了')])
    elif kind[ptilopsis] == user:
        #用户赢
        return MessageChain.create([Plain(message+'\n* 呜···')])
    else:
        #用户输
        return MessageChain.create([Plain(message+'\n* 呼呼呼～')])        


