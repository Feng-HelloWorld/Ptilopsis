import nonebot
from funcs import Time

bot = nonebot.get_bot()

#Class for reply
class Reply:

    #Protected var
    __messages_for_group = list()
    __messages_for_private = list()
    __user_id = int()
    __user_name = str()
    __group_id = int()
    __time = Time()

    def __init__(self, user_id:int, user_name:str, group_id:int):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__group_id = group_id
        self.__time = Time()
        self.__messages_for_private=list()
        self.__messages_for_group=list()

    def add_group_msg(self, msg:str, id=000):
        if id==000:id=self.__group_id
        self.__messages_for_group.append( (msg,id) )

    def add_private_msg(self, msg:str, id=000):
        if id==000:id=self.__user_id
        self.__messages_for_private.append( (msg,id) )

    def user_name(self):
        return self.__user_name

    def user_id(self):
        return self.__user_id

    def group_id(self):
        return self.__group_id

    def time(self):
        return self.__time

    async def send(self):
        for message in self.__messages_for_group:
            msg = message[0]
            id = message[1]
            print("==GROUP REPLY {:=<12d}======\n{}".format(id,msg))
            await bot.send_group_msg(group_id=id,message=msg)

        for message in self.__messages_for_private:
            msg = message[0]
            id = message[1]
            print("==PRIVATE REPLY {:=<12d}====\n{}".format(id,msg))
            await bot.send_private_msg(user_id=id,message=msg)

        self.__messages_for_private=list()
        self.__messages_for_private.clear()
        self.__messages_for_group=list()
        self.__messages_for_group.clear()
        print("="*32)

async def checkUserInfo(group_id, user_id):
    info = await bot.get_group_member_info(group_id=group_id,user_id=user_id,no_cache=True)
    return info