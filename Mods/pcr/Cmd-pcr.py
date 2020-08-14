from teamFight import jiaru, tuichu, tichu, zhuangtai, baodao, weidao, chadao, guashu, xiashu, chashu, yuyue, quxiaoyuyue, rank, chexiao, mingdan

#模块指令列表
cmdList = {
    '^加入[公工行]会[0-9]{13}$':jiaru,
    '^退出[公工行]会$':tuichu,
    '^踢出[公工行]会[0-9]+$':tichu,
    '^状态$':zhuangtai,
    '^报刀[0-9]+$':baodao,
    '^尾刀$':weidao,
    '^查刀$':chadao,
    '^挂树$':guashu,
    '^上树$':guashu,
    '^下树$':xiashu,
    '^查树$':chashu,    
    '^预约[1-5]$':yuyue, 
    '^取消预约[1-5]$':quxiaoyuyue,
    '^(公会)?排名$':rank,
    '^(公会)?排行$':rank,
    '^撤销(报刀)?$':chexiao,
    '^(成员)?名单$':mingdan
}