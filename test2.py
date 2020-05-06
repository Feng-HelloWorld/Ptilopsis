import time


class Caaa:
    #Protected var
    _messages_for_group = list()
    _messages_for_private = list()
    _user_id = int()
    _user_name = str()
    __group_id = 0

    def __init__(self, user_id:int, user_name:str, group_id:int):

        self._user_id = user_id
        self._user_name = user_name
        self.__group_id = group_id
        print("* New reply created.\n- USER_ID {}  USER_NAME {}  GROUP {}".format(self._user_id,self._user_name,self.__group_id))


    def add_group_msg(self, msg:str, id=000000):
        if id==000000:id=self.__group_id
        print("2* NEW REPLY IN [{}] ADDED:{}".format(id,msg))
        self._messages_for_group.append( (msg,id) )

def p(a:str,b:int=1):
    print("a{}s{}d".format(a,b))

p(333)

cc = Caaa(10,"aaa","456")
cc.add_group_msg("jhgfds")


