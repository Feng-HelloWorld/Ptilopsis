import time
import random
from reply import Reply

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


def rollJrrp():
    """
    按照4:6:9:7的比例返回1-20/21-50/51-80/81-100的jrrp
    """
    scale = random.randint(1,28)
    if scale<=4:
        final = random.randint(1,20)
    elif scale<=12:
        final = random.randint(21,50)    
    elif scale<=21:
        final = random.randint(51,80)
    else:
        final = random.randint(81,100)
    return final



def jrrp(msg:Reply):
    """jrrp指令"""
    #获取信息
    QQ=str(msg.user_id())
    name=msg.user_name()
    #重新加载日期，若过期则清空数组，然后直接计算当前用户的新运势
    global t
    new_t = int((int(time.time())-1584129600)/86400)
    if new_t > t:
        jr.clear()
        rp=rollJrrp()
        jr[QQ]=rp
        t=new_t
        __write_to_file()
    elif QQ not in jr.keys():
        rp=rollJrrp()
        jr[QQ]=rp  
        __write_to_file()
    rp=jr[QQ]        
    if rp>9:
        n=int(rp/5)   
        result = "* {}的今日运势指数为【{}】\n".format(name,rp) + ">"*(n)+"="*(20-n) + "\n- 结果仅供参考"
        msg.add_group_msg(result)
    else:
        result = "* {}的今日运势...emmm...\n- 摸摸头不哭\n- 结果仅供参考".format(name)
        msg.add_group_msg(result)
    
def __write_to_file():
    fp=open('./jrrp.txt','w',encoding='utf-8')
    fp.write("##"+str(t)+'\n')
    for key,item in jr.items():
        fp.write("{}:{}\n".format(key,item))
    fp.close

def first_jrrp(msg:Reply):
    """每日首次发言自动jrrp"""
    #获取信息
    QQ=str(msg.user_id())
    #重新加载日期，若过期则清空数组，然后直接计算当前用户的新运势
    global t
    new_t = int((int(time.time())-1584129600)/86400)
    if new_t > t:
        jrrp(msg)
    elif QQ not in jr.keys():
        jrrp(msg) 
