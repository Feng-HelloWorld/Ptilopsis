import os
from card import investigator
import re
from fileIO import *

cardPath=os.path.abspath('./coc/cards')
cardList=os.listdir(cardPath)
cardDict=dict()

#初始化代码，载入目录中所有卡
for name in cardList:
    if name[0:5].isdigit():
        cardDict[name]=investigator()
        read_card_from_file(name,cardDict)




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