import requests
import re
from reply import Reply

def biliSearch(name: str, reply:Reply):
    url = "https://search.bilibili.com/all?keyword="+name
    try:
        page=requests.Session().get(url) 
        title = re.search("a title.*href",page.text).group()[9:-6]
        #print(title)
        link = re.search("www.bilibili.com/video/BV[0-9A-Za-z]*",page.text).group()
        #print(link)
        up = re.search("up-name[^<]*<",page.text).group()[9:-1]
        #print(up)
        reply.add_group_msg("{}\nUP:{}\n{}".format(title,up,link) )
    except:
        reply.add_group_msg("ERRO: 404咕")

def bvSearch(bv:str, reply:Reply):
    if re.match("^BV[0-9a-zA-Z]+$",bv):
        biliSearch(bv, reply)

