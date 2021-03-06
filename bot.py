import asyncio
import sys, os, time, regex, importlib
from funcs.msgPack import gMsgP
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, App
from graia.application.friend import Friend
from graia.application.group import Group, Member


################
#模块导入代码
################
sys.path.append('./mods')
dirList = os.listdir('./mods/')
group_cmds = dict()
friend_cmds = dict()
for name in dirList:
    if '.py' in name:
        name = name[:-3]
        print('==Import mod: {:=<34s}'.format(name))
        mod = importlib.import_module(name)
        try:
            group_cmds.update({name:mod.cmd_group})
            print('* Group:', mod.cmd_group)
        except:
            print('- No Group Method')
        try:
            friend_cmds.update({name:mod.cmd_friend})
            print('* Friend:', mod.cmd_friend)
        except:
            print('- No Friend Method')
print('='*48)
################

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        # host="http://172.17.0.1:8080", # 填入 httpapi 服务运行的地址
        host="http://47.98.229.41:8080", # 填入 httpapi 服务运行的地址
        authKey="Ptilopsis", # 填入 authKey
        account=1803983079, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver("FriendMessage")
async def friend_message_handler(message: MessageChain,app: GraiaMiraiApplication, friend: Friend):
    pass
    #await app.sendFriendMessage(friend,msg)

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    print(message)
    print(message.asDisplay())
    for func in group_cmds.values():
        msg = func(gMsgP(group, member, message))
        if msg:
            await app.sendGroupMessage(group,msg)
            break


app.launch_blocking()