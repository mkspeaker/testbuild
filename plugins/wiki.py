import sonutils
def run(query):

	import wikipediaapi
	import re

	query = " ".join(query)
	wiki = wikipediaapi.Wikipedia("nigger", "ru")
	ws = wiki.search(query, what=wikipediaapi.SearchWhat.NEAR_MATCH).pages
	for a, b in ws.items(): 
		wiki_page = wiki.page(a)
	sonutils.logger.debug(wiki_page.title)
	text=wiki_page.summary
	while text.find('(') != -1:
		fs=text.find('(')
		ss=text.find(')')
		text = text[:fs]+text[ss+1:]
	text = text[:text.find('\n')]

	sonutils.tts(text)
