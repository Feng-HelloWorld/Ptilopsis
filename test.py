import sys
sys.path.append('./Mods/pcr')
import asyncio, random
from pic import thankPic
from funcs import *
'''
async def aaa():
    await thankPic("Peach",123456789,5666777)


# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(aaa())
loop.close()'''

cd_a = CD(4,'P')

def a(ID):
    cd = cd_a.check(ID)
    if cd[0]:
        print('Pass!')
    else:
        print('left {} s!'.format(cd[1]))

a('111')#P
time.sleep(2)
a('111')#F
time.sleep(1)
a('222')#P
a('111')#F
time.sleep(2)
a('111')#P
a('222')#F