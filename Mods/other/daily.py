from reply import Reply
from funcs import *



async def majang(reply:Reply, text:str):
    reply.add_group_msg('https://game.maj-soul.com/1/')
    await reply.send()

async def qikongshi(reply:Reply, text:str):
    reply.add_group_msg('到处都是骑空士的陷阱')
    await reply.send()

async def ruling(reply:Reply, text:str):
    reply.add_group_msg('[CQ:image,file=001.jpeg]')
    await reply.send()