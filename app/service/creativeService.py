# Import everything needed to edit video clips
from moviepy.editor import *
import cv2
from fastapi import FastAPI, File, UploadFile,Request
import uuid
import numpy as np
from typing import List
from conf.conf import Conf
import response
from pydantic import BaseModel
from typing import Union
from db.database import DB

class CreativeRequest(BaseModel):
    productID: int
    creativeID: int


class CreativeService:
    def __init__(self) -> None:
        pass
 
    def GetCreative(self,r, req):
        #creativeID 创意ID
        #根据创意ID去DB查找，找到对应的视频,并生成抠图视频，后期还要返回创意文案
        creative = DB.GetCreative()
        return
