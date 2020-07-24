from reply import Reply
from funcs import *
from dice import *
from pic import checkAttendencePic, thankPic
from copy import deepcopy
import json
import random
import re
import requests

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
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            r = await rank(reply, 'string')
            reply.add_group_msg("* 当前第{}周目Boss[{}] 剩余血量[{:,d}]\n{}".format(data['term'], data['boss'], data['hp'], r))
            await reply.send()
            
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 报刀指令未在此群开启')

#排行
async def rank(reply:Reply, text:str):
    '''获取公会排名'''
    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            #检查是否已获取到最新数据
            if time.time()-data['rank'][1]<1800:
                rank = data['rank'][0]
                t = Time(data['rank'][1]).print()[11:16]
                if text=="string":return "- 公会{}排名 [{}]位".format(t,rank)#以字符串形式返回
                reply.add_group_msg("* 公会{}排名 [{}]位".format(t,rank))
                await reply.send()
            else:
                #获取排名
                header = {
                    'Host': 'service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com',
                    'Connection': 'keep-alive',
                    'Content-Length': '21',
                    'DNT': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Origin': 'https://kengxxiao.github.io',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://kengxxiao.github.io/Kyouka/'
                }
                result = requests.post('https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/name/0', data=json.dumps({'clanName':'桃星'}), headers=header)
                if result.status_code==200:
                    temp = result.json()
                    rank = temp['data'][0]['rank']
                    t = Time(temp['ts']).print()[11:16]
                    #更新数据文件
                    if not temp['ts']== data['rank'][1]:
                        data['rank'][0]=rank
                        data['rank'][1]=temp['ts']
                        await saveSettings(dataPath, data)
                    if text=="string":return "- 公会{}排名 [{}]位".format(t,rank)#以字符串形式返回
                    reply.add_group_msg("* 公会{}排名 [{}]位".format(t,rank))
                    await reply.send()

                else:
                    if text=="string":return "[ERRO] 服务器发生错误 返回值[{}]".format(result.status_code)#以字符串形式返回
                    reply.add_group_msg("[ERRO] 服务器发生错误\n- 返回值[{}]".format(result.status_code))
                    await reply.send()
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 排行指令未在此群开启')

#报刀
async def baodao(reply:Reply, text:str):
    '''报刀'''
    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
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
                        left = int(left)
                        log_type = '补刀'
                    else:#这一刀是整刀
                        left -= 1
                        log_type = '整刀'  
                    data['absent'][str(reply.user_id())]=left  
                    num = cfg['member_init'][str(reply.user_id())]-left
                    data['hp']-=damage
                    temp = { 'Time':reply.time().print(), 'Boss':data['boss']+data['term']*10, 'Type':log_type, 'Num':num, 'Damage':damage }
                    data['today_logs'][str(reply.user_id())].append(temp)
                    await saveSettings(dataPath, data)
                    #发送消息
                    reply.add_group_msg('* {}今日第[{}]刀 {}\n- 对{}周目Boss[{}]造成[{:,d}]伤害\n- 剩余血量 [{:,d}]'.format(reply.user_name(), temp['Num'] , log_type , data['term'], data['boss'], damage, data['hp']))
                    await reply.send()
                    #写入log
                    await writeLog(logPath, '{}  {}第[{}]刀{},对{}周目Boss[{}]造成[{:,d}]伤害,剩余血量[{:,d}]'.format(reply.time().print(), reply.user_name(), temp['Num'] , log_type , data['term'], data['boss'], damage, data['hp']))
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
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
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
                if left%1==0: left = int(left) #将left切回整数
                if left>0:
                    #数据写入
                    data['absent'][str(reply.user_id())]=left  
                    num = cfg['member_init'][str(reply.user_id())]-left
                    temp = { 'Time':reply.time().print(), 'Boss':data['boss']+data['term']*10, 'Type':'尾刀', 'Num':num, 'Damage':damage }
                    data['today_logs'][str(reply.user_id())].append(temp)
                    #发送消息
                    reply.add_group_msg('* {}今日第[{}]刀 尾刀\n- 对{}周目Boss[{}]造成[{:,d}]伤害\n- 当前Boss已被击杀'.format(reply.user_name(), temp['Num'] , data['term'], data['boss'], damage))
                    await reply.send()
                    #数据写入2
                    if data['boss']==5:
                        data['boss']=0
                        data['term']+=1
                    data['boss']+=1
                    data['hp']=cfg['boss_init'][data['boss']-1]
                    await saveSettings(dataPath, data)
                    #写入log
                    await writeLog(logPath, '{}  {}第[{}]刀尾刀,对{}周目Boss[{}]造成[{:,d}]伤害,当前Boss已被击杀'.format(reply.time().print(), reply.user_name(), temp['Num'] , data['term'], data['boss'], damage))
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
                            reply.add_private_msg('[预约提醒] 你预约的Boss[{}]已可供挑战'.format(data['boss']), id)
                            await reply.send()
                        data['subscribe'][data['boss']-1] = list()
                else:
                    reply.add_group_msg('* 今日出刀数已满，如有错误请联系管理员')
                    await reply.send()                    

        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 尾刀指令未在此群开启')

#修正
async def xiuzheng(reply:Reply, text:str):
    pass

#撤销
async def chexiao(reply:Reply, text:str):
    '''撤销'''
    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            await dayChange(reply)
            if str(reply.user_id()) in data['today_logs'].keys():
                #获取数据
                record=data['today_logs'][str(reply.user_id())][-1]
                if record['Boss']==data['boss']+data['term']*10:
                    #Boss回血
                    data['hp']+=record['Damage']
                    #写入日志
                    await writeLog(logPath, '{}  {}第[{}]刀{}被撤回,剩余血量[{:,d}]'.format(reply.time().print(), reply.user_name(),record['Num'],record['Type'],data['hp']) )
                    #发送消息
                    reply.add_group_msg('* {}今日第[{}]刀 {} 被撤回\n- Boss剩余血量[{:,d}]'.format( reply.user_name(),record['Num'],record['Type'],data['hp']))
                    await reply.send()
                    #记刀数增加
                    if record['Type']=='整刀':
                        data['absent'][str(reply.user_id())]+=1
                    else:
                        data['absent'][str(reply.user_id())]+=0.5
                    #数据擦除
                    if len(record)==2:
                        data['today_logs'].pop(str(reply.user_id()))
                    else:
                        data['today_logs'][str(reply.user_id())].pop()
                    await saveSettings(dataPath,data)
                else: 
                    reply.add_group_msg('* 只能撤回对当前Boss造成的伤害')
                    await reply.send() 
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 撤销指令未在此群开启')

#查刀
async def chadao(reply:Reply, text:str):
    '''查刀'''
    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
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
        await writeLog(logPath,"=====================\nDay Change\n=====================")
        data['record_date'] = now.print()
        data['absent']=deepcopy(cfg['member_init'])
        data['today_logs']=dict()
        await saveSettings(dataPath, data)
        
#挂树
async def guashu(reply:Reply, text:str):

    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            if data['hp']>5000000:
                reply.add_group_msg('* 救不了救不了')
                await reply.send() 
            else:
                data['tree'].append(reply.user_id())
                await saveSettings(dataPath, data)
                reply.add_group_msg('* 挂上了挂上了')
                await reply.send() 
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 查刀指令未在此群开启')

    

#下树
async def xiashu(reply:Reply, text:str):

    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            if reply.user_id() in data['tree']:
                data['tree'].remove(reply.user_id())
                await saveSettings(dataPath, data)
                reply.add_group_msg('* 下来了下来了')
                await reply.send() 
            else:
                reply.add_group_msg('* 你在哪你在哪')
                await reply.send() 
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 查刀指令未在此群开启')

    

#查树
async def chashu(reply:Reply, text:str):

    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            if len(data['tree'])>0:
                temp = "* 爬树爱好者名单:"
                for id in data['tree']:
                    temp += "\n- {}".format(  cfg['member_name'][str(  id  )]  )
                reply.add_group_msg(temp)
            else:
                reply.add_group_msg('* 树上无人，岁月静好')
            await reply.send()
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 查树指令未在此群开启')

    

#预约
async def yuyue(reply:Reply, text:str):

    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            index = int(text[2:])-1
            if reply.user_id() not in data['subscribe'][index]:
                data['subscribe'][index].append(reply.user_id())
                await saveSettings(dataPath, data)
                reply.add_group_msg('* 已预约Boss[{}], 当此Boss可供挑战时会收到提醒'.format(index+1))
                await reply.send() 
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 预约指令未在此群开启')



#取消预约
async def quxiaoyuyue(reply:Reply, text:str):

    if reply.group_id() in cfg['bot_on']:
        if reply.time()>Time(cfg['open_time'][1]) or reply.time()<Time(cfg['open_time'][0]):
            reply.add_group_msg('* 当前不在公会战开放时间\n- 开始时间:{}\n- 结束时间:{}'.format( cfg['open_time'][0],cfg['open_time'][1] ))
            await reply.send()
        elif str(reply.user_id()) in cfg['member'].keys():
            index = int(text[4:])-1
            if reply.user_id() in data['subscribe'][index]:
                data['subscribe'][index].remove(reply.user_id())
                await saveSettings(dataPath, data)
                reply.add_group_msg('* 已取消预约Boss[{}]'.format(index+1))
                await reply.send() 
        else:
            reply.add_group_msg('* 请先加入公会\n- 指令:"加入公会"+13位数字ID')
            await reply.send()   
    else:
        print('[ERRO] 取消预约指令未在此群开启')

