# Import everything needed to edit video clips
from moviepy.editor import *
import cv2
from fastapi import FastAPI, File, UploadFile,Request
import uuid
import numpy as np
from service.videoService import VideoService
from typing import List
from conf.conf import Conf
import response
from pydantic import BaseModel
from typing import Union
# from db.database import SessionLocal
import db.crud as crud
import threading

class CreativeRequest(BaseModel):
    creativeID: int

class CreativeResponse(BaseModel):
    creativeID: int
    videoID:int
    videoName:str
    picID:int
    picName:str
    videoDownloadSrc:str

class ContentResponse():
    contentID: int
    videoContent: str
    postContent: str
    productList: list
    def __init__(self,contentID,videoContent,postContent,productList):
        self.contentID = contentID
        self.videoContent = videoContent
        self.postContent = postContent
        self.productList = productList

class CreativeService:
 
    def GetCreative(r, creativeID):
        p = VideoService
        #生成task
        taskID = p.GetNewTaskUUID(p)
        r.app.logger.info("GetCreative creativeID:%d 生成taskID:%s" % (creativeID,taskID))

        creativeDB = crud.GetCreative(creativeID)
        r.app.logger.info("GetCreative 查询对应创意, creativeID:%d 生成taskID:%s" % (creativeID,taskID))
        #获取创意内容
        resp = CreativeResponse
        resp.creativeID = creativeID
        resp.videoID = creativeDB.VideoID

        #根据videoID获取原始视频路径
        videoDB = crud.GetVideo(creativeDB.VideoID)
        resp.videoName = videoDB.VideoName
        r.app.logger.info("GetCreative 查询视频,VideoName:%s creativeID:%d 生成taskID:%s" % (videoDB.VideoName,creativeID,taskID))

        #根据picID获取原始图片路径
        picDB= crud.GetPicture(creativeDB.PicID)
        resp.picName = picDB.PicName
        
        crud.CreateTask(taskID,creativeID)
        r.app.logger.info("GetCreative 录入任务,VideoName:%s creativeID:%d 生成taskID:%s" % (videoDB.VideoName,creativeID,taskID))

        #调用videoService进行制作，并返回下载地址
        threading.Thread(target=p.MakeNewVideoByPicVideoPath, args=(p,taskID,resp,r)).start()
       
        return taskID

    def GetCreativeContent(r, creativeID):
        creativeDB = crud.GetCreative(creativeID)
        if creativeDB.CreativeID == 0:
            r.app.logger.info("GetCreativeContent request 没有找到创意 creativeID:%d" % creativeID)
            return
        #根据CreativeJD获取视频文案
        contentDB = crud.GetContent(creativeDB.ContentID)
        if contentDB.ContentID == 0:
            r.app.logger.info("GetCreativeContent request 没有找到文案 creativeID:%d,contentID:%d" % (creativeID,creativeDB.ContentID))
            return
        
        productDB = crud.GetProductList(creativeDB.ProductID)
        re = ContentResponse(creativeDB.ContentID,contentDB.VideoContent,
        contentDB.PostContent,productDB)
        return re

    def GetTaskStatus(r, taskID):
        taskDB = crud.GetTask(taskID)
        if taskDB.CreativeID == 0:
            r.app.logger.info("GetTaskStatus request 数据错误 taskID:%s" % taskID)
            return False
        if taskDB.Status == 1:
            #如果是1就代表更新完成
            return True
        return False