import os
from card import investigator
import copy

cardPath=os.path.abspath('./coc/cards')
print(cardPath)
cardList=os.listdir(cardPath)
cardDict=dict()

for name in cardList:
    if name.isdigit():
        cardDict[name]=investigator()
        fp=open('./coc/cards/'+name,"r",encoding='utf-8')
        lineNum=1
        for line in fp:
            if lineNum==1:
                pass
            elif line[0:3]=="STR":
                cardDict[name].stats['STR']=line[4:6]
                cardDict[name].stats['CON']=line[12:14]
                cardDict[name].stats['SIZ']=line[20:22]
                cardDict[name].stats['DEX']=line[28:30]
            elif line[0:3]=="APP":
                cardDict[name].stats['APP']=line[4:6]
                cardDict[name].stats['INT']=line[12:14]
                cardDict[name].stats['POW']=line[20:22]
                cardDict[name].stats['EDU']=line[28:30]
        print(cardDict[name])
