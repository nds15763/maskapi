from videoService import picToVideo
from fastapi import FastAPI, File, UploadFile,HTTPException,Request
from typing import List
from starlette.responses import FileResponse
from custom_logging import CustomizeLogger
from pathlib import Path
import uvicorn
import logging

logger = logging.getLogger(__name__)
config_path=Path(__file__).with_name("log_config.json")

def create_app() -> FastAPI:
    app = FastAPI(title='CustomLogger', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


app = create_app()

@app.get("/")
def read_root(request: Request):
    request.app.logger.info("Hello MaskAPI!")
    return {"Hello": "World"}

@app.post("/tk/greenscreen/")
async def create_upload_files(request: Request,files: List[UploadFile] = File(...)):
    p = picToVideo(files)
    request.app.logger.info("create_upload_files request")
    reFileName = picToVideo.creatUploadTask(p,logger)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)