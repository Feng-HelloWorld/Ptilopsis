import os
from card import investigator
import copy
import re

cardPath=os.path.abspath('./coc/cards')
#print(cardPath)
cardList=os.listdir(cardPath)
cardDict=dict()

for name in cardList:
    cardDict[name]=investigator()
    fp=open('./coc/cards/'+name,"r",encoding='utf-8')
    lineNum=0
    for line in fp:
        lineNum+=1
        if lineNum<24 and line!='' and line[0:1]!="=":
            try:
                temp=line.strip().split(':')
                print('stats: ',temp)
                if (temp[0] in ['NAME','DB']) and temp[2]!='':
                    cardDict[name].stats[temp[0]]=temp[2]
                elif temp[0] in ['HP','SAN','MP']:
                    value=temp[2].strip().split('/')
                    cardDict[name].stats[temp[0]]=[int(value[0]),int(value[1])]
                else:
                    cardDict[name].stats[temp[0]]=int(temp[2])
            except:
                pass
        elif line!='' and line[0:1]!='=':
            try:
                temp=line.strip().split(':')
                print("temp:",temp)
                if len(temp)==3:
                    cardDict[name].add_skill(temp[0],temp[1],int(temp[2]))
                elif len(temp)==4:
                    cardDict[name].add_weapon(temp[0],temp[1],int(temp[2]),temp[3])
            except:
                pass

    print(cardDict[name])
