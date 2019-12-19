import os
from card import investigator
import copy
import re
from fileIO import *

cardPath=os.path.abspath('./coc/cards')
#print(cardPath)
cardList=os.listdir(cardPath)
cardDict=dict()
print('cardList',cardList)

"""
for name in cardList:
    if not name[0:5].isdigit():
        continue
    cardDict[name]=investigator()
    fp=open('./coc/cards/'+name,"r",encoding='utf-8')
    lineNum=0
    for line in fp:
        lineNum+=1
        if lineNum<30 and line!='' and line[0:1]!="=":
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
    fp.close()
"""

for name in cardList:
    if name[0:5].isdigit():
        cardDict[name]=investigator()

read_card_from_file('1150640066.txt',cardDict)

cardDict['1150640066.txt'].age_modify()

print(cardDict['1150640066.txt'])

write_card_to_file('1150640066.txt',cardDict)