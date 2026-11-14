from ddgs import DDGS
from ollama import chat
import sonutils

MODEL_NAME = 'gemma3:270m'

def run(querystr):
    querystr = " ".join(querystr)

    ddg_response = DDGS().text(
        query = querystr,
        region = "ru-ru",
        max_results = 5,
        page = 1
    )

    text=""
    for i in ddg_response:
        text += "\n" + i['body']

    llm_response = chat(
        model = MODEL_NAME,
        messages = [
        {
            'role': 'system',
            'content': "Ты — помощник, который отвечает на вопросы, основываясь на следующих данных: "+text
        },
        {
            'role': 'user', 
            'content': querystr
        }]
    )
    answer = llm_response['message']['content'].replace("Ответ:","")
    sonutils.logger.debug(answer)
    sonutils.tts(answer)