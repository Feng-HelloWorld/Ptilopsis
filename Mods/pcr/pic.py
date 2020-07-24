from PIL import Image, ImageDraw, ImageFont
import os

import random
import sys
sys.path.append('./Mods/pcr')


def initPic(img_path):
    image = Image.open(img_path)
    img_draw = ImageDraw.Draw(image)
    return image,img_draw

async def savePic(image,fileName):
    file_path = '../CQP/data/image/'+fileName
    image.save(file_path+'.png')
    try:
        os.remove(file_path+'.jpg')
    except:pass
    os.rename(file_path+'.png',file_path+'.jpg')

async def thankPic(name, id, total_damage):

    pic = random.randint(1,5)
    #pic =5
    if pic==1:
        image, img_draw = initPic('./Mods/pcr/thank.png')
        left_side = 580
    elif pic==2:
        image, img_draw = initPic('./Mods/pcr/thank2.png')
        left_side = 80
    elif pic==3:
        image, img_draw = initPic('./Mods/pcr/thank3.png')
        left_side = 540
    elif pic==4:
        image, img_draw = initPic('./Mods/pcr/thank4.png')
        left_side = 80
    elif pic==5:
        image, img_draw = initPic('./Mods/pcr/thank5.png')
        left_side = 80

    ttf_name = ImageFont.truetype('./Mods/pcr/bold.ttf',80)
    ttf_id = ImageFont.truetype('./Mods/pcr/bold.ttf',40)
    ttf = ImageFont.truetype('./Mods/pcr/bold.ttf',70)
    ttf_small = ImageFont.truetype('./Mods/pcr/bold.ttf',40)
    ttf_damage = ImageFont.truetype('./Mods/pcr/bold.ttf',140)
    ttf_japan = ImageFont.truetype('./Mods/pcr/japan.ttf',140)
    
    top_side = 80

    img_draw.text( (left_side,top_side+20), name, font=ttf_name, fill=(0,0,0) )
    img_draw.text( (left_side,top_side+112), "[{}]".format(id), font=ttf_id, fill=(60,60,60) )
    img_draw.text( (left_side,top_side+150), "今日出刀已完成", font=ttf, fill=(0,0,0) )
    img_draw.text( (left_side,top_side+240), "总计输出", font=ttf_small, fill=(120,120,120) )
    img_draw.text( (left_side,top_side+260), "{:,}".format(total_damage), font=ttf_damage, fill=(0,0,0) )
    img_draw.text( (left_side-60,top_side+430), "おつかれさま", font=ttf_japan, fill=(230,230,230) )
    await savePic(image,'thankPic')

async def checkAttendencePic(name_list:tuple):
    file_name='./Mods/pcr/checkAttendence_small.png'
    if len(name_list)>15:file_name='./Mods/pcr/checkAttendence_big.png'
    image, img_draw = initPic(file_name)
    ttf = ImageFont.truetype('./Mods/pcr/normal.ttf',28)
    ttf_backup = ImageFont.truetype('./Mods/pcr/pf-light.ttf',24)
    left_side = 620
    top_side = 140    
    line_space = 33
    new_col = 500
    count = 0
    left_sum = 0
    for record in name_list:
        if count==15:
            left_side+=new_col
            count=0
        top = top_side+count*line_space
        img_draw.text( (left_side, top), '[{}]'.format(record[0]), font=ttf, fill=(0,0,0) )
        img_draw.text((left_side+50, top), '{}'.format(record[1][:12]), font=ttf, fill=(100,100,100) )
        count+=1  
        left_sum += record[0]
    img_draw.text( (1065, 50), '[{}]人'.format(len(name_list)), font=ttf, fill=(255,162,162) )
    img_draw.text( (1065, 80), '[{}]刀'.format(left_sum), font=ttf, fill=(255,162,162) )
    await savePic(image,'checkAttendencePic')




    
    