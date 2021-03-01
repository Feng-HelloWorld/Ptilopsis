import random

#普通骰            
def dice(cmd_list=['+d100']):
    '''
    根据指令列表进行投掷检定 \n
    cmd_list: 指令列表 list(str) \n
    Return: 投掷值
    '''
    sum=0
    for cmd in cmd_list:
        cmd=cmd.lower()
        #判断指令是否为减
        negative=1
        if cmd[0]=='-':negative=-1
        cmd=cmd[1:]
        num=cmd.split("d")
        #将str转换成int
        for i in range(len(num)):
            if num[i].isdigit():
                num[i]=int(num[i])
        #检查并投掷
        if len(num)==1:
            # +50
            sum += negative*num[0]
        elif len(num)==2:
            # +d
            if num[0]=="" and num[1]=="":
                sum += negative*random.randint(1,100)
            # +d100
            elif num[0]=="" and num[1]>=1:
                sum += negative*random.randint(1,num[1])
            # +3d
            elif num[1]=="" and num[0]>=1:
                for i in range(0,num[0]):
                    sum += negative*random.randint(1,100)
            # +3d100
            elif num[1]>=1 and num[0]>=1:
                for i in range(0,num[0]):
                    sum += negative*random.randint(1,num[1])
    return sum

#奖惩骰
def add_dice(ori_dice:int,cmd:str):
    ''''''
    print('Param',ori_dice,cmd)
    cmd = int(cmd)
    dice_list = list()
    if cmd>0:#奖励骰
        for i in range(cmd):
            temp = random.randint(0,9)
            dice_list.append(temp)
            if temp<ori_dice/10:ori_dice = temp*10 + ori_dice%10
            if ori_dice<1:ori_dice=1
    elif cmd<0:#惩罚骰
        for i in range(cmd*-1):
            temp = random.randint(1,10)
            dice_list.append(temp)
            if temp>ori_dice/10:ori_dice = temp*10 + ori_dice%10
            if ori_dice>100:ori_dice=100
    return (ori_dice,dice_list)
            