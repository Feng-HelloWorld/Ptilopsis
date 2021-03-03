from mods.gomoku import GameBoard

x=-7
y=7

x=7+x
y=7-y
print(x,y)
a = GameBoard(11123)
for i in range(15):
    for m in range(15):
        a.add(1,x+i,y+m)

