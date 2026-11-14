import requests, xmltodict, sonutils



def get_price_by_name(valutename):
	from fuzzywuzzy import process
	CBR_URL="https://www.cbr.ru/scripts/XML_daily.asp"

	cbr_currencies = xmltodict.parse(requests.get(CBR_URL, timeout=5).text)
	cbr_currency_names = []
	for i in range(len(cbr_currencies['ValCurs']['Valute'])):
		cbr_currency_names.append(cbr_currencies['ValCurs']['Valute'][i]['Name'])
			#return float(cbr_currencies['ValCurs']['Valute'][i]['Value'].replace(",","."))
	processextraction = process.extractOne(valutename, cbr_currency_names)
	if processextraction[1]>80: 
		return cbr_currencies['ValCurs']['Valute'][cbr_currency_names.index(processextraction[0])]['VunitRate'].replace(",",".")



def get_price_by_code(valutecode):
	CBR_URL="https://www.cbr.ru/scripts/XML_daily.asp"
	cbr_currencies = xmltodict.parse(requests.get(CBR_URL, timeout=5).text)

	for i in range(len(cbr_currencies['ValCurs']['Valute'])):
		if cbr_currencies['ValCurs']['Valute'][i]['CharCode']==valutecode:
			return cbr_currencies['ValCurs']['Valute'][i]['VunitRate'].replace(",",".")



def make_txt_price(name, price): 
	ans = str(price).split(".")
	sonutils.logger.debug(ans)
	ans = f"{name} стоит {ans[0]} целых {ans[1][0]} десятых рублей"
	return ans


def run(context):

	currencies = {
		"valute": ["доллар", "евро", "рубль", "фунт", "йена","юань","лира","гривна",
			"песо","реал","рупия","бат","донг","крона","злотый","шекель","динар",
			"риал","дирхам","франк","тенге"]
	}

	if len(context)==0:
		dollar_price = make_txt_price("доллар", get_price_by_code("USD"))
		euro_price = make_txt_price("евро", get_price_by_code("EUR"))
		print(dollar_price, euro_price)

	else:
		pipeline_dict = sonutils.tir(context, currencies)

		if pipeline_dict['pipeline'].count('valute')==1:
			print(pipeline_dict)
			valutepos = pipeline_dict['pipeline'].index('valute')
			valutename = pipeline_dict['source'][valutepos]
			if valutename=="доллар": valutename="доллар сша"
			multiplier=[x for x in pipeline_dict['pipeline'] if type(x)==int]
			print(multiplier)
			if len(multiplier)!=0:
				multiplier = multiplier[0]
				valute_price = make_txt_price(str(multiplier)+" "+valutename, round(multiplier*float(get_price_by_name(valutename)),1))
				sonutils.tts(valute_price)
				print(valute_price)
			else:
				valute_price = make_txt_price(valutename, get_price_by_name(valutename))
				sonutils.tts(valute_price)
				print(valute_price)
		
		#sonutils.tts(f"доллар стоит ")
