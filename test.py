import time
import json

#cfg = dict()

def loadSettings():
    print("!!!")
    fp = open('test.json', 'r',encoding="utf-8") 
    print(fp)
    return json.load(fp)

cfg = loadSettings()

print("Type: ", type(cfg),"\n", cfg)


