from os import path
import nonebot
import config

if __name__ == '__main__':
    nonebot.init(config)
    #nonebot.load_builtin_plugins()

    #nonebot.load_plugins(path.join(path.dirname(__file__), 'COC'),'COC')
    #nonebot.load_plugins(path.join(path.dirname(__file__), 'Daily'),'Daily')

    #进入初始化插件
    #nonebot.load_plugins(path.join(path.dirname(__file__), 'coc'),'coc')
    
    #启用指令解析插件
    nonebot.load_plugin('deliver')
    nonebot.run()