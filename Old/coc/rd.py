import re
from dice import dice
from reply import Reply

def rd(raw:str,msg:Reply):
    """rd指令"""
    reason = '普通骰子'
    if re.match('.+ .+',raw):
        temp = raw.strip().split(' ')
        raw = temp[0]
        reason = temp[1]
    raw = raw[2:]
    cmdList = []
    cmds = raw.strip().split('+')
    for cmd in cmds:
        if (re.match('^\d*[dD]\d*$',cmd) or re.match('^\d+$',cmd)):
            cmdList.append(cmd)
        else:
            msg.add_group_msg("你说这些谁懂啊？\n[CQ:image,file=exc.jpg]")
            print("**WARN：指令错误！")
            return 0
            break
    result = dice(cmdList)
    msg.add_group_msg("* {}投掷 {} [{}]\n- 出目[{}]".format(msg.user_name(),raw.lower(),reason,result[0]))