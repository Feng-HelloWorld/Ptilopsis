import nonebot
import re
from nonebot.typing import Context_T
import sys
import time
sys.path.append('./coc')
from coc.rd import rd
from coc.ra import ra
from jrrp import jrrp, first_jrrp
#<<<<<<< Updated upstream
#from webGet import biliSearch, bvSearch
#from ban import is_ban, ban
#from sleep import sleep
#
#from coc.coc import coc7th
#=======
#from webGet import biliSearch, bvSearch
#from ban import is_ban, ban
#from sleep import sleep
from random import choice
#from coc.coc import coc7th
#>>>>>>> Stashed changes

bot = nonebot.get_bot()

#炼铜
lastTime = 0


#其余指令时间限制
lt_sleep = 0
lt_sound = 0
lt_hyl = 0
lt_ll = 0
lt_qks = 0


#私聊消息处理
@bot.on_message('private') 
async def handle_private_message(ctx: Context_T):
    #print("====================\n",ctx,"\n========================\n")
    pass

#群消息处理
@bot.on_message('group') 
async def handle_group_message(ctx: Context_T):
    #print("====================\n",ctx,"\n========================\n")
    t = int(time.time())
    global lastTime
    global lt_sound
    #消息返回值
    pub=[]
    pri=[]
    msg=(pub,pri)
    print("\n====================Message Receive====================\n")
    print("群号：",ctx.get("group_id"),"\n")
    print(ctx.get("raw_message"),"\n")

    
    print("==========\n")
    #如果消息为纯文本
    if is_only_text(ctx):
        #消息文本
        txt = ctx['raw_message']

        if txt=='wwssaaddabab':
            msg[0].append('输出测试')
            msg[0].append('copyright@2020 Ptilposis')
            msg[1].append('[CQ:record,file=未闻花名.mp3,magic=false]')
#<<<<<<< Updated upstream
#=======
        #ra指令
        elif re.match('^\.ra [0-9]+$',txt,re.I):
            ra(txt,ctx,msg) 
            
#>>>>>>> Stashed changes
        #rd指令
        elif re.match('^\.r\d*d\d*.*$',txt,re.I):
            #if is_ban(ctx,msg):
            rd(txt,ctx,msg)
        #coc7th指令
        elif re.match('^\.coc7th',txt,re.I):
            if is_ban(ctx,msg):
                coc7th(txt,ctx,msg)
        #jrrp指令
        elif txt==".jrrp":
            #if is_ban(ctx,msg):
            jrrp(ctx,msg)
        #ban指令
        elif re.match("^\.ban [0-9]+$",txt,re.I):
            if is_ban(ctx,msg):
                ban(ctx,txt,msg)
        #sleep指令 
        elif re.match("^\.sleep$",txt,re.I) and t-lt_sleep > 30:
            #if is_ban(ctx,msg):
            sleep(ctx, msg)
        elif re.match("^.*granbluefantasy\.jp.*$",txt,re.I) and t-lt_qks > 30:
            msg[0].append("到处都是骑空士的陷阱")
        elif re.match("^好运来$",txt) and t-lt_hyl > 120:
            msg[0].append("[CQ:record,file=好运来.mp3,magic=false]")
        elif re.match("^凉凉$",txt) and t-lt_ll > 120:
            msg[0].append("[CQ:record,file=凉凉.mp3,magic=false]")
        #炼铜检测
        elif re.match(".*炼铜.*",txt) or re.match(".*恋童.*",txt) :
            if t-lastTime>120:
                msg[0].append("[CQ:record,file=FBIOpentheDoor.mp3,magic=false]")
                await send_msg(msg,ctx)
                #msg[0][0]="《中华人民共和国刑法》规定："
                #msg[0].append("* 第二百三十六条：以暴力、胁迫或者其他手段强奸妇女的，处三年以上十年以下有期徒刑。")
                #msg[0].append("- 奸淫不满十四周岁的幼女的，以强奸论，从重处罚...")                
                #msg[0].append("* 第二百三十七条：以暴力、胁迫或者其他方法强制猥亵妇女或者侮辱妇女的，处五年以下有期徒刑或者拘役。")
                #msg[0].append("- 聚众或者在公共场所当众犯前款罪的，处五年以上有期徒刑。")
                #msg[0].append("- 猥亵儿童的，依照前两款的规定从重处罚。")
                #msg[0].append("* 第二百六十二条：拐骗不满十四周岁的未成年人，脱离家庭或者监护人的，处五年以下有期徒刑或者拘役。")
                #msg[0].append("* 第三百六十条：...嫖宿不满十四周岁的幼女的，处五年以上有期徒刑，并处罚金。")
                msg[0].append('''http://www.npc.gov.cn/wxzl/wxzl/2000-12/17/content_4680.htm''')
            lastTime = t
        elif t-lt_sound > 20:
            if re.match("^\.peko$",txt):
                msg[0].append("[CQ:record,file=你的胖次几厘米.mp3,magic=false]")
            elif re.match("^\.korone$",txt):
                msg[0].append("[CQ:record,file=吼辣迷迭吼辣呦.mp3,magic=false]")
            elif re.match("^\.fubuki$",txt):
                msg[0].append("[CQ:record,file=fbk.mp3,magic=false]")
            elif re.match("^\.kanata$",txt):
                msg[0].append("[CQ:record,file=kanata.mp3,magic=false]")
            elif re.match("^\.aqua$",txt):
                msg[0].append("[CQ:record,file=Neeeeeeeee.mp3,magic=false]")
            elif re.match("^\.matsuri$",txt):
                msg[0].append("[CQ:record,file=斯哈斯哈.mp3,magic=false]")
            elif re.match("^\.索兰$",txt):           
                msg[0].append("[CQ:record,file=索兰调.mp3,magic=false]")
            elif re.match("^\.hatto$",txt):
                msg[0].append("[CQ:record,file=我爱你.mp3,magic=false]")
            elif re.match("^\.watame$",txt):
                msg[0].append("[CQ:record,file=棉芽rap.mp3,magic=false]")
            elif re.match("^\.suisei$",txt):
                msg[0].append("[CQ:record,file=噫hihihihi.mp3,magic=false]")
        else:
            #每日首次发非指令消息时自动执行jrrp
            first_jrrp(ctx,msg)text
            #检测bv号
            bvSearch(text,msg)

        #发送消息
        await send_msg(msg,ctx)
    
    #如果是bilibili小程序分享
    elif(is_bili_share(ctx)):
        name = is_bili_share(ctx)
        biliSearch(name,msg)
        await send_msg(msg,ctx)

async def send_msg(msg:tuple, ctx: Context_T):
    """
    发送消息 \n
    msg: 消息列表\n
    ctx: 用于查询群号和用户QQ\n
    Return: 无
    """
    #要发送到群里的列表，每个元素之间增加空格
    if len(msg[0])>0:
        reply=connect(msg[0])
        print(reply)
        await bot.send_group_msg(group_id=ctx.get('group_id'),message=reply)
    #要发送给私人的列表，每个元素之间增加空格
    if len(msg[1])>0:
        reply=connect(msg[1])
        await bot.send_private_msg(user_id=ctx.get('sender').get('user_id'),message=reply)
    print("\n====================Message Send====================\n")

def connect(l:list):
    """
    把一个list拼接成一个带换行的string
    """
    result=str()
    for i in range(len(l)):
        result+=l[i]
        if i<len(l)-1:
            result+="\n"
    return result

def is_only_text(ctx: Context_T):
    '''
    检查此消息是否只含有文本 \n
    Return: 布尔值
    '''
    msg=ctx['message']
    if len(msg)==1:
        if msg[0]['type']=='text':
            return True
    return False

def is_bili_share(ctx: Context_T):
    """
    检查此消息是否为哔哩哔哩小程序 \n
    Return: 返回视频标题，或者返回false
    """
    try:
        if(ctx['message'][0]["data"]["title"]=="&#91;QQ小程序&#93;哔哩哔哩"):
            msg = ctx['message'][0]["data"]["content"]
            return re.search('desc":"[^}]*"',msg).group()[7:-1]
        else:
            return False
    except:
        return False

