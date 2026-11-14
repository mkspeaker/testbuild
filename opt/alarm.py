import sonutils
def run(message):
	sonutils.tts(message)
	sonutils.logger.debug(message)
	#sonutils.tts("время вышло")