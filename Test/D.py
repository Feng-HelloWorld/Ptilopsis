import re

while True:
    text = input('>>>')
    if text=='stop':break
    temp = re.match('^\.r(h?)(\d*d\d*[^ ]*)( \S+)?$',text)
    hide = temp.group(1)
    print(hide)
    cmds = '+'+temp.group(2)
    print(cmds)
    comment = temp.group(3)
    print(comment)

    cmd = re.findall('[\+\-]\d*d?\d*',cmds)
    print(cmd)
    
    if comment==None:print("="+cmds+"=")
    else:print("="+cmds+"=",'\n='+comment+'=')