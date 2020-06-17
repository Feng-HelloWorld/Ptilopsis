import re
from dice import dice
from reply import Reply
from random import choice

def ra(raw:str,msg:Reply):
    stander = int(raw[3:].strip())
    d100 = dice()[0]
    level = list()
    if d100==1:
        level = ["大成功"]
    elif d100<=stander/5:
        level = ["极难成功"]
    elif d100<=stander/2:
        level = ["困难成功"]
    elif d100<=stander:
        level = ["成功"]
    elif d100==100 or (d100>95 and stander<50):
        level = ["大失败"]
        msg.add_group_msg("[CQ:record,file=凉凉.mp3,magic=false]")
    else:
        level = ["失败"]           
    msg.add_group_msg("* {}进行检定 出目[{}]\n- {}".format(msg.user_name(),d100,choice(level)))



#奖惩骰
def add_dice(value,cmd):
    '''
    '''
    if cmd>0:
        add=dice([str(cmd)+'d10'])
        for i in range(len(add)):
            add[i]=add[i]-1
            temp=add[i]*10+value%10
            if temp<value:
                value=temp
                if value<1:
                    value=1
    elif cmd<0:
        add=dice([str(cmd*-1)+'d10'])
        for i in range(len(add)):
            temp=add[i]*10+value%10
            if temp>value:
                value=temp
                if value>100:
                    value=100
    return [value]+add