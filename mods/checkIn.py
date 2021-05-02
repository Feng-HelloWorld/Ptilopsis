from funcs.miniapp import miniapp as App
from funcs.time import Time
from funcs.msgPack import gMsgP
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Xml

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if text in ["签到","早","早安","早上好"]:
        if text=="签到":
            return __check_in(mp)
        else:
            return __check_in(mp,"早上好，一日之计在于晨")
    else:
        return False

rank = list()

def __check_in(mp:gMsgP, hello='签到成功'):
    t = Time()
    h = int(t.print(flag='[h]'))
    user = mp.sender
    if 4<=h<=9:
        if user.id not in rank:
            timeStr = t.print(flag="[Y]-[M]-[D] [h]:[m]")
            r = len(rank)+1
            rank.append(user.id)
            import random
            appD = [("签到时间",timeStr),("今日顺位",f"{r}位"),("今日运势",random.randint(1,100))]
            appB = []
            app = App(prompt="签到",app_name=hello, title=user.name,app_data=appD, app_button=appB)
            xml = Xml(xml='<?xml version="1.0" encoding="utf-8"?>\n<msg templateID="12345" action="web" brief="庆典筹备" serviceID="1" url="https://ak.hypergryph.com/activity/preparation?source=game"><item layout="2"><picture cover="http://hz.shirolovol.cn:3001/ptilopsis01.jpg"/><title>庆典筹备计划</title><summary>唔，你可能需要这个，大概···</summary></item><source/></msg>', type='Xml')
            msg1 = MessageChain.create([app])
            msg2 = MessageChain.create([xml])
            #msg = MessageChain.join(msg1, msg2)
            return [msg1,msg2]
    else:
        if hello=='签到成功':
            return MessageChain.create([Plain("* 签到仅在4-10点开放")])
        else:
            if 0<h<4:
                return MessageChain.create([Plain("* 离天亮还有一段时间，要再睡一会嘛")])
            elif 9<h<12:
                return MessageChain.create([Plain("* 死后亦自会长眠，生前又何必久睡")])

