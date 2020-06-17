from roll import rd, ra, rc

#模块指令列表
cmdList = {
    '^\.rh?\d*d\d*.*$':rd,
    '^\.ra([\+\-][1-3])? [^\d ]*[ ]?\d+([\+\-]\d+)?$':ra,
    '^\.rc.*$':rc
}