# Import everything needed to edit video clips
from moviepy.editor import *
import cv2
from fastapi import FastAPI, File, UploadFile,Request
import uuid
import numpy as np
from typing import List
from conf.conf import Conf
import response
import db.crud as crud

class VideoService:
    taskUUID = "" #本次任务UUID
    taskFiles = List[UploadFile]
    uploadPic = "" #上传图片名称
    uploadImgPath = "" #上传图片路径
    uploadVideo = "" #上传视频名称
    uploadVideoPath = "" #上传视频路径
    uploadTimeStr = "" #上传时间戳
    outputVideoPath = "" #生成视频路径
    outputVideo = "" #生成视频名称
    cvTmpImg = "" #opencv处理图片名称
    TempPicPath = ""
    TempVideoPath = ""

    def __init__(self):
        self.SetConf(self)
        self.uploadPic = ""
        self.uploadVideo = ""

    def SetUUID(self):
        self.taskUUID = uuid.uuid4().hex

    def SetFiles(self,files):
        self.SetUUID(self)
        self.taskFiles = files

    def SetConf(self):
        conf = Conf()
        self.uploadImgPath = conf.uploadImgPath
        self.uploadVideoPath = conf.uploadVideoPath
        self.outputVideoPath = conf.outputVideoPath
        self.TempPicPath = conf.tempImgPath
        self.TempVideoPath = conf.tempVideoPath

    def DownloadPath(self,task_id,r):
        task = crud.GetTask(task_id)
        r.app.logger.info("DownloadPath request task_id:%s" % task_id)
        if task == None:
            r.app.logger.error("DownloadPath task = %s not found" % task_id)
            return 604,"程序内部错误，请联系管理员"
        if task.Status != 1:
            r.app.logger.info("DownloadPath task = %s not completed" % task_id)
            return 605,"视频还未完成"
        return 200,self.outputVideoPath+task.OutVideoSrc

    def GetNewTaskUUID(self):
        self.SetUUID(self)
        return self.taskUUID

    #根据照片路径和视频路径制作抠图视频
    def MakeNewVideoByPicVideoPath(self,taskID,creative,r):
        self.SetConf(self)
        r.app.logger.info("MakeNewVideoByPicVideoPath request creative:%s" % creative.__dict__)
        #赋值结构体
        self.uploadPic = creative.picName
        self.uploadVideo = creative.videoName

        #图片扣色，或者扣好了传上去也行
        self.greenScrean(self,self.TempPicPath,creative.picName)
        #打开视频
        video = self.openVideo(self,self.TempVideoPath+creative.videoName, r)
        #去掉视频声音
        video = self.muteVideo(self,video,r)
        filename = self.taskUUID+".mp4"
        #制作遮罩层
        self.picToImgMask(self,video,filename,r)
        r.app.logger.info("MakeNewVideoByPicVideoPath 视频生成完成,更新记录 taskID:%s" % (taskID))
        #更新进度
        crud.UpdateTask(1,taskID,filename)
        r.app.logger.info("MakeNewVideoByPicVideoPath 更新完成 taskID:%s" % (taskID))

        return

    def CreatUploadTask(self,request):
        request.app.logger.info("creatUploadTask request self:%s" % self.__dict__)
        self.SetConf(self)
        #保存文件
        for file in self.taskFiles:
            #保存图片文件
            if (self.detect_picture(self,file.filename,request)):
                re,code = self.saveFile(self,self.uploadImgPath,file,"pic",request)
                if not re:
                    request.app.logger.error("creatUploadTask saveImgFile code:%d"%code)
                    return response.Response(code)
            #保存视频文件
            elif (self.detect_video(self,file.filename,request)):
                re,code = self.saveFile(self,self.uploadVideoPath,file,"video",request)
                if not re:
                    request.app.logger.error("creatUploadTask saveVideoFile code:%d"%code)
                    return response.Response(code)
                else:
                    continue
            else:
                request.app.logger.error("creatUploadTask UnknowFileType code:%d"%602)
                return response.Response("602")

        #图片扣色，或者扣好了传上去也行
        self.greenScrean(self,self.uploadImgPath, self.uploadPic)
        #打开视频
        video = self.openVideo(self,self.uploadVideoPath+self.uploadVideo,request)
        #去掉视频声音
        video = self.muteVideo(self,video,request)
        outFileName = self.uploadVideo
        #制作遮罩层
        self.picToImgMask(self,video,outFileName,request)
        return self.outputVideoPath+self.outputVideo

    def saveFile(self,path,file,ftype,request):
        request.app.logger.info("saveFile path:%s,file:%s,ftype:%s"%(path,file,ftype))
        #不存在该路径，报错
        if not os.path.exists(path):
            request.app.logger.error("不存在该路径 path:%s" % path)
            return False,603
        #判断文件类型，保存
        save_file = ""
        if ftype == "pic":
            self.uploadPic = self.taskUUID +'.'+ file.filename.split(sep='.')[-1]
        if ftype == "video":
            self.uploadVideo = self.taskUUID +'.'+ file.filename.split(sep='.')[-1]

        save_file = os.path.join(path, self.taskUUID +'.'+ file.filename.split(sep='.')[-1])
        # else:
        #     return False,601
        #保存文件
        f = open(save_file, 'wb')
        data = file.file.read()
        f.write(data)
        f.close()
        request.app.logger.info("saveFile success filename:%s"%save_file)
        return True,200

    def picToImgMask(self,video,filename,request):
        request.app.logger.info("picToImgMask request")
        picBg = self.uploadImgPath+self.cvTmpImg
        self.outputVideo = filename
        try:
            mask = (ImageClip(picBg)
                        .set_duration(video.duration) 
                        .resize(video.size))
            request.app.logger.info("picToImgMask set mask picBg:%s,outputfile:%s"%(picBg,self.outputVideo))    
            CompositeVideoClip([video, mask]).write_videofile(self.outputVideoPath+self.outputVideo)
            request.app.logger.info("picToImgMask success outputfile:%s"%self.outputVideo)
        except Exception as e:
            request.app.logger.info("picToImgMask error:%s,"%e)
        request.app.logger.info("picToImgMask success outputfile:%s"%self.outputVideo)
        return self.outputVideo

    def openVideo(self,vPath,request):
        request.app.logger.info("openVideo vPath:%s"%vPath)
        clip = VideoFileClip(vPath)
        return clip

    def muteVideo(self,video,request):
        request.app.logger.info("muteVideo")
        muteClip = video.without_audio()
        return muteClip

    def greenScrean(self,imgPath,picName):
        # todo 读取并转换图片格式
        opencv = cv2.imread(imgPath + picName)
        hsv = cv2.cvtColor(opencv, cv2.COLOR_RGB2HSV)

        # todo 指定绿色范围,60表示绿色，我取的范围是-+10
        minGreen = np.array([40, 80, 80])
        maxGreen = np.array([80, 255, 255])

        # todo 确定绿色范围
        mask = cv2.inRange(hsv, minGreen, maxGreen)

        # todo 确定非绿色范围
        mask_not = cv2.bitwise_not(mask)

        # todo 通过掩码控制的按位与运算锁定绿色区域
        green = cv2.bitwise_and(opencv, opencv, mask=mask)

        # todo 通过掩码控制的按位与运算锁定非绿色区域
        green_not = cv2.bitwise_and(opencv, opencv, mask=mask_not)

        # todo 拆分为3通道
        b, g, r = cv2.split(green_not)

        # todo 合成四通道
        bgra = cv2.merge([b, g, r, mask_not])

        self.cvTmpImg = "cvtmp_"+self.taskUUID+".png"
        # todo 保存带有透明通道的png图片,有了这种素材之后，就可以给这张图片替换任意背景了
        cv2.imwrite(self.uploadImgPath + self.cvTmpImg, bgra)
    
    def detect_picture(self,file,request):
        request.app.logger.info("detect_picture filename:%s"%file)
        return file.casefold().endswith(".png" ) or file.casefold().endswith(".jpg") or file.casefold().endswith(".webp") or file.casefold().endswith(".jpeg")

        
    def detect_video(self,file,request):
        request.app.logger.info("detect_video filename:%s"%file)
        return file.casefold().endswith(".mp4" )

    def safeUploadFile(self,files,request):
        file = files[0]
        re,code = self.saveFile(self.uploadVideoPath,file,"video",request)
        if not re:
            request.app.logger.error("creatUploadTask saveImgFile code:%d"%code)
            return response.Response(code)
        return self.uploadVideoPath+self.uploadVideo