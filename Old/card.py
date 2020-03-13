import random
import re
import copy
import make_pic

#有一类东西，叫调查员卡
class card():
    def __init__(self):

#它有以下属性：
#调查员名称NAME，年龄AGE，编号NO
#十大属性（STR，CON，SIZ，DEX，APP，INT，POW，SAN，EDU，LUCK）
#基于上值计算出的属性BUILD，DB，MOV
#以及以下可变属性：
    #HP_NOW/HP
    #SAN_NOW/SAN
    #MP_NOW/MP

#它还有一个技能列表，里面存储了一些技能的名称，代码和成功率
#它还有一个武器列表，里面存储了一些武器的名称，代码，成功率和伤害

#它可以做以下事情：
#对指定的技能或属性项目进行检定rc
#使用指定的武器进行攻击检定和伤害检定
#对san值进行特殊方式的检定
#允许对自身属性的查询操作
#对自身能力值进行修改，同时检查此属性的修改是否影响其他值
#使用自身存储的数据，生成一张jpg格式的人物卡
#将自身存储的数据写入到文件中
#从文件中读取数据



    def coc7th(self, reply):
        '''
        根据COC7th规则随机生成人物数据 \n
        Return: 返回一个包含各项属性的字典
        '''
        Stats=dict()
        sum=0
        Stats['NAME']='深海猎人'
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
        for value in Stats:
            if value.isdigit():
                sum +=value
        return Stats

