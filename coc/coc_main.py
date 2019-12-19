import os
from coc.card import investigator
import re
from coc.fileIO import *

cardPath=os.path.abspath('./coc/cards')
cardList=os.listdir(cardPath)
cardDict=dict()

for name in cardList:
    if name[0:5].isdigit():
        cardDict[name]=investigator()
        read_card_from_file(name,cardDict)




cardDict['1150640066.txt'].age_modify()

print(cardDict['1150640066.txt'])

write_card_to_file('1150640066.txt',cardDict)

def printCard():
    return cardDict['1150640066.txt']