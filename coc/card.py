import random
import re
import copy

skill={
    "ACCOUNTING":5,
    "ACTING":5,
    "ANIMAL_HANDLING":5,
    "ANTHROPOLOGY":1,
    "APPRAISE":5,
    "ARCHAEOLOGY":1,
    "ART_AND_CRAFT":5,
    "ARTILLERY":1,
    "ASTRONOMY":1,
    "AXE":15,
    "BIOLOGY":1,
    "BOTANY":1,
    "BOW":15,
    "BRAWL":25,
    "CHAINSAW":10,
    "CHARM":15,
    "CHEMISTRY":1,
    "CLIMB":20,
    "COMPUTER_USE":5,
    "CREDIT_RATING":0,
    "CRYPTOGRAPHY":1,
    "CTHULHU_MYTHOS":0,
    "DEMOLITIONS":1,
    "DISGUISE":5,
    "DIVING":1,
    "DRIVE_AUTO":20,
    "ELECTRICAL_REPAIR":10,
    "ELECTRONICS":1,
    "FAST_TALK":5,
    "FINE_ART":5,
    "FIRST_AID":30,
    "FLAIL":10,
    "FLAMETHROWER":10,
    "FORENSICS":1,
    "FORGERY":5,
    "GARROTE":15,
    "GEOLOGY":1,
    "HANDGUN":20,
    "HEAVY_WEAPONS":10,
    "HISTORY":5,
    "HYPNOSIS":1,
    "INTIMIDATE":15,
    "JUMP":20,
    "LANGUAGE_OTHER":1,
    "LAW":5,
    "LIBRARY_USE":20,
    "LISTEN":20,
    "LOCKSMITH":1,
    "MACHINE_GUN":10,
    "MATHEMATICS":1,
    "MECHANICAL_REPAIR":10,
    "MEDICINE":1,
    "METEOROLOGY":1,
    "NATURAL_WORLD":10,
    "NAVIGATE":10,
    "OCCULT":5,
    "OPERATE_HEAVY_MACHINERY":1,
    "PERSUADE":10,
    "PHARMACY":1,
    "PHOTOGRAPHY":5,
    "PHYSICS":1,
    "PILOT":1,
    "PSYCHOANALYSIS":1,
    "PHYCHOLOGY":10,
    "READ_LIPS":1,
    "RIDE":5,
    "RIFLE":25,
    "SCIENCE":1,
    "SHOTGUN":25,
    "SLEIGHT_OF_HAND":10,
    "SPEAR":20,
    "SPOT_HIDDEN":25,
    "STEALTH":20,
    "SUBMACHINE_GUN":15,
    "SURVIVAL":10,
    "SWORD":20,
    "SWIM":20,
    "THROW":20,
    "TRACK":10,
    "WHIP":5,
    "ZOOLOGY":1
    }


class investigator():
    def __init__(self):
        self.stats=copy.deepcopy(self.coc7th())
        self.stats['AGE_modify']=True #True表明这张卡允许进行年龄增强检定
        self.build_and_DB()
        self.hp()
        self.mov()
        #self.age_modify()
        self.skills=copy.deepcopy(self.skill())

    def __str__(self):
        data=str()
        for key, value in self.stats.items():
            data+="{:>12} {:<9}\n".format(key,str(value))
        data=data+"="*20+"\n"
        for key, value in self.skills.items():
            data+="{:>24} {:<9}\n".format(key,str(value))        
        return data
    
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

    def skill(self):
        '''
        生成一份均为默认值的技能字典
        '''
        Skill=copy.deepcopy(skill)
        Skill["LANGUAGE_OWN"]=self.stats['EDU']
        Skill["DODGE"]=self.stats['DEX']//2
        return Skill
    
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


"""
def build_and_DB(value):
    '''
    计算体格和伤害加深 \n
    value: STR+SIZ int \n
    Return: 体格 int, 伤害加深 cmdList
    '''
    
    if value<65:
        return -2, '-2'
    elif value<85:
        return -1, '-1'
    elif value<125:
        return 0, '0'
    elif value<165:
        return 1, '1d4'
    elif value<205:
        return 2, '1d6'
    else:
        num=(value-205)//80
        return [3+num, str(2+num)+"d6"]
"""  

