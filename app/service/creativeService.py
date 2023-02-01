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

class CreativeRequest(BaseModel):
    productID: int
    creativeID: int


class CreativeService:
    def __init__(self) -> None:
        pass
 
    def GetCreative(self, req: CreativeRequest):
        #productID 产品ID
        #creativeID 创意ID
        req.creativeID
        return
