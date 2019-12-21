import sys
sys.path.append('./coc')

import os
from card import investigator
import re
from fileIO import *
from nonebot.typing import Context_T

cardPath=os.path.abspath('./coc/cards')
cardList=os.listdir(cardPath)
cardDict=dict()

#初始化代码，载入目录中所有卡
for name in cardList:
    if name[0:5].isdigit():
        cardDict[name]=investigator()
        read_card_from_file(name,cardDict)

SUCCESS=[1:'你开挂了吧',2:'极难成功',3:'困难成功',4:'普通成功',5:'差点失败',6:'差点成功',7:'蔡',8:'你人没了']



def parse(cmd,ctx):
    '''
    '''
    QQ=ctx.get('user_id')
    fileName=str(QQ)+'.txt'

    if fileName not in cardDict.keys():
        new_card(ctx)
    Card=cardDict[fileName]
    if re.match('^\.card$',cmd,re.I):
        Card.creat_pic()
        return True
    elif re.match('^\.HP[\+\-]\d*',cmd,re.I):
        value=int(cmd[3:])
        origin, now = Card.status_add('HP',value)
        return origin, now
    elif re.match('^\.SAN[\+\-]\d*',cmd,re.I):
        value=int(cmd[3:])
        origin, now = Card.status_add('SAN',value)
        return origin, now
    elif re.match('^\.MP[\+\-]\d*',cmd,re.I):
        value=int(cmd[3:])
        origin, now = Card.status_add('MP',value)
        return origin, now
    elif re.match('^\.rc[\+\-]?\d? .+$',cmd,re.I):
        temp=cmd.strip().split(' ')
        item=temp[1]
        add_cmd=0
        if len(temp[0])>3:
            add_cmd=int(temp[0][3:])
        result = Card.rc(skill,add_cmd)
        if item in ['STR','CON','SIZ','DEX','APP','INT','POW','EDU','LUCK']:
            item_ch=item
        elif item in Card.skills.keys():
            item_ch=Card.skills[item][0]
        if len(result)<3:
            msg='\*{}进行检定 出目[{}]\n{}'.format(Card.stats['NAME'],result[0],SUCCESS[result[1]])
        else:
            final=result[2]
            i=3
            a=' '
            while i<len(result):
                a=a+str(result[i])+' '
            msg='\*{}进行检定 出目[{}]->{}->[{}]\n{}'.format(Card.stats['NAME'],result[0],a,final,SUCCESS[result[1]])
        return msg
    
    or re.match('^\.SAN[\+\-]\d*',cmd,re.I) or re.match('^\.MP[\+\-]\d*',cmd,re.I):



def new_card(ctx):
    '''
    在线新建人物卡
    '''
    QQ=ctx.get('user_id')
    name=ctx.get('sender')['card']
    if name=='':
        name=ctx.get('sender')['nickname']
    if len(name)>10:
        name=name[0:10]
    fileName=str(QQ)+'.txt'
    cardDict[fileName]=investigator()
    cardDict[fileName].add_stats('NAME',name)
    write_card_to_file(fileName,cardDict)


#cardDict['1150640066.txt'].age_modify()
#cardDict['1150640066.txt'].creat_pic()
#cardDict['3426285834.txt'].creat_pic()
#print(cardDict['3426285834.txt'].rc('jsfs',+2))
#print(cardDict['3426285834.txt'].rc('jsfs'))
#print(cardDict['3426285834.txt'].rc('jsfs',-2))
#print(card.dice(['2d10']))
#print(cardDict['1150640066.txt'])

#write_card_to_file('1150640066.txt',cardDict)



def printCard():
    return str(cardDict['1150640066.txt'])