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
from db.database import DB

class CreativeRequest(BaseModel):
    creativeID: int

class CreativeResponse(BaseModel):
    creativeID: int
    videoID:int
    videoName:str
    picID:int
    picName:str
    videoDownloadSrc:str

class CreativeService:
    def __init__(self) -> None:
        pass
 
    def GetCreative(r, creativeID):
        creative = DB.GetCreative(creativeID)

        #获取创意内容
        resp=CreativeResponse
        resp.creativeID = creativeID
        resp.videoID = creative.videoID

        #根据videoID获取原始视频路径
        video = DB.GetVideo(creative.videoID)
        resp.videoName = video.videoName

        resp.picName = 'tmp_pixle3_1.jpg'

        #调用videoService进行制作，并返回下载地址
        p = VideoService
        outsrc = p.MakeNewVideoByPicVideoPath(p,resp,r)
        resp.videoDownloadSrc = outsrc
        return resp
