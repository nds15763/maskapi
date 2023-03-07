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
    request.app.logger.info("Hello MaskAPI!")
    return {"Hello": "World"}

@app.post("/uploadvideo/")
async def CreateUploadFileHandler(r:Request,files: List[UploadFile] = File(...)):
    p = VideoService    
    VideoService.SetFiles(p,files)
    fDownload = VideoService.safeUploadFile(p,files,r)
    return FileResponse(
        fDownload,
        filename=fDownload,
    )

@app.get("/get_file/name={fname}")
async def get_file(r: Request,fname :str):
    re = "../upload/video/"+fname
    return FileResponse(re,filename=re)

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

#批量返回今日执行脚本内容
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
async def CreateUploadFilesHandler(r: Request,files: List[UploadFile] = File(...)):
    p = VideoService
    VideoService.SetFiles(p,files)
    r.app.logger.info("create_upload_files request")
    reFileName = VideoService.CreatUploadTask(p,r)
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