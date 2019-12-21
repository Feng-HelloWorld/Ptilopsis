from PIL import Image, ImageDraw, ImageFont
import os

ttf_path='pf-bz.ttf'
img_path='blank.png'

def init():
    image = Image.open(img_path)
    img_draw = ImageDraw.Draw(image)
    return image,img_draw

def add_name_and_age(img_draw,name,age):
    ttf = ImageFont.truetype(ttf_path, 70)
    img_draw.text((350, 100), str(name), font=ttf, fill=(0,0,0))
    ttf = ImageFont.truetype(ttf_path, 35)
    img_draw.text((350, 210), str(age)+'岁', font=ttf, fill=(0,0,0))

def add_stats(img_draw,dataList):
    left_edge=120
    top_edge=390
    ttf = ImageFont.truetype(ttf_path, 35)
    num=0
    for i in range(5):
        top=top_edge+55*i
        if i==4:
            top=720
        for m in range(3):
            left=left_edge+290*m
            img_draw.text((left, top), dataList[num], font=ttf, fill=(0,0,0))
            num+=1

def add_skills(img_draw,dataList):
    left=120
    top_edge=890
    ttf = ImageFont.truetype(ttf_path, 35)
    num=0
    for m in range(10):
        top=top_edge+50*m
        try:
            img_draw.text((120, top), dataList[num][0], font=ttf, fill=(0,0,0))
            img_draw.text((220, top), dataList[num][1], font=ttf, fill=(0,0,0))
            img_draw.text((750, top), str(dataList[num][2]), font=ttf, fill=(0,0,0))
            img_draw.text((820, top), str(dataList[num][2]//2), font=ttf, fill=(80,80,80))
            img_draw.text((890, top), str(dataList[num][2]//5), font=ttf, fill=(160,160,160))
        except:
            pass
        num+=1

def add_weapons(img_draw,dataList):
    left=120
    top_edge=1500
    ttf = ImageFont.truetype(ttf_path, 35)
    num=0
    for m in range(4):
        top=top_edge+50*m
        try:
            img_draw.text((120, top), dataList[num][0], font=ttf, fill=(0,0,0))
            img_draw.text((220, top), dataList[num][1], font=ttf, fill=(0,0,0))
            img_draw.text((500, top), str(dataList[num][2]), font=ttf, fill=(0,0,0))
            img_draw.text((560, top), str(dataList[num][2]//2), font=ttf, fill=(80,80,80))
            img_draw.text((620, top), str(dataList[num][2]//5), font=ttf, fill=(160,160,160))
            img_draw.text((700, top), str(dataList[num][3]), font=ttf, fill=(0,0,0))
        except:
            pass
        num+=1

def save(image,fileName):
    image.save(fileName)
    os.rename('card_out.png','card_out.jpg')
    