from funcs import *
import json
import random
import re
import sys
import os
from copy import deepcopy

cfg = dict()

cfgPath = './user.json'
userPath = './Users/'
cfg = loadSettings(cfgPath)

################
#用户数据导入
################
users = dict()
sys.path.append('./Users')
file_names = os.listdir('./Users/')
for file_name in file_names:
    temp = loadSettings('./Users/{}'.format(file_name))
    users[str(temp['ID'])]=temp

async def get_user(user_name:str, user_id:int, mod_name:str):
    try:
        if mod_name not in users[str(user_id)].keys():
            temp = deepcopy(users['111'][mod_name])
            print(1,temp)
            await set_user(user_name, user_id, mod_name, temp)
        print(2,users[str(user_id)][mod_name])
        return users[str(user_id)][mod_name]
    except:
        print("[ERRO] Data not found, return init value.")
        await init_user(user_name, user_id)
        return users[str(user_id)][mod_name]



async def set_user(user_name:str, user_id:int, mod_name:str, value):
    try:
        users[str(user_id)][mod_name]=value
        await saveSettings(userPath+"{}.json".format(user_id),users[str(user_id)])
    except:
        print("[ERRO] Save error.")

    
async def init_user(user_name:str,user_id:int):
    temp = deepcopy(users['111'])
    temp['Name']=user_name
    temp['ID']=user_id
    users[str(user_id)]=temp
    await saveSettings(userPath+"{}.json".format(user_id),temp)

async def gift(text:str):
    for id, user in users.items():
        pass