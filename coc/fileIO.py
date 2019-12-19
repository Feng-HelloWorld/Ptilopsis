
import coc.card

def read_card_from_file(fileName,cardDict):
    '''
    将文件中的人物卡加载到内存中 \n
    fileName: 即用户的QQ号加上.txt，cardDict的索引 \n
    cardDict: 人物卡字典
    '''
    Card=cardDict[fileName]
    fp=open('./coc/cards/'+fileName,'r',encoding='utf-8')
    for line in fp:
        temp=line.strip().split(':')
        if len(temp)==2:
            index=temp[0]
            value=temp[1]
            if (index in ['NAME','DB']) and value!='':
                pass
            elif (index in ['HP','SAN','MP']) and value!='':
                value=value.strip().split('/')
                try:
                    value=[int(value[0]),int(value[1])]
                except:
                    continue
            elif value!='' and value.isdigit():
                value=int(value)
            else:
                continue
            Card.add_stats(index,value)
        elif len(temp)==3:
            cmd=temp[0]
            name=temp[1]
            value=temp[2]
            if cmd!='' and value.isdigit():
                Card.add_skill(cmd,name,int(value))
        elif len(temp)==4:
            cmd=temp[0]
            name=temp[1]
            value=temp[2]
            damage=temp[3]
            if cmd!='' and value.isdigit():
                Card.add_weapon(cmd,name,int(value),damage)
    fp.close()
    Card.build_and_DB()
    Card.mov()





def write_card_to_file(fileName,cardDict):
    '''
    将内存中的人物卡写入文件中 \n
    fileName: 即用户的QQ号加上.txt，cardDict的索引 \n
    cardDict: 人物卡字典
    '''
    Card=cardDict[fileName]
    Stats=Card.stats
    Skills=Card.skills
    Weapon=Card.weapon
    fp=open('./coc/cards/'+fileName,'w',encoding='utf-8')
       
    fp.write('==Stats属性'+'='*20+'\n')
    order=['NAME','AGE','STR','CON','SIZ','DEX','APP','INT','POW','EDU','LUCK','BUILD','DB','MOV']
    for item in order:
        fp.write(item+':{}\n'.format(Stats[item]))
    order=['HP','SAN','MP']
    for item in order:
        fp.write(item+':'+'{}/{}\n'.format(Stats[item][0],Stats[item][1]))

    fp.write('==Skills技能'+'='*20+'\n')
    for key, value in Skills.items():
        fp.write(key+':{}:{}\n'.format(value[0],value[1]))

    fp.write('==Weapon武器'+'='*20+'\n')
    for key, value in Weapon.items():
        fp.write(key+':{}:{}:{}\n'.format(value[0],value[1],value[2]))

    fp.close()