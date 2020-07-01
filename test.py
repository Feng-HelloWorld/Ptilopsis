import sys
sys.path.append('./Mods/pcr')
import asyncio
from pic import thankPic

async def aaa():
    await thankPic("Peach",123456789,555666777)

if __name__ == "__main__":
    thankPic("Peach",123456789,5666777)

