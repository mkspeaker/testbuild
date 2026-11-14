import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sonutils
import importlib



with open('settings.json', 'r', encoding='utf-8') as config:
	settings = json.load(config)
	INTENT_CATEGORIES = settings['INTENT_CATEGORIES']
	WORD_MATCH_MULTIPLIER = settings['WORD_MATCH_MULTIPLIER']
	FUZZ_MATCH_MULTIPLIER = settings['FUZZ_MATCH_MULTIPLIER']
	PRIVILIGED_KEY_POSITION = settings['PRIVILIGED_KEY_POSITION']
	MAX_KEY_POSITION = settings['MAX_KEY_POSITION']
	MIN_APPROVAL_PERCENT = settings['MIN_APPROVAL_PERCENT']

with open('intent_config.json', 'r', encoding='utf-8') as config:
	INTENT_CONFIG = json.load(config)



# функция удаляет ключевые слова и/или ключевые фразы из запроса, оставляя только контекст
def leave_context(input_list, keys):
	if (type(keys) == str):
		keys = keys.split()
	try:
		pos = input_list.index(keys[-1])
		del input_list[:pos+1]
		return input_list
	except: 
		return input_list

def intent_recognition(query):
	# переменные
	query_categories=["miscellaneous"]
	functions=[]
	functions_percents=[]
	querystr=query
	query=query.split()
	category_keys=[]
	query_keys=[]

	# определение категории

	for category, values in INTENT_CATEGORIES.items():
		for word in query:
			found_key = process.extractOne(word, values)
			if (found_key[1]>92 and 
				query.index(word)<MAX_KEY_POSITION): 
				query_categories.append(category)
				if (word not in category_keys):
					category_keys.append(word)

	# определение функций

	for function_name, category in INTENT_CONFIG.items():
		for query_category in query_categories:
			if (query_category in category['intentcategory'] and 
				function_name not in functions): 
				functions.append(function_name)
	if (len(functions)==0): 
		functions = [x for x in INTENT_CONFIG]

	# попытка определения по ключевой фразе

	for function_name, category in INTENT_CONFIG.items():
		if (function_name in functions and
			'keyphrases' in category):
			for phrase in category['keyphrases']:
				if (phrase in querystr): 
					sonutils.logger.info(phrase)
					return [function_name, 
							leave_context(query, 
										query[:phrase.count(" ")+1])]

	# попытка определения совпадания по ключевым словам и фразам
	for i in range(len(functions)): query_keys.append([])

	function_number=0
	for function_name, category in INTENT_CONFIG.items():
		if (function_name in functions):
			# поиск ключей в запросе
			matches=0
			for i in range(len(query)):
				word = query[i]
				if (len(word) > 2):
					found_key = process.extractOne(word, 
												category['keys'])
					if (found_key[1] > category['percent'][0]):
						if (len(query_keys) < PRIVILIGED_KEY_POSITION):
							matches+=2
						else: matches+=1
						query_keys[function_number].append(word)

					if ('auxiliary_keys' in category):
						found_auxiliary_key = process.extractOne(word, 
																category['auxiliary_keys'])
						if (found_auxiliary_key[1] > category['percent'][0]):
							matches+=1
					
			# сравнение строки-ключа с запросом
			if 'keyphrases' in category:
				fuzzmatch=0
				for phrase in category['keyphrases']:
					fuzzquery = " ".join(query[:MAX_KEY_POSITION])
					string_matching = fuzz.ratio(fuzzquery, phrase)/100
					if (string_matching > fuzzmatch): 
						fuzzmatch = string_matching
				functions_percents.append(
					(matches/len(query) * WORD_MATCH_MULTIPLIER
					+ fuzzmatch * FUZZ_MATCH_MULTIPLIER)/2
				)
			function_number+=1

	max_percents = max(functions_percents)
	function_number = functions_percents.index(max_percents)
	function_name = functions[function_number]
	sonutils.logger.debug(querystr)
	if (len(functions)!=0 and max_percents > MIN_APPROVAL_PERCENT):
		sonutils.logger.info([category_keys + query_keys[function_number], 
														functions, 
														functions_percents])
		return [function_name, 
				leave_context(query, category_keys
							+ query_keys[function_number])]
	return ["llm", 
			query]

while True:
	userquery = input("запрос: ")
	intent_recognition_output = intent_recognition(userquery)
	sonutils.logger.debug(intent_recognition_output)
	plugin = importlib.import_module("plugins."+intent_recognition_output[0])
	#try:
	plugin.run(intent_recognition_output[1])
	#except:
	#	sonutils.logger.error("плагин не загрузился")