import sonutils
from ollama import chat

def run(query):
	query = " ".join(query)
	response = chat(
		model='gemma3:1b',
		messages = [
		{
			'role': 'system',
        	'content': 'Ты краткий помощник. Отвечай строго не более чем в двух предложениях.'
		},
		{
			'role': 'user', 
			'content': query
		}]
	)
	sonutils.logger.debug(response['message']['content'])
	sonutils.tts(response['message']['content'])
	#print(response['message']['content'])
