import re
from dice import dice

def rd(raw:str,ctx,msg:tuple):
    """
    rd指令\n
    raw: 指令原文\n
    ctx\n
    msg\n
    Return: 无
    """
    raw = raw[2:]
    cmdList = []
    try:
        cmds = raw.strip().split('+')
        for cmd in cmds:
            if (re.match('^\d*[dD]\d*$',cmd) or re.match('^\d+$',cmd)):
                cmdList.append(cmd)
            else:
                raise Exception
                break
        result = dice(cmdList)
        msg[0].append("* "+__getName(ctx)+"投掷"+raw.lower())
        msg[0].append("- 出目："+str(result[0]))
    except Exception:
        msg[0].append("你说这些谁懂啊？")
        #msg[0].append('[CQ:image,file=exc.jpg]')
        print("**WARN：指令错误！")

def __getName(ctx):
    """
    获取用户名 \n
    ctx \n
    Return: 若用户有马甲就返回马甲，没有就返回昵称 (str)
    """
    nick = ctx['sender']['card']
    name = ctx['sender']['nickname']
    if nick=='': return name
    else: return nick