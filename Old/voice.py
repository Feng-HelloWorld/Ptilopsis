from reply import Reply
from random import choice
import re

def sing(txt,msg:Reply):
    if re.match("^\.peko$",txt):
        msg.add_group_msg("[CQ:record,file=你的胖次几厘米.mp3,magic=false]")
    elif re.match("^\.korone$",txt):
        msg.add_group_msg("[CQ:record,file=吼辣迷迭吼辣呦.mp3,magic=false]")
    elif re.match("^\.fubuki$",txt):
        msg.add_group_msg("[CQ:record,file=fbk.mp3,magic=false]")
    elif re.match("^\.kanata$",txt):
        msg.add_group_msg("[CQ:record,file=kanata.mp3,magic=false]")
    elif re.match("^\.aqua$",txt):
        msg.add_group_msg("[CQ:record,file=Neeeeeeeee.mp3,magic=false]")
    elif re.match("^\.matsuri$",txt):
        msg.add_group_msg("[CQ:record,file=斯哈斯哈.mp3,magic=false]")
    elif re.match("^\.索兰$",txt):           
        msg.add_group_msg("[CQ:record,file=索兰调.mp3,magic=false]")
    elif re.match("^\.hatto$",txt):
        msg.add_group_msg("[CQ:record,file=我爱你.mp3,magic=false]")
    elif re.match("^\.watame$",txt):
        msg.add_group_msg("[CQ:record,file=棉芽rap.mp3,magic=false]")
    elif re.match("^\.suisei$",txt):
        msg.add_group_msg("[CQ:record,file=噫hihihihi.mp3,magic=false]")


sleep_voice = list()
sleep_voice.append("[CQ:record,file=未闻花名.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=晚安.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=棉芽安眠曲.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=Yagoo大家族.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=狐狸歌1.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=狐狸歌2.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=奇异恩典.mp3,magic=false]")
sleep_voice.append("[CQ:record,file=现在还不能休息哦.mp3,magic=false]")

def sleep(msg:Reply):
    msg.add_group_msg(choice(sleep_voice))

