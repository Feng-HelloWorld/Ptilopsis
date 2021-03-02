import re
import os
from random import randint
from copy import deepcopy
from funcs.msgPack import gMsgP
from libs.gomokuError import *
from PIL import Image, ImageDraw, ImageFont
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.application.message.elements.internal import Image as Picture

def cmd_group(mp:gMsgP):
    text = mp.msg.asDisplay()
    try:
        if re.match('^发起五子棋挑战$',text):
            return __creat_game(mp)
        elif re.match('^加入[0-9]{5}$',text):
            return __join_game(mp, text[2:])
        elif re.match('^退出房间$',text): 
            return __exit_game(mp)      
        elif re.match('^[\(（][\+\-]?[0-7][\,，][\+\-]?[0-7][\)）]$',text) and mp.sender.id in gamers.keys():
            return __go(mp, text)
        elif re.match('^查看[0-9]{5}$',text):
            return __check(mp, text[2:])
        elif re.match('^发起麻将挑战$',text):
            return MessageChain.create([Plain('https://game.maj-soul.com/1/')])
        elif re.match('.有无雀魂.',text):
            return MessageChain.create([Plain('https://game.maj-soul.com/1/')])
        else:
            return False
    #异常捕获
    except (AlreadyInGame,NotInGame, RoomFull,NoEnoughPlayer,NotYourTurn, AlreadyHavePiece,RoomNotExist,OutOfBoard) as e:
        return MessageChain.create([Plain(e.msg)])

games = dict()
gamers = dict()
gameboards = dict()

def __ingame(id:int):
    '''检查玩家是否已在对局中；若在，返回所在房间实例；若不在，抛出异常'''
    try: return gamers[id]
    except: raise NotInGame

def __multipal_game_check(id:int):
    '''检查玩家是否已在对局中；若在，抛出异常；若不在，返回True'''
    if id in gamers.keys():raise AlreadyInGame(gamers[id].game_id)
    else: return True

def __find_room(game_id:str):
    '''检查房间是否存在；若存在，返回房间的实例；若不存在，抛出异常'''
    try: return games[game_id]
    except: raise RoomNotExist(game_id)

def __creat_game(mp:gMsgP):
    '''创建新对局'''
    __multipal_game_check(mp.sender.id) #资格审查
    game_id = f'{randint(1,99999):>05d}'
    while(game_id in games.keys()):
        print('房间号重复，正在重新生成')
        game_id = f'{randint(1,99999):>05d}'
    games[game_id]=Game(game_id, mp.sender.id)
    gamers[mp.sender.id]=games[game_id]
    gameboards[game_id]=GameBoard(game_id)
    # return MessageChain.create([Picture.fromLocalFile(gameboards[game_id].path)])
    return MessageChain.create([Plain(f"* 五子棋对局已创立\n- 房间号:{game_id}\n- 快输入'加入{game_id}'来挑战{mp.sender.name}吧！"),Picture.fromLocalFile(gameboards[game_id].path)])

def __join_game(mp:gMsgP,game_id:str):
    '''加入对局'''
    __multipal_game_check(mp.sender.id) #资格审查
    __find_room(game_id).join(mp.sender.id) #加入对局
    gamers[mp.sender.id]=__find_room(game_id) #挂载玩家信息
    return MessageChain.create([Plain(f"* {mp.sender.name}加入了房间{game_id}，大战一触即发！")])
    
def __exit_game(mp:gMsgP):
    '''退出对局'''
    __ingame(mp.sender.id).exit(mp.sender.id) #退出对局
    gamers.pop(mp.sender.id) #取消挂载
    return MessageChain.create([Plain(f"* {mp.sender.name}退出了房间{game_id}，泥给路打呦！")])

def __go(mp:gMsgP, cmd:str):
    '''下子'''
    temp = re.match('^[\(（]([\+\-]?[0-7])[\,，]([\+\-]?[0-7])[\)）]$',cmd)
    x = int(temp.group(1))
    y = int(temp.group(2))
    return __ingame(mp.sender.id).go(mp.sender.id,x,y)

def __check(mp:gMsgP, game_id):
    '''查看棋盘'''
    if game_id in games.keys():
        return MessageChain.create([Picture.fromLocalFile(gameboards[game_id].path)])
    else: raise RoomNotExist(game_id)


class Game:

    pieces = []
    game_id = None
    black_id = None
    white_id = None
    turn = 1

    def __init__(self, game_id:str, black_id:int):
        self.game_id = game_id
        self.black_id = black_id
        self.pieces = []
        for i in range(15):
            self.pieces.append(deepcopy([0]*15))

    def join(self, id:int):
        '''加入对局；若对局已满，抛出异常；否则返回新加入玩家执子颜色'''
        if self.black_id and self.white_id:raise RoomFull(self.game_id) #检查人数
        if self.white_id:
            self.black_id=id
            return '黑色'
        else:
            self.white_id=id
            return '白色'

    def exit(self, id:int):
        '''退出对局'''
        if self.black_id==id:
            self.black_id=None
            gamers.pop(self.black_id)
        else: 
            self.white_id=None
            gamers.pop(self.white_id)
        if not self.black_id and not self.white_id:
            #没人了，删除对局
            games.pop(self.game_id)

    def go(self, id:int, x:int, y:int):
        '''下子'''
        if not (self.black_id and self.white_id):raise NoEnoughPlayer(self.game_id) #检查人数
        x=7+x
        y=7-y
        if id==self.black_id:piece=1
        else :piece=-1
        if self.turn!=piece:raise NotYourTurn
        elif self.pieces[y][x]!=0:raise AlreadyHavePiece(x-7, 7-y)
        else:
            self.pieces[y][x]=piece
            self.turn = self.turn*-1
            gameboards[self.game_id].add(piece,x,y)
            # print(self)
            # mc = MessageChain.create([Plain(str(self))])
            mc = MessageChain.create([Picture.fromLocalFile(gameboards[self.game_id].path)])
            if self.win_chack(piece,x,y):
                print('Game Over')
                mc = MessageChain.create([Plain('* 游戏结束！'),Picture.fromLocalFile(gameboards[self.game_id].path)])
                gamers.pop(self.black_id)
                gamers.pop(self.white_id)
                games.pop(self.game_id)
            return mc

    def win_chack(self, piece, x, y):
        '''检查是否有玩家获胜'''
        def left(i:int):return -i-1
        def right(i:int):return i+1
        def none(i:int):return 0

        def check_side(fx=int, fy=int):
            count = 0
            for i in range(5):
                try:
                    if self.pieces[y+fy(i)][x+fx(i)]==piece:count+=1
                    elif self.pieces[y+fy(i)][x+fx(i)]==0:
                        count+=0.5
                        break
                    else:break
                except IndexError:
                    print('Reach boundary.')
                    break
            return count

        #横
        heng = 1+check_side(none, left)+check_side(none, right)
        if heng>=5:return True
        #竖
        shu = 1+check_side(left, none)+check_side(right, none)
        if shu>=5:return True
        #撇
        pie = 1+check_side(left, left)+check_side(right, right)
        if pie>=5:return True
        #捺
        na = 1+check_side(left, right)+check_side(right, left)
        if na>=5:return True

        return False

    def __str__(self):
        temp = f"{'':>2s}"+' |'
        for i in range(15):
            temp+=f"{i-7:>2d} "
        temp+='\n'
        temp=temp+'---|'+'-'*45+'\n'
        row_no = 7
        for row in self.pieces:
            temp+=f"{row_no:>2d} |"
            for dot in row:
                temp+=f"{dot:>2d} "
            temp+='\n'
            row_no-=1
        return temp

    def print(self):
        print('')
        print(f"{'':>2s}",end=' |')
        for i in range(15):
            print(f"{i-7:>2d}",end=' ')
        print('')
        print('---|'+'-'*45)
        row_no = 7
        for row in self.pieces:
            print(f"{row_no:>2d}",end=' |')
            for dot in row:
                print(f"{dot:>2d}",end=' ')
            print('')
            row_no-=1
        print('')
        


class GameBoard:
    game_id:int
    path:str

    def __init__(self, game_id):
        self.game_id = game_id
        self.path = f'./data/gomoku/{self.game_id}.jpg'
        image = Image.open('./data/gomoku/bg2.jpg')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('./data/gomoku/pf-light.ttf',38)
        draw.text((600,2),f'[{self.game_id}]',font=font,fill=(35,35,35))
        image.save(self.path)

    def add(self,ptype,x,y):
        fill = (255,255,255)
        if ptype==1:fill = (0,0,0)
        # if ptype==1:piece=Image.open('./data/gomoku/black.png')
        # elif ptype==-1:piece=Image.open('./data/gomoku/white.png')
        board = Image.open(self.path)
        draw = ImageDraw.Draw(board)
        x = 50*x + 34
        y = 50*y + 34
        draw.ellipse((x, y, x+30, y+30), fill=fill)
        # board.paste(piece,(x*20,y*20))
        board.save(self.path)

    def delet(self):
        os.remove(self.path)
        
        
        




# image = Image.new('RGB', (width, height), (255, 255, 255))
# # 创建Font对象:
# font = ImageFont.truetype('Arial.ttf', 36)
# # 创建Draw对象:
# draw = ImageDraw.Draw(image)
# # 填充每个像素:
# for x in range(width):
#     for y in range(height):
#         draw.point((x, y), fill=rndColor())
# # 输出文字:
# for t in range(4):
#     draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())


#         .save(self.path) #储存图片

#     def add(self,)


