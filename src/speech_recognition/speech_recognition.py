import os
from dotenv import load_dotenv

from pathlib import Path
import hashlib
import google.generativeai as genai


def send_to_gemini(mp3_file):

    load_dotenv()
    api_key = os.getenv("API_KEY")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    uploaded_files = []

    def upload_if_needed(pathname: str) -> list[str]:
        path = Path(pathname)
        hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            existing_file = genai.get_file(name=hash_id)
            return [existing_file.uri]
        except:
            pass
        uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
        return [uploaded_files[-1].uri]

    audio_uri = upload_if_needed("./src/speech_recognition/audio0.mp3"),

    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": audio_uri,
        },
        {
            "role": "user",
            "parts": ["Pode transcrever o que foi falado neste audio?"]
        },
        {
            "role": "model",
            "parts": [
                "Sim, posso transcrever o que foi falado no áudio. Você disse: \"Pode transcrever o que estou falando?\"."]
        },

        {
            "role": "user",
            "parts": audio_uri
        },

    ])

    convo.send_message("faça o mesmo para o ultimo audio enviado")
    print(convo.last.text)
    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
