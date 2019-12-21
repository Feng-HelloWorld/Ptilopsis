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

def parse(cmd,ctx):
    '''
    '''
    if re.match('^\.card$',cmd,re.I):
        cmd_card(ctx)
        pic='[CQ:image,file=out.png]'
        return pic



def cmd_card(ctx):
    '''
    输出调查员人物卡
    '''
    QQ=ctx.get('user_id')
    fileName=str(QQ)+'.txt'
    if fileName in cardDict.keys():
        cardDict[fileName].creat_pic()
    else:
        new_card(ctx)
        cardDict[fileName].creat_pic()

def new_card(ctx):
    '''
    在线新建人物卡
    '''
    QQ=ctx.get('user_id')
    name=ctx.get('sender')['card']
    if name='':
        name=ctx.get('sender')['nickname']
    if len(name)>10:
        name=name[0:10]
    fileName=str(QQ)+'.txt'
    cardDict[fileName]=investigator()
    write_card_to_file(fileName,cardDict)


#cardDict['1150640066.txt'].age_modify()
#cardDict['1150640066.txt'].creat_pic()
#cardDict['3426285834.txt'].creat_pic()
print(cardDict['3426285834.txt'].rc('jsfs',+2))
print(cardDict['3426285834.txt'].rc('jsfs'))
print(cardDict['3426285834.txt'].rc('jsfs',-2))
#print(card.dice(['2d10']))
#print(cardDict['1150640066.txt'])

#write_card_to_file('1150640066.txt',cardDict)



def printCard():
    return str(cardDict['1150640066.txt'])