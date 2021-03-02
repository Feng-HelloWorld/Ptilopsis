from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain

class gMsgP:
    '''群组消息包'''
    msg:MessageChain
    sender:Member
    group:Group

    def __init__(self, group, sender, msg):
        self.group = group
        self.sender = sender
        self.msg = msg
    
