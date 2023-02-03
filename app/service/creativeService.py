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

class ContentResponse(BaseModel):
    contentID: int
    videoContent: str
    postContent: str


class CreativeService:
 
    def GetCreative(r, creativeID):
        creativeDB = crud.GetCreative(creativeID)

        #获取创意内容
        resp=CreativeResponse
        resp.creativeID = creativeID
        resp.videoID = creativeDB.VideoID

        #根据videoID获取原始视频路径
        videoDB= crud.GetVideo(creativeDB.VideoID)
        resp.videoName = videoDB.VideoName

        #根据picID获取原始图片路径
        picDB= crud.GetPicture(creativeDB.PicID)
        resp.picName = picDB.PicName

        p = VideoService
        #生成task
        taskID = p.GetNewTaskUUID(p)
        crud.CreateTask(taskID,creativeID)
        #调用videoService进行制作，并返回下载地址
        threading.Thread(target=p.MakeNewVideoByPicVideoPath, args=(p,resp,r)).start()
       
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
            
        return contentDB
