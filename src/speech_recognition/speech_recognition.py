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
    prompt = "Transcreva o audio:"
    your_file = genai.upload_file(path=mp3_file)


    response = model.generate_content([prompt, your_file])
    print(response.text)

    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
