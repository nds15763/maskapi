from service.videoService import VideoService
from fastapi import FastAPI, File, UploadFile,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from starlette.responses import FileResponse
from log.custom_logging import CustomizeLogger
from service.creativeService import CreativeService,CreativeRequest
from pathlib import Path
import uvicorn
from fastapi_utils.tasks import repeat_every
import cron.cron as Cron
import logging
import response

logger = logging.getLogger(__name__)
config_path=Path(__file__).with_name("log_config.json")

def create_app() -> FastAPI:
    app = FastAPI()
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


app = create_app()

@app.get("/")
def read_root(request: Request):
    request.app.logger.info("Hello USOAPI!")
    return {"Hello": "USOAPI"}

#批量上传素材
@app.post("/video/upload/")
async def CreateUploadFileHandler(r:Request,files: List[UploadFile] = File(...),product_id:int = 0):
    p = VideoService
    re = p.CheckUploadRequest(p,files,product_id,r)
    if re != 200:
        return response.Response(re)
    
    VideoService.SetFiles(p,files)
    re = VideoService.safeUploadFile(p,files,product_id,r)
    if re != 200:
        return response.Response(re)
    
    return {"code":200,"status":"success"}

#根据创意ID获取合成视频视频
@app.get("/product/list/")
async def GetProductListHandler(r: Request,product_id:int):
    r.app.logger.info("GetProductListHandler Request")
    p = VideoService
    productInfo = p.GetProductList(p,r,product_id)
    return productInfo


#根据创意ID获取合成视频视频
@app.get("/product/create/")
async def CreateProductHandler(r: Request,product_id:int,product_name:str):
    r.app.logger.info("CreateProductHandler Request")
    taskId = CreativeService.CreateProduct(r,product_id,product_name)
    return  {"taskID": taskId}

#上传口播视频，返回提供下载的连接
@app.post("/video/multivideo/")
async def MakeMultiVideoByOne(r:Request,product_id:int,count:int,speach_lenght:int = 15):
    p = VideoService
    code,re = p.multivideo(p,product_id,count,speach_lenght,r)
    if code != 200:
        return response.Response(re)
    
    return re

#根据创意ID获取合成视频视频
@app.get("/zip/download/token={token}")
async def ZipDownload(r: Request,token:str):
    #r.app.logger.info("VideoDownload Request videoID:%s,token:%s"%videoID,token)
    p = VideoService
    VideoService.SetConf(p)
    code,path = VideoService.DownloadVideoZip(p,token,r)
    if code != 200 :
        return {"code":code}
    else:
        return FileResponse(
            path,
            filename=token+".zip",
            status_code=code
        )


#根据创意ID获取合成视频视频
@app.get("/tk/getcreate/id={created_id}")
async def GetCreateHandler(r: Request,created_id :int):
    r.app.logger.info("GetCreateHandler Request")
    taskId = CreativeService.GetCreative(r,created_id)
    return  {"taskID": taskId}

#根据创意ID获取合成视频视频
@app.get("/tk/getcontent/id={created_id}")
async def GetContentHandler(r: Request,created_id :int):
    r.app.logger.info("GetContentHandler Request")
    content = CreativeService.GetCreativeContent(r,created_id)
    return {"content_id":content.contentID,
    "video_content":content.videoContent,
    "post_content":content.postContent,
    "product_list":content.productList}

#根据创意ID获取合成视频视频
@app.get("/tk/get_task_status/id={task_id}")
async def GetTaskStatus(r: Request,task_id :str):
    r.app.logger.info("GetTaskStatus Request:%s"%task_id)
    status = CreativeService.GetTaskStatus(r,task_id)
    return {"status":status}

#根据创意ID获取合成视频视频
@app.get("/tk/download/t={taskID}")
async def TkDownload(r: Request,taskID :str):
    r.app.logger.info("TkDownload Request taskID:%s"%taskID)
    p = VideoService
    VideoService.SetConf(p)
    code,path = VideoService.DownloadPath(p,taskID,r)
    if code != 200 :
        return {"code":code}
    else:
        return FileResponse(
            path,
            filename=path,
            status_code=code
        )

@app.post("/tk/greenscreen/")
async def CreateUploadFilesHandler(r: Request,mute:int,files: List[UploadFile] = File(...)):
    p = VideoService
    VideoService.SetFiles(p,files)
    r.app.logger.info("create_upload_files request")
    reFileName = VideoService.CreatUploadTask(p,r,mute)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )


@app.post("/tk/gst/")
async def CreateUploadFilesHandler(r: Request, videoText:str,files: List[UploadFile] = File(...)):
    p = VideoService
    VideoService.SetFiles(p,files)
    r.app.logger.info("create_upload_files request")
    reFileName = VideoService.MakeVideoWithText(p,r,videoText)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )

@app.on_event("startup")
@repeat_every(seconds=60*60,wait_first=True)
def Cronjob():
    print("CronJob StartUp")
    Cron.CronJob.CronDeleteUploadedFile()
    print("CronJob Finished")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)