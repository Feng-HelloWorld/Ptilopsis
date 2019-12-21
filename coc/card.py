import random
import re
import copy
import make_pic

class investigator():
    def __init__(self):
        self.stats=copy.deepcopy(self.coc7th())
        self.stats['AGE_modify']=True #True表明这张卡允许进行年龄增强检定
        self.build_and_DB()
        self.hp()
        self.mov()
        self.san()
        self.mp() #此函数未完成
        #self.age_modify()
        self.skills=dict()
        self.weapon=dict()

    def __str__(self):
        data=str()
        i=0
        for key, value in self.stats.items():
            if key=='AGE_modify': key='Modi'
            data+="{:<5} {:<9}".format(key,str(value))
            i+=1
            if i%3==0:
                data+='\n'
            
        data=data+"="*40+"\n"
        for key, value in self.skills.items():
            data+="{:<5} {:<12} {:<3}\n".format(key,value[0],value[1])    
        data=data+"="*40+"\n"    
        for key, value in self.weapon.items():
            data+="{:<5} {:<8} {:<3} {}\n".format(key,value[0],value[1],value[2])  
        return data

    def __repr__(self):
        return self.__str__()

    def creat_pic(self):
        image, img=make_pic.init()
        
        make_pic.add_name_and_age(img,self.stats['NAME'],self.stats['AGE'])

        stats=['STR','CON','SIZ','DEX','APP','INT','POW','EDU','LUCK','BUILD','DB','MOV']
        dataList=list()
        for item in stats:
            dataList.append('{}: {}'.format(item,self.stats[item]))
        for item in ['HP','SAN','MP']:
            dataList.append('{}: {}/{}'.format(item,self.stats[item][0],self.stats[item][1]))
        make_pic.add_stats(img,dataList)

        dataList=list()
        for key, value in self.skills.items():
            dataList.append([key,value[0],value[1]])
        make_pic.add_skills(img,dataList)

        dataList=list()
        for key, value in self.weapon.items():
            dataList.append([key,value[0],value[1],value[2]])
        make_pic.add_weapons(img,dataList)

        make_pic.save(image,'../data/image/card_out.png')

    def add_stats(self,index,value):
        '''
        修改调查员能力值及相应调整 \n
        index: 能力值名称 str \n
        num: 数值 int
        '''
        origin=self.stats[index]
        self.stats[index]=value 
        print(index+":",origin,"->",self.stats[index])        
        if index=="STR":
            self.build_and_DB()
            self.mov()
        elif index=="SIZ":
            self.build_and_DB()
            self.hp()
            self.mov()
        elif index=="CON":
            self.hp()
        elif index=="DEX":
            self.mov()
        elif index=="AGE":
            self.mov()
        elif index=="POW":
            self.san()

    def add_skill(self,cmd,name,value):
        '''
        为调查员添加技能 \n
        cmd:自定义指令 str \n
        name:技能名称 str \n
        value:技能值 int
        '''
        self.skills[cmd]=[name,value]

    def add_weapon(self,cmd,name,value,damage):
        '''
        为调查员添加武器 \n
        cmd:自定义指令 str \n
        name:武器名称 str \n
        value:武器检定值 int \n
        dmage: 伤害 str
        '''
        self.weapon[cmd]=[name,value,damage]

    def is_skill_exist(self,cmd):
        '''
        检查技能是否已存在 \n
        cmd: 技能指令 \n
        Return: 存在返回True，否则返回False
        '''
        if cmd in self.skills.keys():
            return True
        else:
            return False

    def stats_add(self,index,num):
        '''
        对调查员能力值的增减及相应调整 \n
        index: 能力值名称 str \n
        num: 调整数值 int
        '''
        origin=self.stats[index]
        if num>0:
            self.stats[index]=self.stats[index]+num
            if self.stats[index]>99:
                self.stats[index]=99
        elif num<0:
            self.stats[index]=self.stats[index]+num
            if self.stats[index]<1:
                self.stats[index]=1    
        print(index+":",origin,"->",self.stats[index])        
        if index=="STR":
            self.build_and_DB()
            self.mov()
        elif index=="SIZ":
            self.build_and_DB()
            self.hp()
            self.mov()
        elif index=="CON":
            self.hp()
        elif index=="DEX":
            self.mov()
        elif index=="AGE":
            self.mov()
        elif index=="POW":
            self.san()

    def coc7th(self):
        '''
        根据COC7th规则随机生成人物数据 \n
        Return: 返回一个包含各项属性的字典
        '''
        Stats=dict()
        Stats['NAME']='Investigator'
        Stats['AGE']=sum(dice(['3d6']))*5
        Stats['STR']=sum(dice(['3d6']))*5
        Stats['CON']=sum(dice(['3d6']))*5
        Stats['SIZ']=sum(dice(['2d6','6']))*5
        Stats['DEX']=sum(dice(['3d6']))*5
        Stats['APP']=sum(dice(['3d6']))*5
        Stats['INT']=sum(dice(['2d6','6']))*5
        Stats['POW']=sum(dice(['3d6']))*5
        Stats['SAN']=[Stats['POW'],Stats['POW']]
        Stats['EDU']=sum(dice(['2d6','6']))*5
        Stats['LUCK']=sum(dice(['3d6']))*5
        return Stats

    #STR SIZ
    def build_and_DB(self):
        '''
        根据STR和SIZ计算体格和伤害加深 \n
        '''
        value=self.stats['STR']+self.stats['SIZ']
        if value<65:
            self.stats['BUILD']=-2
            self.stats['DB']='-2'
        elif value<85:
            self.stats['BUILD']=-1
            self.stats['DB']='-1'
        elif value<125:
            self.stats['BUILD']=0
            self.stats['DB']='0'
        elif value<165:
            self.stats['BUILD']=1
            self.stats['DB']='1d4'
        elif value<205:
            self.stats['BUILD']=2
            self.stats['DB']='1d6'
        else:
            num=(value-205)//80
            self.stats['BUILD']=3+num
            self.stats['DB']=str(2+num)+"d6"

    #CON SIZ
    def hp(self):
        '''
        根据CON和SIZ计算HP
        '''
        num=(self.stats['CON']+self.stats['SIZ'])//10
        self.stats['HP']=[num,num] #血量值表示为包含两个int的list，格式为[当前血量,最大血量]

    #POW
    def san(self):
        '''
        根据POW计算SAN
        '''
        num=self.stats['POW']
        self.stats['SAN']=[num,num] #理智值表示为包含两个int的list，格式为[当前理智,最大理智]

    def mp(self):
        self.stats['MP']=[0,0]


    #DEX STR SIZ AGE
    def mov(self):
        '''
        根据DEX，STR，SIZ和AGE计算MOV
        '''
        Dex=self.stats['DEX']
        Str=self.stats['STR']
        Siz=self.stats['SIZ']
        Age=self.stats['AGE']
        if Dex<Siz and Str<Siz:
            self.stats['MOV']=7
        elif Dex>Siz and Str>Siz:
            self.stats['MOV']=9
        else:
            self.stats['MOV']=8
        Age=Age-30
        if Age>0:
            self.stats['MOV']=self.stats['MOV']-Age//10

    def age_modify(self):
        '''
        根据年龄进行增强检定
        '''
        Age=self.stats['AGE']
        Modify=self.stats['AGE_modify']
        if Modify:
            if Age>=15 and Age<20:
                num1=random.randint(0,5)
                num2=5-num1
                self.stats_add('STR',-num1)
                self.stats_add('SIZ',-num2)
                self.stats_add('EDU',-5)
                #幸运增强检定
                luck2=random.randint(1,100)
                if luck2>self.stats['LUCK']:
                    self.stats_add('LUCK',luck2)
            elif Age<40:
                #教育增强检定
                edu2=random.randint(1,100)
                if edu2>self.stats['EDU']:
                    num=sum(dice(['d10']))
                    self.stats_add('EDU',num)
            elif Age<50:
                num1=random.randint(0,5)
                num2=random.randint(0,5-num1)
                num3=5-num1-num2
                self.stats_add('STR',-num1)
                self.stats_add('CON',-num2)
                self.stats_add('DEX',-num3)
                self.stats_add('APP',-5)
                #教育增强检定
                for i in range(2):
                    edu2=random.randint(1,100)
                    if edu2>self.stats['EDU']:
                        num=sum(dice(['d10']))
                        self.stats_add('EDU',num)
            elif Age<60:
                num1=random.randint(0,10)
                num2=random.randint(0,10-num1)
                num3=10-num1-num2
                self.stats_add('STR',-num1)
                self.stats_add('CON',-num2)
                self.stats_add('DEX',-num3)
                self.stats_add('APP',-10)
                #教育增强检定
                for i in range(3):
                    edu2=random.randint(1,100)
                    if edu2>self.stats['EDU']:
                        num=sum(dice(['d10']))
                        self.stats_add('EDU',num)        
            elif Age<70:
                num1=random.randint(0,20)
                num2=random.randint(0,20-num1)
                num3=20-num1-num2
                self.stats_add('STR',-num1)
                self.stats_add('CON',-num2)
                self.stats_add('DEX',-num3)
                self.stats_add('APP',-15)
                #教育增强检定
                for i in range(4):
                    edu2=random.randint(1,100)
                    if edu2>self.stats['EDU']:
                        num=sum(dice(['d10']))
                        self.stats_add('EDU',num)
            elif Age<80:
                num1=random.randint(0,40)
                num2=random.randint(0,40-num1)
                num3=40-num1-num2
                self.stats_add('STR',-num1)
                self.stats_add('CON',-num2)
                self.stats_add('DEX',-num3)
                self.stats_add('APP',-20)
                #教育增强检定
                for i in range(4):
                    edu2=random.randint(1,100)
                    if edu2>self.stats['EDU']:
                        num=sum(dice(['d10']))
                        self.stats_add('EDU',num)     
            elif Age<90:
                num1=random.randint(0,80)
                num2=random.randint(0,80-num1)
                num3=80-num1-num2
                self.stats_add('STR',-num1)
                self.stats_add('CON',-num2)
                self.stats_add('DEX',-num3)
                self.stats_add('APP',-25)
                #教育增强检定
                for i in range(4):
                    edu2=random.randint(1,100)
                    if edu2>self.stats['EDU']:
                        num=sum(dice(['d10']))
                        self.stats_add('EDU',num)
        self.stats['AGE_modify']=False

    def sc(self,cmdList1,cmdList2):
        '''
        '''
        roll=dice()
        success = roll<=self.stats['POW']
        if success:
            value=sum(dice(cmdList1))*-1
            self.status_add('SAN',value)
        else:
            value=sum(dice(cmdList2))*-1
            self.status_add('SAN',value)
        return roll, success, value

    def status_add(self,index,num):
        '''
        对调查员状态值的增减及相应调整 \n
        index: 状态值名称 str \n
        num: 调整数值 int
        '''
        origin=self.stats[index][0]
        if num>0:
            self.stats[index][0]=self.stats[index][0]+num
            if self.stats[index][0]>self.stats[index][1]:
                self.stats[index][0]=self.stats[index][1]
        elif num<0:
            self.stats[index][0]=self.stats[index][0]+num
            if self.stats[index][0]<0:
                self.stats[index][0]=0  
        return origin, self.stats[index][0]

    def rc(self,index,cmd=0):
        '''
        '''
        roll=sum(dice())
        add=list()
        if cmd!=0:
            add=add_dice(roll,cmd)
            level=ra_rc(self.skills[index][1],add[0])
        else:
            level=ra_rc(self.skills[index][1],roll) 
        return [roll,level]+add

def ra_rc(stander,value):
    '''
    '''
    opppps=99
    if stander<50:
        opppps=95
    # 1     2        3      4      5        6      7       8
    #大成功 极难成功 困难成功 普通成功 压线成功 压线失败 普通失败 大失败
    if value==1:
        return 1
    elif value<=stander//5:
        return 2
    elif value<=stander//2:
        return 3
    elif value<stander:
        return 4
    elif value==stander:
        return 5
    elif value==stander+1:
        return 6
    elif value>opppps:
        return 8
    else:
        return 7
    
def add_dice(value,cmd):
    '''
    '''
    if cmd>0:
        add=dice([str(cmd)+'d10'])
        for i in range(len(add)):
            add[i]=add[i]-1
            temp=add[i]*10+value%10
            if temp<value:
                value=temp
                if value<1:
                    value=1
    elif cmd<0:
        add=dice([str(cmd*-1)+'d10'])
        for i in range(len(add)):
            temp=add[i]*10+value%10
            if temp>value:
                value=temp
                if value>100:
                    value=100
    return [value]+add
            
def dice(cmdList=['d100']):
    '''
    根据指令列表进行投掷检定 \n
    cmdList: 指令列表 list(str) \n
    Return: 投掷值列表 list(int)
    '''
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
            minus(dataList,negative,num[0])
        elif len(num)==2:
            # +d
            if num[0]=="" and num[1]=="":
                minus(dataList,negative,random.randint(1,100))
            # +d100
            elif num[0]=="" and num[1]>=1:
                minus(dataList,negative,random.randint(1,num[1]))
            # +3d
            elif num[1]=="" and num[0]>=1:
                for i in range(0,num[0]):
                    minus(dataList,negative,random.randint(1,100))
            # +3d100
            elif num[1]>=1 and num[0]>=1:
                for i in range(0,num[0]):
                    minus(dataList,negative,random.randint(1,num[1]))
    return dataList

def minus(dataList,negative,value):
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




