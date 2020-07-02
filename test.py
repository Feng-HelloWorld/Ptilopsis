import sys
sys.path.append('./Mods/pcr')
import asyncio, random
from pic import thankPic

async def aaa():
    await thankPic("Peach",123456789,5666777)


# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(aaa())
loop.close()