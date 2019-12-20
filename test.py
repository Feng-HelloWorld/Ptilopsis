import coc.card
import time
import os

from PIL import Image, ImageDraw, ImageFont

cmd=['2d10','-3d6','23','-d5','-2d','-3']
#print(coc.card.dice(cmd))

'''
success=list()
for i in range(0,50):
    data=list()
    Sum=int()
    fail_times=0
    stander=5
    stander=int(stander)
    times=5
    times=int(times)
    for i in range(0,times):
        data=data+coc.card.dice()
        Sum=Sum+data[-1]
        if data[-1]>stander:
            fail_times+=1
        time.sleep(0.005)
    #print('success rate:', (times-fail_times)/times*100,'%')
    success.append((times-fail_times)/times*100)
    #print('average:' , Sum/times)
    #print(data)
    #print(sum(data),Sum)
print("="*20)
print(success)
print("-"*20)
print("Finall success:",sum(success)/50,"%")
'''


a=coc.card.investigator()
for i in range(1):
    #print(a)
    pass
    

#print(31//5)

#print(coc.card.build_and_DB(524))

#cardList=os.listdir('./coc/cards/')
#print(cardList)

s=''
print(s.isdigit())

a=print('sdf')
print(a)







img_path = "6.png"
ttf_path = "pf-bz.ttf"


# 1. 加载图像文件
image = Image.open(img_path)
# 2. 加载字体并指定字体大小
#ttf = ImageFont.load_default()  # 默认字体

# 3. 创建绘图对象
img_draw = ImageDraw.Draw(image)
# 4. 在图片上写字
# 第一个参数：指定文字区域的左上角在图片上的位置(x,y)
# 第二个参数：文字内容
# 第三个参数：字体
# 第四个参数：颜色RGB值


chars = "德克萨斯"
chars_x, chars_y = 350, 100
ttf = ImageFont.truetype(ttf_path, 70)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "16岁"
chars_x, chars_y = 350, 210
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

left1=120
space=290

line1=390

chars = "STR: 50"
chars_x, chars_y = left1, line1
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "CON: 45"
chars_x, chars_y = left1+space, line1
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "SIZ: 50"
chars_x, chars_y = left1+space*2, line1
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))


space2=55

chars = "DEX: 40"
chars_x, chars_y = left1, line1+space2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "APP: 45"
chars_x, chars_y = left1+space, line1+space2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "INT: 70"
chars_x, chars_y = left1+space*2, line1+space2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

#line3
chars = "POW: 60"
chars_x, chars_y = left1, line1+space2*2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "EDU: 80"
chars_x, chars_y = left1+space, line1+space2*2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "LUCK: 70"
chars_x, chars_y = left1+space*2, line1+space2*2
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))


#line4
chars = "BUILD: 1"
chars_x, chars_y = left1, line1+space2*3
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "DB: 1d4"
chars_x, chars_y = left1+space, line1+space2*3
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "MOV: 8"
chars_x, chars_y = left1+space*2, line1+space2*3
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

line5=720
#line5
chars = "HP: 10/11"
chars_x, chars_y = left1, line5
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "SAN: 62/65"
chars_x, chars_y = left1+space, line5
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "MP: 0/5"
chars_x, chars_y = left1+space*2, line5
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

#技能区


chars = "ksu    克总发糖(克苏鲁神话)    0"
chars_x, chars_y = left1, 890
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1+500, line5+170
ttf = ImageFont.truetype(ttf_path, 30)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, 940
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, 1340
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+220
ttf = ImageFont.truetype(ttf_path, 30)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+270
ttf = ImageFont.truetype(ttf_path, 30)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+620
ttf = ImageFont.truetype(ttf_path, 30)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+670
ttf = ImageFont.truetype(ttf_path, 25)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+720
ttf = ImageFont.truetype(ttf_path, 25)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "ksu:克总发糖(克苏鲁神话):0"
chars_x, chars_y = left1, line5+770
ttf = ImageFont.truetype(ttf_path, 25)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))


chars = "do   王八拳(斗殴)     70     1d3+db"
chars_x, chars_y = left1, line5+730
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "do   王八拳(斗殴)     70     1d3+db"
chars_x, chars_y = left1, line5+780
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "do   王八拳(斗殴)     70     1d3+db"
chars_x, chars_y = left1, line5+830
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "do   王八拳(斗殴)     70     1d3+db"
chars_x, chars_y = left1, line5+880
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))
chars = "*"
chars_x, chars_y = left1+100, line5+930
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(255,0,0))
chars = "80"
chars_x, chars_y = left1+450, line5+930
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(0,0,0))

chars = "40"
chars_x, chars_y = left1+500, line5+930
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(80,80,80))
chars = "16"
chars_x, chars_y = left1+550, line5+930
ttf = ImageFont.truetype(ttf_path, 35)
img_draw.text((chars_x, chars_y), chars, font=ttf, fill=(160,160,160))

# image.show()
image.save("1234.png")
