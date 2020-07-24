import random


class Level:
    '''同级池子模板'''
    __all_items=list()
    __up_items=list()
    __up_probability=0 #数值为0-10000，精度为小数点后4位，2550意味出现概率为25.50%

    def __init__(self, all_items:list):
        self.__all_items = all_items
    
    def setUpItem(self, up_item:list):
        self.__up_items = up_item

    def setUpProbability(self, up_probability:int):
        self.__up_probability = up_probability
    
    def cancleUP(self):
        self.__up_items = list()
        self.__up_probability = 0
    
    def extract(self):
        if random.randint(1,10000)<self.__up_probability and len(self.__up_items)>0:
            return random.choice(self.__up_items)
        else:
            result = random.choice(self.__all_items)
            while result in self.__up_items:
                result = random.choice(self.__all_items)
            return result

'''
l1 = ['能天使','星熊','安洁莉娜','银灰','艾雅法拉','伊芙利特']
l1up = ['能天使']
sixStar = Level(l1)
sixStar.setUpItem(l1up)
sixStar.setUpProbability(5000)
sum = 0
num = 10
for i in range(num):
    #print(sixStar.extract())
    if sixStar.extract() in l1up:
        sum+=1
print(sum/num)
'''


class Event:
    '''卡池模板'''
    __all_level=list() 

    def addLevel(self, level:Level, count:int):
        for i in range(count):
            self.__all_level.append(level)
    
    def extract(self):
        return random.choice(self.__all_level).extract()

'''
l1 = ['能天使','星熊','安洁莉娜','银灰','艾雅法拉','伊芙利特']
l1up = ['能天使','安洁莉娜']
l2 = ['天火','赫默','白面鸮','惊蛰','德克萨斯','拉普兰德','送葬人','华法林','红','食铁兽','崖心','阿米娅','白金','蓝毒']
l2up = ['赫默','白面鸮','德克萨斯']
l3 = ['波登可','末药','调香师','桃金娘','红豆','讯使','霜叶','角峰','古米','蛇屠箱','暗锁','阿消','远山']

aknz = Event()
sixStar = Level(l1)
sixStar.setUpItem(l1up)
sixStar.setUpProbability(5000)
fiveStar = Level(l2)
fiveStar.setUpItem(l2up)
fiveStar.setUpProbability(5000)
fourStar = Level(l3)
aknz.addLevel(sixStar,2)
aknz.addLevel(fiveStar,8)
aknz.addLevel(fourStar,90)

num = 500
l1c = 0
l1uc = 0
l2c = 0
l2uc = 0
l3c = 0


for i in range(num):
    result = aknz.extract()
    if result in l1:
        l1c +=1
        if result in l1up:
            l1uc +=1
    elif result in l2:
        l2c +=1
        if result in l2up:
            l2uc +=1
    else:
        l3c +=1

print(l1c/num, l1uc/l1c)
print(l2c/num, l2uc/l2c)
print(l3c/num)

'''

