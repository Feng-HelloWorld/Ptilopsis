import random


class dice:
    raw_numbers = list()
    raw_sum = int()

#普通骰            
def dice(cmdList=['+d100']):
    '''
    根据指令列表进行投掷检定 \n
    cmdList: 指令列表 list(str) \n
    Return: 投掷值列表 tuple(int,list(int))
    '''
    sum=0
    dataList=list() # 返回用的列表
    for cmd in cmdList:
        cmd=cmd.lower()
        #判断指令是否为减
        negative=False
        if cmd[0]=='+':
            cmd=cmd[1:]
        elif cmd[0]=='-':
            cmd=cmd[1:]
            negative=True
        num=cmd.split("d")
        #将str转换成int
        for i in range(0,len(num)):
            if num[i].isdigit():
                num[i]=int(num[i])
        #检查并投掷
        if len(num)==1:
            # +50
            __minus(dataList,negative,num[0])
        elif len(num)==2:
            # +d
            if num[0]=="" and num[1]=="":
                __minus(dataList,negative,random.randint(1,100))
            # +d100
            elif num[0]=="" and num[1]>=1:
                __minus(dataList,negative,random.randint(1,num[1]))
            # +3d
            elif num[1]=="" and num[0]>=1:
                for i in range(0,num[0]):
                    __minus(dataList,negative,random.randint(1,100))
            # +3d100
            elif num[1]>=1 and num[0]>=1:
                for i in range(0,num[0]):
                    __minus(dataList,negative,random.randint(1,num[1]))
    for num in dataList:
        sum += num
    result=(sum,dataList)
    return result

#减函数
def __minus(dataList,negative,value):
    '''
    dice()函数附属函数，用于检查投掷值是否应为负数 \n
    negative: 若为True，则加入dataList的值变更为负数 \n
    value: 等待加入dataList的值 \n
    dataList: 返回值列表
    '''
    if negative:
        dataList.append(value*-1)
    else:
        dataList.append(value)