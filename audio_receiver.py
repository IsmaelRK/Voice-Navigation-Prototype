import os
import uuid
import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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

    file_uuid = str(uuid.uuid4())
    file.filename = file_uuid + ".mp3"
    audio_dir_path = "./src/audios"

    if not os.path.exists(audio_dir_path):
        os.makedirs(audio_dir_path)

    file_path = os.path.join(audio_dir_path, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    speech_form_examples = [

        {

            "intention": "buy",
            "item": "black car toy",
            "minimum_price": None,
            "maximum_price": None,

        },

        {

            "intention": "buy",
            "item": "gamer computer",
            "minimum_price": "5000",
            "maximum_price": "7000",

        },

        {

            "intention": "sell",
            "item": "car",
            "price": "35000",
            "description": "Honda black car with air-conditioner",

        },

        {
          "login": "useremail@email.com",
          "password": "user_password",
        }

    ]

    send_to_gemini(file_path, file_uuid, speech_form_examples)
    os.remove(file_path)
