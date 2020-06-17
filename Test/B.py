import os
import sys
import re
import importlib
sys.path.append('./Mods')


path = './Mods/'
dirList = os.listdir(path)
print(dirList)
cmds = dict()
for name in dirList:
    if '.' not in name:
        print('Importing mod:',name)
        sys.path.append('./Mods/'+name)
        modCfg = importlib.import_module(name+'.Cmd')
        print('Before:',modCfg.cmdList)
        cmds.update(modCfg.cmdList)
        print('After:',cmds)


cmd =input('Enter CMD: ')
for key, func in cmds.items():
    if re.match(key, cmd):
        func()