import re
import asyncio
from Arcapi import AsyncApi, SyncApi
from funcs.miniapp import miniapp as App
from funcs.time import Time
from funcs.msgPack import gMsgP
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    if re.match('^.recent[0-9]{9}$',text):
        return __arc_score(text)
    else:
        return False


diff_dict={0:"[Past]",1:"[Present]",2:"[Future]"}

def __score_cal(s:int):
    if s>=9900000:return "EX+"
    elif s>=9800000:return "EX"
    elif s>=9500000:return "AA"
    elif s>=9200000:return "A"
    elif s>=8900000:return "B"
    elif s>=8600000:return "C"
    else:return "D"

def __arc_score(text:str):
    user_code = re.match('^.recent([0-9]{9})$',text).group(1)
    try:
        api_ = SyncApi(user_code=user_code) 
        data = api_.user()
        # api_ = AsyncApi(user_code=user_code)
        # data = asyncio.get_event_loop().run_until_complete(api_.user())

        user = data[1]
        name = user["name"]+"的记录"
        song = data[0][user["recent_score"][0]["song_id"]]['en']
        diff = diff_dict[user["recent_score"][0]["difficulty"]]+ str(user["recent_score"][0]["constant"])
        score = "[{}] {:,}".format(__score_cal(user["recent_score"][0]["score"]),user["recent_score"][0]["score"])
        pure = user["recent_score"][0]["perfect_count"]
        near = user["recent_score"][0]["near_count"]
        miss = user["recent_score"][0]["miss_count"]
        grade = "{:.3f}".format(user["recent_score"][0]["rating"])
        time = Time(user["recent_score"][0]["time_played"]/1000).print(flag="[Y]-[M]-[D] [h]:[m]")
        appD = [("难度",diff),("分数",score),("Pure",pure),("Near",near),("Miss",miss),("评分",grade),("游玩时间",time)]
        appB = []

        app = App(prompt="Arcaea",app_name=name, title=song,app_data=appD, app_button=appB)
        msg = MessageChain.create([app])
        return msg
    except:
        return MessageChain.create([Plain("[ERRO] API接口发生错误，检查参数是否正确")])


# {
#     "user_id": 1446269,
#     "name": "ShirolOvOl",
#     "recent_score": [
#         {
#             "song_id": "garakuta",
#             "difficulty": 1,
#             "score": 9703277,
#             "shiny_perfect_count": 480,
#             "perfect_count": 544,
#             "near_count": 22,
#             "miss_count": 6,
#             "clear_type": 5,
#             "best_clear_type": 2,
#             "health": 96,
#             "time_played": 1612062654036,
#             "modifier": 2,
#             "rating": 7.17759,
#             "constant": 6.5,
#             "song_date": 1558573200
#         }
#     ],
#     "character": 7,
#     "join_date": 1552738459439,
#     "rating": 1000,
#     "is_skill_sealed": false,
#     "is_char_uncapped": false,
#     "is_char_uncapped_override": false,
#     "is_mutual": false,
#     "rating_records": [
#         [
#             "210131",
#             "1000"
#         ]
#     ],
#     "user_code": "041285347"
# },