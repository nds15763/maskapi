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
import threading
import traceback
import random
import zipfile

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
        self.SetConf(self)
        self.taskFiles = files

    def SetConf(self):
        #conf = Conf()
        # self.uploadImgPath = conf.uploadImgPath
        # self.uploadVideoPath = conf.uploadVideoPath
        # self.outputVideoPath = conf.outputVideoPath
        # self.TempPicPath = conf.tempImgPath
        # self.TempVideoPath = conf.tempVideoPath
        self.uploadImgPath = "../upload/img/"
        self.uploadVideoPath = "../upload/video/"
        self.outputVideoPath = "../out_video/"
        self.TempPicPath = "../template/img/"
        self.TempVideoPath ="../template/video/"

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
    
    def DownloadVideoCut(self,video_id,token,r):
        videos = crud.GetVideoList(video_id)
        r.app.logger.info("DownloadVideoCut request video_id:%s,token:%s" %(video_id,token))
  
        #更新token状态
        # crud.UpdateToken(token)
        
        #拉取所有videos里面的地址video_fullpath
        file_names = []
        for v in videos:
            file_names.append(v.VideoFullPath)
        #把所有这些视频压缩成一个zip包,保存到out_videos里面
        zip_file_name = token+".zip"
        outpath = os.path.abspath(os.path.join(os.getcwd(), "../maskapi/out_video/"))
        output_zip = outpath+zip_file_name 
        r.app.logger.info("DownloadVideoCut request video_id:%s,token:%s,outpath:%s" %(video_id,token,output_zip))
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for file in file_names:
                zipf.write(file, os.path.basename(file))          
        
        # crud.CreateVideoLog(2,token+".zip")
        #返回zip包地址
        return 200,output_zip

    def GetNewTaskUUID(self):
        self.SetUUID(self)
        return self.taskUUID

    #根据照片路径和视频路径制作抠图视频
    def MakeNewVideoByPicVideoPath(self,taskID,creative,r):
        self.SetConf(self)
        print("MakeNewVideoByPicVideoPath request")
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
        #异步制作视频
        threading.Thread(target=self.makeVideo, args=(self,video,filename,r,taskID)).start()
        #制作遮罩层
        # self.picToImgMask(self,video,filename,r)
        # r.app.logger.info("MakeNewVideoByPicVideoPath 视频生成完成,更新记录 taskID:%s" % (taskID))
        # #更新进度
        # crud.UpdateTask(1,taskID,filename)
        # r.app.logger.info("MakeNewVideoByPicVideoPath 更新完成 taskID:%s" % (taskID))
        return

    def makeVideo(self,video,filename,r,taskID):
        try:
            #制作遮罩层
            self.picToImgMask(self,video,filename,r)
            r.app.logger.info("MakeNewVideoByPicVideoPath 视频生成完成,更新记录 taskID:%s" % (taskID))
            #更新进度
            crud.UpdateTask(1,taskID,filename)
            r.app.logger.info("MakeNewVideoByPicVideoPath 更新完成 taskID:%s" % (taskID))
        except Exception as e:
            traceback.print_exc()

    def CreatUploadTask(self,request,mute):
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
        
        if mute != 1:
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

    #监测上传视频参数合理性
    def CheckUploadRequest(self,files,product_id,request):
        if product_id <=0:
            code = 501
            request.app.logger.error("CheckUploadRequest 参数错误 code:%d, product_id:%d,files:%d"%code,product_id,len(files))
            return code
        
        if len(files) <=0:
            code = 502
            request.app.logger.error("CheckUploadRequest 参数错误 code:%d, product_id:%d,files:%d"%code,product_id,len(files))
            return code
        
        for file in files:
            if not (self.detect_video(self,file.filename,request)):
                code = 502
                request.app.logger.error("CheckUploadRequest detect_video 参数错误 code:%d, product_id:%d,files:%d"%code,product_id,len(files))
                return code
        return 200
    
    
    #生成新的文件名
    def getNewFileName(self):
        return uuid.uuid4().hex+".mp4"

    def get_duration_from_cv2(self,filename):
        cap = cv2.VideoCapture(filename)
        if cap.isOpened():
            rate = cap.get(5)
            frame_num =cap.get(7)
            duration = frame_num/rate
            return duration
        return -1

    def getProductPath(self,product_id):
        re = crud.GetProduct(product_id)
        return re.ProductDir
    
    #根据生成的数量，返回选择的视频，还有视频的下载地址
    def multivideo(self,product_id,count,speach_lenght,request):
        #request.app.logger.info("multivideo request product_id:%d,count:%d,speach_lenght:%d"%product_id,count,speach_lenght)
        
        GroupA,GroupB,GroupC,video_lengths = self.makeABCData(self,product_id,count,speach_lenght,request)

        sort_video_list = []
        for x in range(count):
            randomlist = self.randomVideo(self,GroupA,GroupB,GroupC,video_lengths,speach_lenght,request)
            sort_video_list.append(randomlist)

        video_dict = {}
        for v_list in sort_video_list:
            for y in v_list:
                video_dict[y] = 1

        #然后根据选择出来的视频去查询对应的视频地址
        video_download_dict = self.getVideoPath(self,video_dict,product_id,request)

        #通过product_id 产品视频
        return 200,{
            "video_sort_list":sort_video_list,
            "video_download_dict":video_download_dict
        }
    
    def getVideoPath(self,video_dict,product_id,request):
        video_src_list = []
        for id in video_dict:
            video_src_list.append(str(id))
        dou = ','
        videoIDStr = dou.join(video_src_list)
        video_list = crud.GetVideoList(videoIDStr)
        product_dir = self.getProductPath(self,product_id)
        video_download_dict = {}
        for video in video_list:
            video_download_dict[video.ID] = product_dir+"\\"+video.VideoName

        return video_download_dict
    
    def randomVideo(self,A,B,C,video_lengths,speach_lenght,request):
        selected_videos = []
        #这里video_groups是代表的2.5,5,7.5三个视频组
        #现在这三个组是需要查询出来的
        video_groups = [A, B, C]
        
        while sum(video_lengths[v] for v in selected_videos) < speach_lenght:
            group = random.choice(video_groups)
            video = random.choice(group)
            
            if video not in selected_videos:
                selected_videos.append(video)

        return selected_videos

    def makeABCData(self,product_id,count,speach_lenght,request):
        A = self.getVideoGroup(self,"A",product_id,request)#查询出A组合适的所有ID
        B = self.getVideoGroup(self,"B",product_id,request)#查询出A组合适的所有ID
        C = self.getVideoGroup(self,"C",product_id,request)

        #查询出组合适的所有ID
        video_lengths = {}
        for ID in A:
            video_lengths[ID] = 7.5
        for ID in B:
            video_lengths[ID] = 5
        for ID in C:
            video_lengths[ID] = 2.5

        return A,B,C,video_lengths

    def getVideoGroup(self,group_id,prouct_id,request):
        #A组是7.5秒的视频
        #B组是5秒的视频
        #C组是2.5的视频
        if group_id == "A":
            return crud.GetVideoIDList(prouct_id,7.5)
        elif group_id == "B":
            return crud.GetVideoIDList(prouct_id,5)
        elif group_id == "C":
            return crud.GetVideoIDList(prouct_id,2.5)
        else:
            return []

    #存储上传文件
    def safeUploadFile(self,files,product_id,request):
        #先获取产品id对应的路径
        product_path = self.getProductPath(self,product_id)
        if product_path == "":
            request.app.logger.error("safeUploadFile getProductPath product_id:%d"%product_id)
            return 605
        
        for file in files:
            file.filename = self.getNewFileName(self)
            #生成文件名
            re,code = self.saveFileOrigin(self,product_path,file,"video",request)
            if not re:
                request.app.logger.error("safeUploadFile saveFileOrigin code:%d"%code)
                return code
            
            #获取视频时长
            duration = self.get_duration_from_cv2(self,product_path+"\\"+file.filename)
            if duration > 0:
                #存储数据库
                crud.CreateVideo(file.filename,product_path+"\\"+file.filename,duration,product_id,"")
            else:
                request.app.logger.error("safeUploadFile get_duration_from_cv2 code:%d"%606)
                return 606

        return 200
    

    def saveFileOrigin(self,path,file,ftype,request):
        request.app.logger.info("saveFile path:%s,file:%s,ftype:%s"%(path,file,ftype))
        #不存在该路径，报错
        if not os.path.exists(path):
            request.app.logger.error("不存在该路径 path:%s" % path)
            return False,603
        #判断文件类型，保存
        save_file = file.filename
        self.uploadVideo = file.filename

        save_file = os.path.join(path, save_file)
        # else:
        #     return False,601
        #保存文件
        f = open(save_file, 'wb')
        data = file.file.read()
        f.write(data)
        f.close()
        request.app.logger.info("saveFile success filename:%s"%save_file)
        return True,200

    def setVideoText(self,video,txt):
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (50, 50)
        # fontScale
        fontScale = 1
        # Blue color in BGR
        color = (0, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        # Using cv2.putText() method
        video = cv2.putText(video, txt, org, font, 
                        fontScale, color, thickness, cv2.LINE_AA)
        return video

    def MakeVideoWithText(self,request,txt):
        request.app.logger.info("MakeVideoWithText request self:%s" % self.__dict__)
        self.SetConf(self)
        #保存文件
        for file in self.taskFiles:
            #保存图片文件
            if (self.detect_picture(self,file.filename,request)):
                re,code = self.saveFile(self,self.uploadImgPath,file,"pic",request)
                if not re:
                    request.app.logger.error("MakeVideoWithText saveImgFile code:%d"%code)
                    return response.Response(code)
            #保存视频文件
            elif (self.detect_video(self,file.filename,request)):
                re,code = self.saveFile(self,self.uploadVideoPath,file,"video",request)
                if not re:
                    request.app.logger.error("MakeVideoWithText saveVideoFile code:%d"%code)
                    return response.Response(code)
                else:
                    continue
            else:
                request.app.logger.error("MakeVideoWithText UnknowFileType code:%d"%602)
                return response.Response("602")

        #图片扣色，或者扣好了传上去也行
        self.greenScrean(self,self.uploadImgPath, self.uploadPic)
        #打开视频
        video = self.openVideo(self,self.uploadVideoPath+self.uploadVideo,request)
        #去掉视频声音
        video = self.muteVideo(self,video,request)
        #设置视频文字
        video = self.setVideoText(self,video,txt)
        outFileName = self.uploadVideo
        #制作遮罩层
        self.picToImgMask(self,video,outFileName,request)


        return self.outputVideoPath+self.outputVideo

    def GetProductList(self,request,product_id):
        return crud.GetProductList()