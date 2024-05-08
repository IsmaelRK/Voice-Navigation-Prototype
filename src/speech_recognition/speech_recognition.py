import os
from dotenv import load_dotenv
import google.generativeai as genai


def send_to_gemini(mp3_file_path, mp3_file_name):

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

    prompt = "Transcreva o audio:"
    file_to_upload = genai.upload_file(path=mp3_file_path, display_name=mp3_file_name)

    response = model.generate_content([prompt, file_to_upload])
    print(response.text)

    print(mp3_file_name)
    genai.delete_file(name=file_to_upload.name)
