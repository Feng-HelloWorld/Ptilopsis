from random import randint, choice
import time

start_sleep = list()
start_sleep.append("* 快去睡啦咕~")
start_sleep.append("* 博士又睡着了吗？剩下的工作我来做吧")
start_sleep.append("* 不早啦，快点睡吧")
start_sleep.append("* 晚安，好梦")
start_sleep.append("* 要去找个音声听吗？")
#start_sleep.append("* 博士，您还有许多事情需要处理，现在还不能休息哦")

start_sleep_voice = list()
start_sleep_voice.append("[CQ:record,file=未闻花名.mp3,magic=false]")
start_sleep_voice.append("[CQ:record,file=晚安.mp3,magic=false]")
start_sleep_voice.append("[CQ:record,file=棉芽安眠曲.mp3,magic=false]")




#
def sleep(ctx, msg):
    QQ = ctx["user_id"]
    if QQ == 407670050:
        msg[0].append("[CQ:record,file=现在还不能休息哦.mp3,magic=false]")
    else:
        ran = randint(1,10)
        if ran<8:
            msg[0].append(choice(start_sleep))
        else:
            msg[0].append(choice(start_sleep_voice))

