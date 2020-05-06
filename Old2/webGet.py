import requests
import re


def biliSearch(name: str, msg: tuple):
    url = "https://search.bilibili.com/all?keyword="+name
    try:
        page=requests.Session().get(url) 
        title = re.search("a title.*href",page.text).group()[9:-6]
        #print(title)
        link = re.search("www.bilibili.com/video/BV[0-9A-Za-z]*",page.text).group()
        #print(link)
        up = re.search("up-name[^<]*<",page.text).group()[9:-1]
        #print(up)
        msg[0].append(title)
        msg[0].append("UP:{}".format(up))
        msg[0].append(link)
    except:
        msg[0].append("ERRO: 404咕")

def bvSearch(bv:str, msg:tuple):
    if re.match("^BV[0-9a-zA-Z]+$",bv):
        biliSearch(bv,msg)

