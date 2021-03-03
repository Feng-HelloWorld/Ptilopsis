import re
from funcs.miniapp import miniapp as App
from funcs.msgPack import gMsgP
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain


def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if re.match('^.help$',text):
        return MessageChain.create([Plain('http://47.98.229.41:3001/')])
    else:
        return False