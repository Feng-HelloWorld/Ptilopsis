from jrrp import jrrp
from daily import majang, qikongshi

#模块指令列表
cmdList = {
    '^.jrrp$':jrrp,
    '^.*有无雀魂.*$':majang,
    '^.*雀魂.缺.+$':majang
    '^.*granbluefantasy\.jp.*$':qikongshi
}