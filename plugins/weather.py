import sonutils, requests, json
from fuzzywuzzy import process

def run(context):
    sonutils.logger.info("запущен плагин weather.py")
    cities_dict = [
        "лондон", "париж", "берлин", "мадрид", "рим", "амстердам", "вена", "прага", "варшава", "будапешт",
        "барселона", "милан", "мюнхен", "стокгольм", "осло", "хельсинки", "копенгаген", "дублин", "лиссабон", "брюссель",
        "бухарест", "белград", "люксембург",
        "бостон", "чикаго", "денвер", "даллас", "хьюстон", "майами", "сиэтл", "сан-франциско", "лос-анджелес",
        "нью-йорк", "вашингтон", "детройт",
        "мехико", "буэнос-айрес", "монтевидео", "сан-паулу", "рио-де-женейро",
        "дубай", "тель-авив",
        "сеул", "токио", "осака", "киото", "пекин", "шанхай", "гуанчжоу", "гонконг", "сингапур", "бангкок",
        "сидней",
        "москва", "санкт-петербург", "новосибирск", "екатеринбург", "казань", "новгород", "челябинск", "самара", "омск", "ростов",
        "уфа", "красноярск", "пермь", "воронеж", "волгоград", "краснодар", "саратов", "тюмень", "тольятти", "ижевск",
        "барнаул", "иркутск", "хабаровск", "ярославль", "владивосток", "махачкала", "томск", "оренбург", "кемерово",
        "новокузнецк", "рязань", "астрахань", "пенза", "липецк", "киров", "чебоксары", "калининград", "тверь",
        "сочи", "курск", "ставрополь", "ульяновск", "магнитогорск", "тула", "воркута", "архангельск", "сургут", "севастополь"
    ]

    city = sonutils.find_one(context, cities_dict)
    if city=="": city = "кудрово"
    sonutils.logger.error(city)
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    # получаем данные о температуре и о том, как она ощущается
    sonutils.logger.info(weather_data)
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    description = weather_data['weather'][0]['description']
    if temperature<0 or temperature_feels<0:
        weathertext = 'Сейчас в городе '+ city +" минус "+ str(temperature)[1:]+ ' градус. Ощущается как минус '+ str(temperature_feels)[1:]+ ' градус'+str(description)
    else:
        weathertext = 'Сейчас в городе '+ city+" "+ str(temperature)+ ' градусов. Ощущается как '+ str(temperature_feels)+ ' градусов. '+str(description)

    sonutils.tts(weathertext)
