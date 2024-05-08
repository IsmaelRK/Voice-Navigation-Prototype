import sys
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from src.speech_recognition.speech_recognition import send_to_gemini

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload/")
async def save_file(file: UploadFile = File(...)):

    if file.content_type != "audio/mpeg":
        return JSONResponse(status_code=415, content={"message": "File type not supported, use .mp3"})

    file.filename = str(uuid.uuid4()) + ".mp3"

    send_to_gemini(file)

    # with open(file.filename, "wb") as f:
    #     f.write(await file.read())