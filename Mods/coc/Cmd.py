from roll import rd, ra, rc

#模块指令列表
cmdList = {
    '^\.rh?\d*d\d*.*$':rd,
    '^\.ra[ ]?\d+$':ra,
    '^\.rc.*$':rc
}