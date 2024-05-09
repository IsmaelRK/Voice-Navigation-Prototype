# Voice Navigation Prototype


Disclaimer: This is a prototype and has some bugs. Improved AI modeling is necessary for any production use. 
The prototype is designed to be flexible and adaptable to various scenarios. In its current state, it serves as a simple 
example, which can be found in `alura-ai-project/src/speech_recognition/speech_form_examples.py`.

## About

This project is a speech recognition prototype focused on assisting people with disabilities. Through speech, it can 
recognize the user's intended action and other characteristics. These details are defined previously, and it's important to 
note that the AI needs further refinement for specific applications.

The prototype includes simple examples where users can choose options like buying, selling, or logging in. Known bugs 
include the AI response format (requiring JSON) and the interpretation of user needs, which can be improved. 
Currently, it's a basic prototype with limited examples provided to the AI. These can be enhanced, including providing a
customized history in the `set_gemini_api_settings()` function within `speech_recognition.py`.


The code is primarily in Python, utilizing FastAPI to render a simple HTML page with an integrated JavaScript audio 
recorder. This built-in recorder allows for API testing without relying on external services.

In essence, it's an API that receives audio, sends it to another API for processing, and expects a JSON response. 
The goal is to recognize the user's desired navigation and resources (like what to buy and for how much) 
within the application based on the interpretation of the
audio by the AI.

<br>

## How to Run

Starting from the project root `alura-ai-project/`:


###Install Required Libraries: `pip install -r required.txt`.
* It's recommended to use a Python virtual environment: `python -m venv venv` (remember to activate it).


### Create Your .env File

* In the project root, create a file named `.env` with the key API_KEY. Insert your API key and keep this file secure.


### Run the API
* Open a terminal in the project root and execute uvicorn audio_receiver:app --reload. The application should start on port 8000.
* The integrated audio recorder should be accessible at http://localhost:8000/. Ensure microphone usage is allowed.
* The API expects an .mp3 audio file at the route http://localhost:8000/upload once the recording ends.

<br>

## Project Structure
* At project Root `alura-ai-project/` there is `audio_receiver.py`.
  * Contains API configurations like CORS and declared routes (/ and /upload for GET and POST requests, respectively).
  * Route-associated functions are in the same file due to their simplicity and small number. Consider reorganizing for larger, more complex projects.
  * Note that uploaded audio files are saved in `alura-ai-project/src/audios` and deleted from both local and Gemini file systems after processing.


* At project Root `alura-ai-project/` there is `static/`:
  * `index.html`: Contains embedded JavaScript for the audio recorder. No modularization was implemented due to the single-file nature.
  * `style.css`: Provides basic styling for `index.html`. Styling is minimal as it's not the primary focus of the application.


* At project Root `alura-ai-project/` there is `src/speech_recognition/`:
  * `speech_recognition.py`:
    * `send_to_gemini()`: Receives the path and name of the .mp3 file, along with a list of response examples. Sends the file to Gemini and returns the JSON response. This is the main function.
    * `treat_response()`: Receives a string and returns it formatted for JSON conversion.
    * `treated_response_to_json()`: Receives a treated string from the previous function and returns it in JSON format.
    * `set_gemini_api_settings()`: Contains Google Gemini API settings and chat history, which can be populated as needed. Returns variables required for the main function.
  * `speech_form_examples.py`:
    * `get_examples()`: Returns a list with examples for the Gemini API.