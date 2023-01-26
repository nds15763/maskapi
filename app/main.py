from videoService import picToVideo
from fastapi import FastAPI, File, UploadFile
from typing import List
from starlette.responses import FileResponse

import uvicorn


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/tk/greenscreen/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    p = picToVideo(files)
    reFileName = picToVideo.creatUploadTask(p)
    return FileResponse(
            reFileName,
            filename=reFileName,
        )

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)