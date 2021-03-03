from funcs.msgPack import gMsgP
from funcs.dice import dice
from funcs.dataBase import DataBase
from funcs.time import Time
from libs.dataBaseError import *
from random import choice
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain

#日志数据库导入
try:
    db = DataBase('./data/logs.db3')
    db.creat_table('ROLL',[('time','TEXT'),('user_id','INT'),('user_name','TEXT'),('reason','TEXT'),('cmd','TEXT'),('sum','INT'),('result','TEXT')])
except OperationalError as e:
    print(e)
#日志表单
log = db['ROLL'] 

#词库
adj_list_1 = ['光明正大','大摇大摆','嚣张至极','信心十足','不慌不忙','镇定自若','一本正经','不置可否','心平气和','张扬跋扈','吊儿郎当','心高气傲','一反常态','装模做样','颤颤巍巍','做贼心虚']

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if re.match('^\.r(h?)(\d*d\d*[^ ]*)( \S+)?$',text):
        return rd(text, mp)
    else:
        return False

def cmd_friend():
    pass


def rd(text:str,msg:gMsgP):
    """rd指令"""
    temp = re.match('^\.r(h?)(\d*d\d*[^ ]*)( \S+)?$',text)
    try:
        hide = temp.group(1)
        cmds = '+'+temp.group(2)
        comment = temp.group(3)
        if not comment==None:comment='名为'+comment[1:]+'的'#删掉注释前面的空格并修改格式
        else:comment=''
        cmd_list = re.findall('[\+\-]\d*d?\d*',cmds)#拆分指令串
        result = dice(cmd_list)
        if hide=='h':
            return MessageChain.create([Plain(f'* {msg.sender.name}悄咪咪地扔了一次{comment}骰子，但是骰子不见了')])
            # reply.add_group_msg('* {}悄咪咪地扔了一次{}骰子'.format(reply.user_name(), comment))
            # reply.add_private_msg('* 悄悄告诉你，投掷的{}骰子出目为[{}]'.format(comment,result))
            # await writeLog(logPath, '[rh]{} {}[{}]在群[{}]投掷了一次{}骰子({})，出目[{}]'.format(reply.time().print(),reply.user_name(),reply.user_id(),reply.group_id(),comment,cmds,result))
        else:
            time = str(Time().print())
            id = int(msg.sender.id)
            name = str(msg.sender.name)
            reason = comment
            if not reason=='':reason=comment[2:-1]
            cmd = str(cmds[1:])
            sum = int(result[0])
            detail = str(result[1])
            log.add([time,id,name,reason,cmd,sum,detail])
            reply = f'* {name}{choice(adj_list_1)}地扔了一次{comment}骰子\n- {cmd} 出目[{sum}]'
            if len(result[1])>1:reply+=f'\n- 细则{detail}'
            return MessageChain.create([Plain(reply)])
    except:
        return MessageChain.create([Plain('[!] 你说这些谁懂啊？')])
































def success_level(d100:int,stander:int):
    '''根据传入检定结果和成功率，返回成功等级'''
    if d100==1:
        return (10,"大成功")
    elif d100<=stander/5:
        return (9,"极难成功")
    elif d100<=stander/2:
        return (8,"困难成功")
    elif d100<=stander:
        return (7,"成功")
    elif d100==100 or (d100>95 and stander<50):
        return (5,"大失败")
    else:
        return (6,"失败")

async def ra(reply, text:str):
    ''''''
    #print('开始执行ra指令')
    if reply.group_id() in cfg['bot_on']:
        temp = re.match('^\.ra([\+\-][1-3])? ([^\d ]*)[ ]?(\d+)([\+\-]\d+)?$',text)
        #print('Temp值：',temp)
        try:
            add = temp.group(1)
            #print('Add',add)
            comment = temp.group(2)
            if comment==None:comment=''#默认值
            #print('Comment',comment)
            buff = temp.group(4)
            if buff==None:buff=0
            #print('Buff',buff)
            stander = int(temp.group(3)) + int(buff)
            #print('Stander',stander)
            if stander<0 or stander>100:raise RuntimeError('[ERRO] ra检定值参数错误: {}'.format(stander))
            ori_dice = dice()#扔一个百分骰
            #print('Ori',ori_dice)
            if add==None:
                result = success_level(ori_dice,stander)
                #print('Result',result)
                reply.add_group_msg('* {}进行了一次成功率{}%的{}检定\n- 出目[{}]  {}'.format(reply.user_name(),  stander,comment, ori_dice, result[1]) )
                await writeLog(logPath, '[ra]{} {}[{}]在群[{}]进行了一次成功率{}%的{}检定 出目[{}]{}'.format(reply.time().print(),reply.user_name(),reply.user_id(),reply.group_id(),  stander,comment, ori_dice, result[1]) )
            else:
                final_dice = add_dice(ori_dice, add)
                #print('Final Dice',final_dice)
                result = success_level(final_dice[0],stander)
                #print('Result',result)
                dice_type = '惩罚骰'
                if int(add)>0:dice_type='奖励骰'
                reply.add_group_msg('* {}进行了一次成功率{}%的{}检定\n- 出目[{}]  {}{}\n- 最终检定结果[{}]  {}'.format( reply.user_name(), stander, comment, ori_dice, dice_type, final_dice[1], final_dice[0], result[1] ))
                await writeLog(logPath, '[ra]{} {}[{}]在群[{}]进行了一次成功率{}%的{}检定({}) {}{} 出目[{}]{}'.format( reply.time().print(),reply.user_name(),reply.user_id(),reply.group_id(),  stander,comment, ori_dice, dice_type, final_dice[1], final_dice[0], result[1] ))
            await reply.send()
        except:
            reply.add_group_msg('你说这些谁懂啊？\n[CQ:image,file=exc.jpg]')      
            await reply.send()      
    else:
        print('[ERRO] ra指令未在此群开启')