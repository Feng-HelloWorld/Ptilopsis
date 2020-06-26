from os import path
import nonebot
import config

if __name__ == '__main__':
    nonebot.init(config)

    nonebot.load_plugin('deliver')
    nonebot.run()