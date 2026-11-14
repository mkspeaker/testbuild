import sonutils
import re, xmltodict, requests

#def

def run():
	RBC_URL = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
	titles = []
	f_title=0
	l_title=5
	news_dict = xmltodict.parse(requests.get(RBC_URL, timeout=5).text)
	for i in range(30):
		titles.append(news_dict['rss']['channel']['item'][i]['title'])
	print(titles[f_title:l_title])
	query=input("контекст? ")
	
	if len(query)!=0: 

		if "расскажи подробнее про" in query:
			query=query.replace("расскажи подробнее про", "")
			title_num=f_title
			full_text=""
			pattern = r"&[^;]*;"

			for title in titles[f_title:l_title]:
				if query in title:
					try:
						full_text = news_dict['rss']['channel']['item'][title_num]['rbc_news:full-text'][:-37]
						full_text = " ".join(re.sub(pattern, "", full_text).split())
					except: pass
				title_num+=1

			if len(full_text)!=0:
				print(full_text)

		if "продолжай" in query:
			f_title+=5
			l_title+=5
			print(titles[f_title:l_title])


