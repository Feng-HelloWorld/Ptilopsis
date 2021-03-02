
#五子棋异常类
class Base(Exception):
    msg:str
    def __init__(self, msg:str=None):
        if msg:self.msg = msg
    def __str__(self):return self.msg

class AlreadyInGame(Base):
    def __init__(self, msg:str):self.msg = f'[!] 你已经加入了房间{msg}，专心把这一局打完哦'

class NotInGame(Base):
    msg = '[!] 你还没有加入任何房间'

class RoomNotExist(Base):
    def __init__(self, msg:str):self.msg = f'[!] 房间{msg}不存在，真的没有输错吗？'

class RoomFull(Base):
    def __init__(self, msg:str):self.msg = f'[!] 房间{msg}人满为患啦'

class NoEnoughPlayer(Base):
    def __init__(self, msg:str):self.msg = f'[!] 房间{msg}的人数不够，没法继续游戏啦= ='

class NotYourTurn(Base):
    msg = '[!] 当前不是你的回合'

class AlreadyHavePiece(Base):
    def __init__(self, x:int, y:int):self.msg = f'[!] 点({x},{y})已经有一颗子啦，换一个地方下吧'

class OutOfBoard(Base):
    msg = '[!] 不要把子下在棋盘外啦= ='