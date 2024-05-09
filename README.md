# Protótipo de navegação por voz

[Change to English](./README_ENG.md)

![Static Badge](https://img.shields.io/badge/Gemini-blue)
![Static Badge](https://img.shields.io/badge/Python-orange)
![Static Badge](https://img.shields.io/badge/FastApi-green)
![Static Badge](https://img.shields.io/badge/JSON-yellow)


<br>

Ressalto que este é um protótipo e possui alguns bugs, sendo necessária uma melhor modelagem da IA para qualquer uso em 
produção, deixo claro que o protótipo foi feito para ser flexível, podendo ser adaptado para diversos cenário, no caso 
atual, esta servindo com alguns exemplos simples, que podem ser conferidos em `alura-ai-project/src/speech_recognition/speech_form_examples.py`.

## Sobre

É um protótipo de reconhecimento de fala que foca em ajudar pessoas com deficiência, onde se pode, atravéz da fala, 
reconhecer a ação que o usuário quer tomar, e outras características diversas, tudo deve ser definido posteriormente e 
ressalto que a IA deve ser melhor moldada para a determinada aplicação.

Se encontra com alguns exemplos simples, onde se pode escolher opções dentre, comprar, vender e logar.
Dentre os bugs conhecidos, posso citar principalmente o retorno da IA, que é necessário ser um json, a interpretação das
necessidades do usuário pode ser melhorada também. No estado atual é um protótipo simples com poucos exemplos dados a IA,
que podem ser melhorados, inclusive fornecendo um histórico customizado á mesma em `speech_recognition.py`, na função 
`set_gemini_api_settings()`.

Se trata majoritariamente de um código em python, utilizando FastAPI, que renderiza uma página html simples com um gravador
de áudio em js integrado á mesma, possui um gravador de audio built-in para que se necessário possa ser feito o teste da API
sem haver necessidade outro serviço terceirizado.

Em outras palavras é uma API que recebe um áudio, envia para uma API que deve retornar um json, tendo o objetivo de
reconhecer para onde e como o usuário quer navegar na aplicação, tendo estas informações no json retornado pela interpretação
do áudio pela IA

<br>

## Como executar

A partir da raiz do projeto, dentro de `alura-ai-project/`.


### Instale as libs necessárias: `pip install -r required.txt`.
* Sugiro que use uma venv para o python `python -m venv venv`, lembre de ativa-lá.

### Crie seu .env
* Na raiz do projeto, crie um arquivo `.env` com a chave `API_KEY`, e insira sua chave de api, lembre de não compartilhar este arquivo.

### Execute a API
* Em um terminal na raiz do projeto execute `uvicorn audio_receiver:app --reload`, a aplicação deve iniciar na porta 8000.
* O gravador de áudio integrado deve estar disponível em `http://localhost:8000/`. Lembre de permitir o uso do microfone.
* A API deve receber um áudio .mp3 na rota `http://localhost:8000/upload` assim que a gravação for encerrada.

<br>

## Estrutura do projeto

* Na raiz do projeto, dentro de `alura-ai-project/`, possuimos o arquivo principal `audio_receiver.py`.
  * Este arquivo possui configurações da API, como CORS e as rotas declaradas, `/ e /upload`, respectivamente GET e POST.
  * As funções associadas as rotas estão no mesmo arquivo visto que como são poucas e de baixa complexidade, não há necessidade de separar as mesmas. Sugiro que dependendo das demandas do projeto, tamanho e complexidade organize de outra forma.
  * Ressalto que os áudios enviados e posteriormente salvos em `alura-ai-project/src/audios`, após seu processamento são deletados do sistema de arquivos, tanto local, quanto do Gemini.


* Na raiz do projeto, possuímos o diretório `static/`, que contém `index.html` e `style.css`
  * O `index.html` possui js inserido diretamente, não houve modularização, pois seriam arquivos únicos, não havendo necessidade de tal organização no momento.
  * O `style.css` possui a estilização de `index.html`, sendo uma estilização extremamente simples, pois não é o objetivo principal da aplicação, a não ser para algum eventual teste.
  

* Na raiz do projeto, possuímos o diretório `src/speech_recognition/`, que contém `speech_recognition.py` e `speech_form_examples.py`
  * `speech_recognition.py` possui algumas funções: <br>
    * `send_to_gemini()`, recebe o caminho e nome do `.mp3` além de uma lista de exemplos de resposta, envia o arquivo para Gemini e retorna o json. Se trata função principal.
    * `treat_response()`, recebe uma string, e retorna a mesma pronta para ser convertida para json.
    * `treated_response_to_json()`, recebe uma string tratada pela função anteriormente citada e retorna no formato json.
    * `def set_gemini_api_settings()`, Contém configuração da API do Google Gemini, e o history do chat, que se necessário pode ser populado de acordo com suas necessidades, retorna algumas variáveis necessárias a função principal.
  * `speech_form_examples.py` possui a função `get_examples()`, que retorna uma lista com alguns exemplos enviados a Gemini.