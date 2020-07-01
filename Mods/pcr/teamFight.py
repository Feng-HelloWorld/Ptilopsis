from reply import Reply
from funcs import *
from dice import *
from pic import checkAttendencePic, thankPic
import json
import random
import re

cfg = dict()
data = dict()

cfgPath = './Mods/pcr/teamFight.json'
logPath = './Mods/pcr/teamFight.log'
dataPath = './Mods/pcr/data.json'

cfg = loadSettings(cfgPath)
data = loadSettings(dataPath)

#加入公会
async def jiaru(reply:Reply, text:str):
    '''加入公会'''
    if reply.group_id() in cfg['bot_on']:

        reply.add_group_msg('* 该功能已被禁用，请联系管理员')
        await reply.send()
        '''
        id = text[4:]
        if str(reply.user_id()) not in cfg['member'].keys():
            cfg['member'][str(reply.user_id())] = id
            cfg['member_init'][str(reply.user_id())] = 3
            cfg['member_name'][str(reply.user_id())] = reply.user_name()
            await saveSettings(cfgPath, cfg)
            reply.add_group_msg('* {}[{}]加入本群公会\n- 注册ID [{}]'.format( reply.user_name(), reply.user_id(), id ))
            await reply.send()
        else:
            cfg['member_name'][str(reply.user_id())] = reply.user_name()
            await saveSettings(cfgPath, cfg)
            reply.add_group_msg('* {}已加入本群公会\n- 注册ID [{}]'.format( reply.user_name(), cfg['member'][str(reply.user_id())] ))
            await reply.send()    
        '''        
    else:
        print('[ERRO] 加入公会指令未在此群开启')

#退出公会
async def tuichu(reply:Reply, text:str):
    '''退出公会'''
    if reply.group_id() in cfg['bot_on']:
        if str(reply.user_id()) in cfg['member'].keys():
            reply.add_group_msg('* 该功能已被禁用，请联系管理员')
            await reply.send()
            '''
            cfg['member'].pop(str(reply.user_id() ))
            cfg['member_init'].pop(str(reply.user_id() ))
            cfg['member_name'].pop(str(reply.user_id() ))
            await saveSettings(cfgPath, cfg)
            reply.add_group_msg('* {}[{}]已退出本群公会'.format( reply.user_name(), reply.user_id() ))
            await reply.send()
            '''
        else:
            reply.add_group_msg('* 用户[{}]不存在'.format( reply.user_id() ))
            await reply.send()
    else:
        print('[ERRO] 退出公会指令未在此群开启')

#踢出公会
async def tichu(reply:Reply, text:str):
    '''踢出公会'''
    if reply.group_id() in cfg['bot_on'] and reply.user_id() in cfg['admin']:
        id = text[4:]
        if id in cfg['member'].keys():
            cfg['member'].pop(id)
            cfg['member_init'].pop(id)
            cfg['member_name'].pop(id)
            await saveSettings(cfgPath, cfg)
            reply.add_group_msg('* 用户[{}]已被踢出本群公会'.format( id ))
            await reply.send()
        else:
            reply.add_group_msg('* 用户[{}]不存在'.format( id ))
            await reply.send()
    else:
        print('[ERRO] 踢出公会指令未在此群开启或没有管理员权限')

#状态
async def zhuangtai(reply:Reply, text:str):
    '''状态'''
    if reply.group_id() in cfg['bot_on']:
        if str(reply.user_id()) in cfg['member'].keys():
            
            reply.add_group_msg("当前第{}周目Boss{} 剩余血量[{:,d}]".format(data['term'], data['boss'], data['hp']))
            await reply.send()
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 报刀指令未在此群开启')

#报刀
async def baodao(reply:Reply, text:str):
    '''报刀'''
    if reply.group_id() in cfg['bot_on']:
        if str(reply.user_id()) in cfg['member'].keys():
            await dayChange(reply)
            damage=int(text[2:])
            if damage<1:
                reply.add_group_msg('* 伤害过低，请报掉刀\n- 指令:"掉刀"')
                await reply.send()
            elif damage>cfg['max_damage']:
                reply.add_group_msg('* 伤害超过上限，请联系管理员\n- 本条记录未写入')
                await reply.send()           
            elif damage<data['hp']:
                if str(reply.user_id()) not in data['today_logs'].keys():#新建用户名
                    data['today_logs'][str(reply.user_id())]=list()
                    data['today_logs'][str(reply.user_id())].append("Name: "+reply.user_name())
                if str(reply.user_id()) not in data['absent'].keys():#新建上限
                    data['absent'][str(reply.user_id())]=cfg['member_init'][str(reply.user_id())]
                #检查出刀数
                left = data['absent'][str(reply.user_id())]
                if left>0:
                    #数据写入
                    if left%1==0.5:#这一刀是补刀
                        left -= 0.5
                        log_type = '补刀'
                    else:#这一刀是整刀
                        left -= 1
                        log_type = '整刀'  
                    data['absent'][str(reply.user_id())]=left  
                    num = cfg['member_init'][str(reply.user_id())]-left
                    data['hp']-=damage
                    temp = { 'Time':reply.time().print(), 'Boss':data['boss'], 'Type':log_type, 'Num':num, 'Damage':damage }
                    
                    data['today_logs'][str(reply.user_id())].append(temp)
                    await saveSettings(dataPath, data)
                    #发送消息
                    reply.add_group_msg('* {}今日第[{}]刀 {}\n- 对{}周目Boss{}造成[{:,d}]伤害\n- 剩余血量 [{:,d}]'.format(reply.user_name(), temp['Num'] , log_type , data['term'], data['boss'], damage, data['hp']))
                    await reply.send()
                    #写入log
                    await writeLog(logPath, '{}  {}第[{}]刀{},对{}周目Boss{}造成[{:,d}]伤害,剩余血量[{:,d}]'.format(reply.time().print(), reply.user_name(), temp['Num'] , log_type , data['term'], data['boss'], damage, data['hp']))
                    #thank
                    if left==0:
                        #结算总伤害
                        sum = 0
                        for item in data['today_logs'][str(reply.user_id())][1:]:
                            sum += item['Damage']
                        await thankPic(reply.user_name(), reply.user_id(), sum)
                        reply.add_group_msg('[CQ:image,file=thankPic.jpg]')
                        await reply.send()  
                    
                else:
                    reply.add_group_msg('* 今日出刀数已满，如有错误请联系管理员')
                    await reply.send()                    
            else:
                reply.add_group_msg('* 伤害超过剩余血量，请报尾刀\n- 指令:"尾刀"')
                await reply.send()
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 报刀指令未在此群开启')

#尾刀
async def weidao(reply:Reply, text:str):
    '''尾刀'''
    if reply.group_id() in cfg['bot_on']:
        if str(reply.user_id()) in cfg['member'].keys():
            await dayChange(reply)
            damage = data['hp']
            if data['hp']>cfg['max_damage']:
                reply.add_group_msg('* 不是吧不是吧，这么猛的吗？\n- 本条记录未写入')
                await reply.send()           
            else:
                #检查出刀数
                if str(reply.user_id()) not in data['today_logs'].keys():#新建用户名
                    data['today_logs'][str(reply.user_id())]=list()
                    data['today_logs'][str(reply.user_id())].append("Name: "+reply.user_name())
                if str(reply.user_id()) not in data['absent'].keys():#新建上限
                    data['absent'][str(reply.user_id())]=cfg['member_init'][str(reply.user_id())]
                left = data['absent'][str(reply.user_id())]-0.5
                if left>0:
                    #数据写入
                    data['absent'][str(reply.user_id())]=left  
                    num = cfg['member_init'][str(reply.user_id())]-left
                    temp = { 'Time':reply.time().print(), 'Boss':data['boss'], 'Type':'尾刀', 'Num':num, 'Damage':damage }
                    data['today_logs'][str(reply.user_id())].append(temp)
                    #发送消息
                    reply.add_group_msg('* {}今日第[{}]刀 尾刀\n- 对{}周目Boss{}造成[{:,d}]伤害\n- 当前Boss已被击杀'.format(reply.user_name(), temp['Num'] , data['term'], data['boss'], damage))
                    await reply.send()
                    #数据写入2
                    if data['boss']==5:
                        data['boss']=0
                        data['term']+=1
                    data['boss']+=1
                    data['hp']=cfg['boss_init'][data['boss']-1]
                    await saveSettings(dataPath, data)
                    #写入log
                    await writeLog(logPath, '{}  {}第[{}]刀尾刀,对{}周目Boss{}造成[{:,d}]伤害,当前Boss已被击杀'.format(reply.time().print(), reply.user_name(), temp['Num'] , data['term'], data['boss'], damage))
                    #砍树
                    if len(data['tree'])>0:
                        temp = '[下树通知] '
                        for id in data['tree']:
                            temp += ' [CQ:at,qq={}] '.format(id)
                        reply.add_group_msg(temp)
                        await reply.send() 
                    #预约
                    if len( data['subscribe'][data['boss']-1] )>0:
                        for id in data['subscribe'][data['boss']-1]:
                            reply.add_private_msg('[预约提醒] 你预约的Boss[{}]已可供挑战'.format(data['boss']))
                            await reply.send()
                else:
                    reply.add_group_msg('* 今日出刀数已满，如有错误请联系管理员')
                    await reply.send()                    

        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 尾刀指令未在此群开启')

#查刀
async def chadao(reply:Reply, text:str):
    '''查刀'''
    if reply.group_id() in cfg['bot_on']:
        if str(reply.user_id()) in cfg['member'].keys():
            await dayChange(reply)
            damage = data['hp']

            temp = list()
            for id, left in data['absent'].items():
                if left>0:
                    temp.append((int(left), cfg['member_name'][str(id)]))
            await checkAttendencePic(temp)
            reply.add_group_msg('[CQ:image,file=checkAttendencePic.jpg]')
            await reply.send()
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 查刀指令未在此群开启')

#日期变换
async def dayChange(reply:Reply):
    now = Time()
    if not now.isSameDay(Time(data['record_date']),5):
        await writeLog(logPath,"===============\nDay Change\n=====================")
        data['record_date'] = now.print()
        data['absent']=cfg['member_init']
        data['today_logs']=dict()
        await saveSettings(dataPath, data)
        
#挂树
async def guashu(reply:Reply, text:str):
    if data['hp']>5000000:
        reply.add_group_msg('* 救不了救不了')
        await reply.send() 
    else:
        data['tree'].append(reply.user_id())
        await saveSettings(dataPath, data)
        reply.add_group_msg('* 挂上了挂上了')
        await reply.send() 

#下树
async def xiashu(reply:Reply, text:str):
    if reply.user_id() in data['tree']:
        data['tree'].remove(reply.user_id())
        await saveSettings(dataPath, data)
        reply.add_group_msg('* 下来了下来了')
        await reply.send() 
    else:
        reply.add_group_msg('* 你在哪你在哪')
        await reply.send() 

#查树
async def chashu(reply:Reply, text:str):
    if len(data['tree'])>0:
        temp = "* 爬树爱好者名单:"
        for id in data['tree']:
            temp += "\n- {}".format(  cfg['member_name'][str(  id  )]  )
        reply.add_group_msg(temp)
    else:
        reply.add_group_msg('* 树上无人，岁月静好')
    await reply.send()

#预约
async def yuyue(reply:Reply, text:str):
    index = int(text[2:])-1
    if reply.user_id() not in data['subscribe'][index]:
        data['subscribe'][index].append(reply.user_id())
        await saveSettings(dataPath, data)
        reply.add_group_msg('* 已预约Boss[{}], 当鲨到此Boss时会收到提醒'.format(index+1))
        await reply.send() 

#取消预约
async def quxiaoyuyue(reply:Reply, text:str):
    index = int(text[4:])-1
    if reply.user_id() in data['subscribe'][index]:
        data['subscribe'][index].remove(reply.user_id())
        await saveSettings(dataPath, data)
        reply.add_group_msg('* 已取消预约Boss[{}]'.format(index+1))
        await reply.send() 