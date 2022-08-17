from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from app.Wav2Vec2Inference import Wav2VecInference
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="File extension is not .wav")
    wav2vec = Wav2VecInference()
    final_dict = wav2vec.inference(file.filename)
    return final_dict

