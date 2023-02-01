from service.videoService import VideoService
from fastapi import FastAPI, File, UploadFile,HTTPException,Request
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
    p = VideoService(files)
    fDownload = VideoService.safeUploadFile(p,files,r)
    return FileResponse(
        fDownload,
    )

#根据创意ID获取合成视频视频
@app.post("/tk/getcreate/")
async def GetCreateHandler(r: Request,req :CreativeRequest):
    r.app.logger.info("GetCreateHandler Request")
    reFileName = CreativeService.GetCreative(r,req)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )

@app.post("/tk/greenscreen/")
async def CreateUploadFilesHandler(r: Request,files: List[UploadFile] = File(...)):
    p = VideoService(files)
    r.app.logger.info("create_upload_files request")
    reFileName = VideoService.CreatUploadTask(p,r)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)