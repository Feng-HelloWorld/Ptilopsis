#coding=utf-8
# 同步图片检测服务接口, 会实时返回检测的结果

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import ImageSyncScanRequest
import json
import uuid
import datetime

clt = client.AcsClient("LTAI4GGmMsHi3bVDUURLUR5S", "7aDPrULxMoopSBiDEvHxBsy6iVmf2V",'cn-shanghai')
region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
request = ImageSyncScanRequest.ImageSyncScanRequest()
request.set_accept_format('JSON')

def imgCheck(url:str):
    # 同步现支持单张图片，即一个task
    task = {"dataId": str(uuid.uuid1()),
            "url":url,
            "time":datetime.datetime.now().microsecond
            }
    request.set_content(bytearray(json.dumps({"tasks": [task], "scenes": ["porn"]}), "utf-8"))
    response = clt.do_action(request)
    print("===Response=======\n",response)
    result = json.loads(response)
    if 200 == result["code"]:
        taskResults = result["data"]
        for taskResult in taskResults:
            if (200 == taskResult["code"]):
                sceneResults = taskResult["results"]
                for sceneResult in sceneResults:
                    rate = sceneResult["rate"]
                    suggestion = sceneResult["suggestion"]
                    print("=====\n* 图片检测结果：", rate,suggestion,"\n=====")
                    if suggestion=="block" or (suggestion=="review" and rate>80):
                        return True
    return False 
                    

