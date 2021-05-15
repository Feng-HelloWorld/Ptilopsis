import re
from funcs.msgPack import gMsgP
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Xml

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if re.match('^\.select 索拉$',text):
        return MessageChain.create([Xml(xml='<?xml version="1.0" encoding="utf-8"?>\n<msg templateID="12345" action="web" brief="DnD在线人物卡" serviceID="1" url="http://hz.shirolovol.cn:3002/index.html"><item layout="2"><picture cover="http://hz.shirolovol.cn:3001/ptilopsis01.jpg"/><title>Ptilopsis-DnD</title><summary>测试中，未完工</summary></item><source/></msg>', type='Xml')])
    else:
        return False