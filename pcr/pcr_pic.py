from PIL import Image, ImageDraw, ImageFont
import os


import sys
sys.path.append('./pcr')


def initPic(img_path):
    image = Image.open(img_path)
    img_draw = ImageDraw.Draw(image)
    return image,img_draw

def savePic(image,fileName):
    image.save(fileName)
    try:
        os.remove('../data/image/thank_out.jpg')
    except:pass
    os.rename('../data/image/thank_out.png','../data/image/thank_out.jpg')

def thank(name, id, total_damage):
    image, img_draw = initPic('./pcr/thank.png')
    ttf_name = ImageFont.truetype('./pcr/bold.ttf',80)
    ttf_id = ImageFont.truetype('./pcr/bold.ttf',40)
    ttf = ImageFont.truetype('./pcr/bold.ttf',70)
    ttf_small = ImageFont.truetype('./pcr/bold.ttf',40)
    ttf_damage = ImageFont.truetype('./pcr/bold.ttf',140)
    ttf_japan = ImageFont.truetype('./pcr/japan.ttf',140)

    left_side = 600
    top_side = 80

    img_draw.text( (left_side,top_side+20), name, font=ttf_name, fill=(0,0,0) )
    img_draw.text( (left_side,top_side+112), "[{}]".format(id), font=ttf_id, fill=(0,0,0) )
    img_draw.text( (left_side,top_side+150), "今日三刀已完成", font=ttf, fill=(0,0,0) )
    img_draw.text( (left_side,top_side+240), "总计输出", font=ttf_small, fill=(120,120,120) )
    img_draw.text( (left_side,top_side+260), "{:,}".format(total_damage), font=ttf_damage, fill=(0,0,0) )
    img_draw.text( (left_side-110,top_side+430), "おつかれさま", font=ttf_japan, fill=(230,230,230) )
    savePic(image,'../data/image/thank_out.png')



    
    