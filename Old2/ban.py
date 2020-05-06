import re
from nonebot.typing import Context_T



ban_list=list()

#read from file
fp=open('./ban_list.txt','r',encoding='utf-8')
for line in fp:
    ban_list.append(re.search("[0-9]+",line)[0])
fp.close

def __write_to_file():
    fp=open('./ban_list.txt','w',encoding='utf-8')
    for item in ban_list:
        fp.write("{}\n".format(item))
    fp.close

def __getName(ctx):
    """
    获取用户名 \n
    ctx \n
    Return: 若用户有马甲就返回马甲，没有就返回昵称 (str)
    """
    nick = ctx['sender']['card']
    name = ctx['sender']['nickname']
    if nick=='': return name
    else: return nick


def ban(ctx, cmd, msg):
    QQ = re.search("[0-9]+",cmd)[0]
    print("Ban QQ:",QQ)
    if QQ!="407670050":
        msg[0].append("* 权限不足")
    elif QQ in ban_list:
        msg[0].append("* [{}]已在黑名单中".format(QQ))
    else:
        ban_list.append(QQ)
        __write_to_file()
        msg[0].append("* [{}]已现已加入黑名单豪华套餐".format(QQ))

def is_ban(ctx, msg):
    QQ = str(ctx['user_id'])
    print("Check Ban:",QQ)
    print("Ban list:",ban_list)
    if QQ in ban_list:
        msg[0].append("* [{}]已被禁用此功能".format(__getName(ctx)))
        return False
    else:
        return True