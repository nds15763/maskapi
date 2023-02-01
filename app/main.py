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
    VideoService.SetFiles(files)
    fDownload = VideoService.safeUploadFile(p,files,r)
    return FileResponse(
        fDownload,
        filename=fDownload,
    )

#根据创意ID获取合成视频视频
@app.get("/tk/getcreate/id={created_id}")
async def GetCreateHandler(r: Request,created_id :int):
    r.app.logger.info("GetCreateHandler Request")
    resp = CreativeService.GetCreative(r,created_id)
    return JSONResponse(content={"video_src":resp.videoDownloadSrc})

#根据创意ID获取合成视频视频
@app.post("/tk/download/")
async def TkDownload(r: Request,req :str):
    r.app.logger.info("TkDownload Request")
    p = VideoService
    VideoService.SetConf(p)
    path = VideoService.DownloadPath(p,req)
    return FileResponse(
        path,
        filename=req,
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

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)