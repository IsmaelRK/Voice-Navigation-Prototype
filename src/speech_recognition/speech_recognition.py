import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


def send_to_gemini(mp3_file_path, mp3_file_name, speech_form_results_examples) -> json:
    model, chat = set_gemini_api_settings()

    prompt = "Transcreva o audio"
    file_to_upload = genai.upload_file(path=mp3_file_path, display_name=mp3_file_name)
    gemini_transcription_response = model.generate_content([prompt, file_to_upload])

    prompt = (f"De acordo com o texto {gemini_transcription_response}, transforme para json, sem levar em consideração "
              f"a moeda, apenas valores, mantenha as falas do usuario na linguagem do texto, não adicione campos que "
              f"não estão citados nos exemplos, alguns exemplos: {speech_form_results_examples}")

    response = chat.send_message(prompt)
    print(response)
    treated_response = treat_response(response.text)
    print(treated_response)
    gemini_response_to_json = treated_response_to_json(treated_response)
    print(gemini_response_to_json)

    # Debugs
    print("\n Gemini Transcription: \n", gemini_transcription_response.text)
    print("\n Gemini JSON Format Response: \n", response.text)
    print("\n Treated input: \n", treated_response)
    print("\n JSON: \n", gemini_response_to_json)

    genai.delete_file(name=file_to_upload.name)
    return gemini_response_to_json


def treat_response(text_response) -> str:
    _, treated_response = text_response.split("{", 1)
    treated_response, _ = treated_response.split("}", 1)
    treated_response = "{" + treated_response + "}"
    treated_response = treated_response.replace("'", '"')
    treated_response = treated_response.strip()
    treated_response = treated_response.replace("None", "null")

    return treated_response


def treated_response_to_json(treated_response) -> json:

    json_data = json.loads(treated_response)
    gemini_response_to_json = json.dumps(json_data, indent=4)

    return gemini_response_to_json


def set_gemini_api_settings():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)

    generation_config = {
        "candidate_count": 1,
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

    chat = model.start_chat(history=[])

    return model, chat
