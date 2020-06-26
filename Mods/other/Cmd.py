from jrrp import jrrp
from daily import majang, qikongshi, ruling

#模块指令列表
cmdList = {
    '^.jrrp$':jrrp,
    '^.*有无雀魂.*$':majang,
    '^.*雀魂.缺.+$':majang,
    '一键乳泠':ruling,
    '^.*granbluefantasy\.jp.*$':qikongshi
}