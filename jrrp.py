import time
import random

jr=dict()
t=int((int(time.time())-1584129600)/86400)
#read from file
fp=open('./jrrp.txt','r',encoding='utf-8')
for line in fp:
    if line[0:2]=="##":
        t=int(line[2:])
    elif line[0].isdigit():
        temp = line.split(':')
        jr[temp[0]]=int(temp[1])
fp.close

def jrrp(ctx,msg:tuple):
    """
    jrrp指令\n
    ctx\n
    msg\n
    Return: 无
    """
    #获取信息
    QQ=str(ctx['user_id'])
    name=__getName(ctx)
    #重新加载日期，若过期则清空数组，然后直接计算当前用户的新运势
    global t
    new_t = int((int(time.time())-1584129600)/86400)
    if new_t > t:
        jr.clear()
        rp=random.randint(0,100)
        jr[QQ]=rp
        t=new_t
        __write_to_file()
    elif QQ not in jr.keys():
        rp=random.randint(0,100)
        jr[QQ]=rp  
        __write_to_file()
    rp=jr[QQ]        
    msg[0].append("* {}的今日运势指数为【{}】".format(name,rp))
    n=int(rp/5)
    msg[0].append(">"*(n)+"="*(20-n))    
    
def __write_to_file():
    fp=open('./jrrp.txt','w',encoding='utf-8')
    fp.write("##"+str(t)+'\n')
    for key,item in jr.items():
        fp.write("{}:{}\n".format(key,item))
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