import sonutils
import subprocess
"""
radios = {
    "максимум": 'http://maximum.hostingradio.ru/maximum96.aacp',
    "рокфм": 'http://nashe1.hostingradio.ru/rock-64.mp3',
    "авторадио": 'http://ic7.101.ru:8000/v3_1',
    "вестифм": 'http://icecast.vgtrk.cdnvideo.ru/vestifm',
    "нашерадио": 'http://nashe1.hostingradio.ru/nashespb128.mp3'
}
"""
radios = {
    "рок фм": "http://nashe1.hostingradio.ru/rock-64.mp3",
    "ультра": "http://nashe1.hostingradio.ru/ultra-64.mp3",
    "наше радио": "http://nashe1.hostingradio.ru/nashespb128.mp3",
    "максимум": "http://maximum.hostingradio.ru/maximum96.aacp",
    "DFM": "http://dfm.hostingradio.ru/dfm128.mp3",
    "европа плюс": "http://europaplus.hostingradio.ru:8014/europaplus320.mp3",
    "русское радио": "http://rusradio.hostingradio.ru/rusradio96.aacp",
    "хит фм": "http://hitfm.hostingradio.ru/hitfm96.aacp",
    "новое радио": "http://icecast-newradio.cdnvideo.ru/newradio3",
    "авто радио": "http://ic7.101.ru:8000/v3_1",
    "дорожное радио": "http://emgregion.hostingradio.ru:8064/moscow.dorognoe.mp3",
    "радио ваня": "http://icecast-radiovanya.cdnvideo.ru:8000/radiovanya",
    "ретро фм": "http://emgregion.hostingradio.ru:8064/moscow.retrofm.mp3",
    "радио шансон": "http://chanson-video.hostingradio.ru:8080/hls/chansonabr/live.m3u8",
    "вести фм": "http://icecast.vgtrk.cdnvideo.ru/vestifm",
    "маяк": "http://icecast.vgtrk.cdnvideo.ru/mayakfm",
    "мир": "http://icecast-mirtv.cdnvideo.ru:8000/radio_mir_256",
    "камеди": "http://ic7.101.ru:8000/stream/air/mp3/256/99",
    "джаз": "http://jazz.streamr.ru/jazz-64.mp3",
    "релакс фм": "http://ic6.101.ru:8000/stream/air/mp3/256/200"
}

def run(query):
    query = "".join(query)
    names = list(radios.keys())
    radio = sonutils.find_one(query,names)
    print(radio)
    link = list(radios.values())[names.index(radio)]
    subprocess.Popen(['mpv', link],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True)
    """
    for radio, link in radios.items():
        sonutils.find_one(query,radios.items()[0])
        if query==radio:
            print("нашел")
            subprocess.Popen(['mpv', link],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True)
        else: print("err")
    """
