from reply import Reply
from funcs import *
import random
import os
import re

'''
cfgPath = './Mods/voice/sound.json'
logPath = './Mods/voice/sound.log'
cfg = loadSettings(cfgPath)
'''
temp = os.listdir('../CQP/data/record/')
sleep_list = list()
for File in temp:
    if re.match('^sleep\-.*\.mp3',File):
        sleep_list.append(File)

async def sleep(reply:Reply, text:str):
    reply.add_group_msg("[CQ:record,file={},magic=false]".format(random.choice(sleep_list)))
    await reply.send()

async def sing(reply:Reply, text:str):
    reply.add_group_msg("[CQ:record,file={}.mp3,magic=false]".format(text[1:]))
    await reply.send()