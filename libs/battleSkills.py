from funcs.dice import dice





def B01(ori, tar):
    '''友情破颜拳'''
    if ori.action()<1:
        return "[!] 你的行动点不足，无法发动攻击"
    ori.action(-1)
    damage = dice(['1d6'])[0]
    result = f'[Att] {ori.name}挥舞着拳头打出了一套王八拳法，对{tar.name}造成了[{damage}]点伤害！'
    hp = tar.hp(-1*damage)
    if hp<=0:
        result+=f'\n- {tar.name}被击败了！'
        tar.hp(-1*hp)
    else:
        result +=f'\n- {tar.name}还剩{hp}点血量'
    return result


def C01(ori, tar):
    '''治愈术'''
    if ori.action()<1:
        return "[!] 你的行动点不足，无法进行治疗"
    ori.action(-1)
    cur = dice(['1d6'])[0]
    tar.hp(cur)
    result = f'[Cur] {ori.name}发动了初级治愈术，回复了{tar.name}共计[{cur}]点血量！\n- {tar.name}现在有{tar.hp()}点血量'
    
    return result


def D01(ori, tar):
    '''火球术'''
    if ori.action()<2:
        return "[!] 你的行动点不足，无法发动攻击"
    ori.action(-2)
    damage = dice(['2d6','3'])[0]
    result = f'[Mag] {ori.name}念出咒语，召唤出火球狠狠的打在{tar.name}的屁股上，造成了[{damage}]点伤害！'
    hp = tar.hp(-1*damage)
    if hp<=0:
        result+=f'\n- {tar.name}被击败了！'
        tar.hp(-1*hp)
    else:
        result +=f'\n- {tar.name}还剩{hp}点血量'
    return result

def D02(ori, tar):
    if ori.action()<1:
        return "[!] 你的行动点不足，无法发动攻击"
    ori.action(-1)
    damage = dice(['2d6'])[0]
    result = f'[Mag] {ori.name}将双手在胸前合十，从手臂中射出21万摄氏度的斯卑修姆光线，对{tar.name}造成了[{damage}]点伤害！'
    hp = tar.hp(-1*damage)
    if hp<=0:
        result+=f'\n- {tar.name}被击败了！'
        tar.hp(-1*hp)
    else:
        result +=f'\n- {tar.name}还剩{hp}点血量'
    return result



def diy(ori, tar, result):
    if ori.action()<1:
        return "[!] 你的行动点不足，无法发动攻击"
    ori.action(-1)
    damage = dice(['2d6'])[0]
    result = result.replace('oriname',str(ori.name)).replace('tarname',str(tar.name)).replace('damage',str(damage))
    hp = tar.hp(-1*damage)
    if hp<=0:
        result+=f'\n- {tar.name}被击败了！'
        tar.hp(-1*hp)
    else:
        result +=f'\n- {tar.name}还剩{hp}点血量'
    return result

class Attact:
    pass

