import re
from funcs.msgPack import gMsgP
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Xml

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if re.match('^.help$',text):
        return MessageChain.create([Xml(xml='<?xml version="1.0" encoding="utf-8"?>\n<msg templateID="12345" action="web" brief="帮助文档" serviceID="1" url="http://hz.shirolovol.cn:3001/index.html"><item layout="2"><picture cover="http://hz.shirolovol.cn:3001/ptilopsis01.jpg"/><title>Ptilopsis帮助文档</title><summary>最，最后允许你看一次帮助文档哦...一定要记好啦！</summary></item><source/></msg>', type='Xml')])
    else:
        return False