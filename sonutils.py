import sounddevice as sd
import soundfile as sf
import logging


# логгер
logging.basicConfig(filename="testing.log", filemode="a", level=logging.DEBUG,
		format="%(asctime)s   -   %(levelname)s - %(filename)s - %(funcName)s - %(message)s")
logger=logging.getLogger()


# преобразует текст в звук и сразу проигрывает его
def tts(text):
	from piper import PiperVoice
	import wave

	voice = PiperVoice.load("./opt/ru_RU-irina-medium.onnx")
	with wave.open("./tmp/0.wav", "wb") as wav_file:
	    voice.synthesize_wav(text,wav_file)

	data, samplerate = sf.read("./tmp/0.wav", dtype="float32")
	sd.play(data, samplerate)
	sd.wait()


# проигрывает аудио
def play_wav(path):
	data, samplerate = sf.read(path, dtype="float32")
	sd.play(data, samplerate)
	logger.debug(path)
	sd.wait()


# преобразует голос в аудио. ожидает аудио в течение length секунд
def stt(length=10):
	from vosk import Model, KaldiRecognizer
	import signal, string, queue

	ans=""
	q = queue.Queue()
	model = Model(lang="ru")
	table = str.maketrans('', '', string.punctuation)
	recognizer = KaldiRecognizer(model, 48000)

	def handler(): None
	signal.signal(signal.SIGALRM, handler)
	def callback(indata, frames, time, status):
	    if status:
	        print(status, file=sys.stderr)
	    q.put(bytes(indata))

	with sd.RawInputStream(
	    samplerate=48000,
	    blocksize=8000,
	    device=None,
	    dtype="int16",
	    channels=1,
	    callback=callback,
	    ):
		signal.alarm(length)
		try:
		    while True:
		        data = q.get()
		        if recognizer.AcceptWaveform(data):
		            ans = recognizer.Result()[14:-3].translate(table).lower()
		except: None
	return ans


# находит наиболее подходящее слово из списка wordlist в списке контекстных слов query
def find_one(query, wordlist):
	from fuzzywuzzy import process
	answer = ""
	if (type(query)==list):
		for word in query:
			wordpercent=(len(word)-3)/len(word)*100
			if len(word)>2:
				processextraction = process.extractOne(word, wordlist)
				print(processextraction)
				if processextraction[1]>wordpercent: answer = processextraction[0]
	elif (type(query)==str):
		wordpercent=(len(query)-3)/len(query)*100
		if len(query)>2:
			processextraction = process.extractOne(query, wordlist)
			print(processextraction)
			if processextraction[1]>wordpercent: answer = processextraction[0]
	return answer


# заменяет все числа в формате слов на числа
def list2nums(query):
	from ru_word2number import w2n
	ans = []
	wordnums = []
	wordnums_indexes = []
	num_index = -2
	word_pos = 0
	for word in query:
		try: 
			w2n.word_to_num(word)
				
			if num_index<0: 
				wordnums.append(word)
				num_index=word_pos
				wordnums_indexes.append(word_pos)

			elif num_index+1==word_pos:
				num_index+=1
				wordnums[-1] = wordnums[-1] + " " + word
			
			elif num_index+1!=word_pos:
				wordnums.append(word)
				num_index=word_pos
				wordnums_indexes.append(word_pos)
		except ValueError: ans.append(word)
		word_pos+=1
	for i in range(len(wordnums_indexes)):
		ans.insert(wordnums_indexes[i], w2n.word_to_num(wordnums[i]))
	return ans


# tiny intent recognition - ir для функций. анализирует запрос и возвращает его анализ
def tir(query, dictionary):	
	from fuzzywuzzy import process
	from ru_word2number import w2n

	pipeline_dict = {
		"pipeline":[],
		"positions":[],
		"source":[]
	}
	wordnums = []
	wordnums_indexes = []
	num_index = -2
	word_pos = 0

	for word in query:
		if len(word)>2:

			flag=False
			for intent, names in dictionary.items():
				processextraction = process.extractOne(word, names)
				if processextraction[1]>75:
					logger.debug(processextraction)
					pipeline_dict['pipeline'].append(intent)
					pipeline_dict['positions'].append(word_pos)
					pipeline_dict['source'].append(processextraction[0])
					flag=True
			if flag==False: 
				try: 
					w2n.word_to_num(word)
				
					if num_index<0: 
						wordnums.append(word)
						num_index=word_pos
						wordnums_indexes.append(word_pos)
						pipeline_dict['positions'].append(word_pos)

					elif num_index+1==word_pos:
						logger.error(wordnums)
						num_index+=1
						wordnums[-1] = wordnums[-1] + " " + word

					elif num_index+1!=word_pos:
						wordnums.append(word)
						num_index=word_pos
						wordnums_indexes.append(word_pos)
						pipeline_dict['positions'].append(word_pos)
				except ValueError: pipeline_dict['pipeline'].append(word)

		word_pos+=1

	for i in range(len(wordnums_indexes)):
		pipeline_dict['pipeline'].insert(wordnums_indexes[i], w2n.word_to_num(wordnums[i]))
		pipeline_dict['source'].insert(wordnums_indexes[i], w2n.word_to_num(wordnums[i]))
	logger.debug(pipeline_dict)
	return pipeline_dict


# планировщик задач. принимает тип планирования, время в формате часы, минуты, секунды,
# имя плагина который необходимо выполнить по истечении времени, и опциональное сообщение,
# которое передается в плагин
def scheduler(stype, timelist, plugin_name, message=""):
	from datetime import datetime, timedelta
	import importlib
	from apscheduler.schedulers.background import BackgroundScheduler

	plugin=importlib.import_module(plugin_name)
	scheduler = BackgroundScheduler()

	def runfunc():
		plugin.run(message)

	if stype=="timer":
		run_time = datetime.now() + timedelta(seconds=timelist[2], minutes=timelist[1], hours=timelist[0])
		logger.debug(run_time)
		scheduler.add_job(runfunc, 'date', run_date=run_time)
		scheduler.start()

	elif stype=="scheduler":
		run_time = str(datetime.now()).split()
		run_time = run_time[0]+" "+":".join(map(str,timelist))
		scheduler.add_job(runfunc, 'date', run_date=run_time)
		scheduler.start()

	elif stype=="alarm":
		None
		



