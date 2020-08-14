from extract import ruling, balance, redeem, changeName

#模块指令列表
cmdList = {
    '^一键乳泠$':ruling,
    '^\.balance$':balance,
    '^查看余额$':balance,
    '^\.redeem [0-9a-zA-Z]+$':redeem,
    '^\兑换[0-9a-zA-Z]+$':redeem,
    '^\改名 .+$':changeName
}