import os
import subprocess
from utils import load_ready_model, play_infer, tts_debug
from configs import JTTS_config, JarvisMetaConfig
from command_voices import open_app_voices, get_date_voices, get_time_voices, abstract_voice, create_note_voices, hello_voices, hello_2_voices, g4f_image_voices, search_google_voices
from random import randint


if tts_debug == 'xtts':
    JTTS_config = JTTS_config()
    JarvisMetaConfig = JarvisMetaConfig()
    tts_model = load_ready_model('JTTS', JTTS_config)

def hello():
    text = hello_voices[randint(0, len(hello_voices)-1)]
    
    tts_debug('print', text=text)

def hello_2():
    text = hello_2_voices[randint(0, len(hello_2_voices)-1)]
    
    tts_debug('print', text=text)
        
def open_app(app_name):

    if os.path.exists(f'/Users/user/Desktop/{app_name}.app'):
        subprocess.call(('open', f'/Users/user/Desktop/{app_name}.app'))
    elif os.path.exists(f'/Applications/{app_name}.app'):
        subprocess.call(('open', f'/Applications/{app_name}.app'))
    elif os.path.exists(f"System/Applications/{app_name}.app"):
        subprocess.call(('open', f'System/Applications/{app_name}.app'))
    elif os.path.exists(f'/Applications/{app_name}/{app_name}.app'):
        subprocess.call(('open', f'/Applications/{app_name}/{app_name}.app'))
        
    text = open_app_voices[randint(0, len(open_app_voices)-1)]
    
    tts_debug('print', text=text)    

def close_app(app_name):
    
    import psutil

    for process in psutil.process_iter():
        try:
            if process.name() == app_name:
                process.kill()
        except Exception as e:
            print(e)

def start_bluetooth():
        pass

def stop_bluetooth():
    pass

def connect_light():
    pass

def disconnect_light():
    pass

def light_on():
    pass

def start_airdrop():
    pass

def stop_airdrop():
    pass

def get_battery():
    pass

def listen_me():
    pass

def no_listen_me():
    pass

def start_wifi():
    pass

def get_availabe_device_wifi():
    pass

def weather_today():
    
    pass
    # import requests

    # city = 'Москва'

    # Api_key = 'b1f0392026be880ca306b077739ebe75'

    # url = f"http://api.openweathermap.org/data/2.5/forecast?id=2021851&units=metric&lang=ru&appid={Api_key}"

    # weather_data = requests.get(url).json()
    
    # temp = 0
    # temp_min = []
    # temp_max = []
    # feels_like = 0
    # descroption = ''
    # clouds = 0
    # wind = 0
    
    # act_date = get_date()

    # print(weather_data['list'][0])
    # for i in range(40):
    #     if weather_data['list'][i]['dt_txt'][:10] == act_date:
    #         if temp == 0:
    #             temp = (weather_data['list'][i]['main']['temp'])
    #         temp_min.append(temp)
    #         temp_max.append(temp)

def weather_tomorrow():
    pass

def weather_after_tomorrow():
    pass

def get_date(back = None):
    
    import datetime

    now = str(datetime.datetime.now())
    
    if back is not None:
        return now[:10]

    month = now[5:7]
    day = now[8:10]

    if '0' in month:
        month = month[-1]

    if '0' in day:
        day = day[-1]
        
    months = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    }
    
    days = {
        1: 'первое',
        2: 'второе',
        3: 'третье',
        4: 'четвертое',
        5: 'пятое',
        6: 'шестое',
        7: 'седьмое',
        8: 'восьмое',
        9: 'девятое',
        10: 'десятое',
        11: 'одиннадцатое',
        12: 'двенадцатое',
        13: 'тринадцатое',
        14: 'четырнадцатое',
        15: 'пятнадцатое',
        16: 'шестнадцатое',
        17: 'семнадцатое',
        18: 'восемнадцатое',
        19: 'девятьнадцатое',
        20: 'двадцатое',
        21: 'двадцать первое',
        22: 'двадцать второе',
        23: 'двадцать третье',
        24: 'двадцать четвертое',
        25: 'двадцать пятое',
        26: 'двадцать шестое',
        27: 'двадцать седьмое',
        28: 'двадцать восьмое',
        29: 'двадцать девятое',
        30: 'тридцатое',
        31: 'тридцать первое',
    }
        
    text = get_date_voices[randint(0, len(get_date_voices)-1)]
    text = text.format(day=days.get(day), month=months.get(month))
    
    tts_debug('print', text=text) 

def get_time():

    import datetime

    now = str(datetime.datetime.now())

    time = now[11:19]
    hours = int(time[:2])
    minutes = int(time[3:5])

    if hours == 1:
        hours_word = 'час'
    elif 11 <= hours <= 19:
        hours_word = 'часов'
    elif 2 <= hours % 10 <= 4:
        hours_word = 'часа'
    else:
        hours_word = 'часов'
        
    if 11 <= minutes <= 19:
        minutes_word = 'минут'
    elif minutes % 10 == 1:
        minutes_word = 'минута'
    elif 2 <= minutes % 10 <= 4:
        minutes_word = 'минуты'
    else:
        minutes_word = 'минут'

    text = get_time_voices[randint(0, len(get_time_voices)-1)]
    text = text.format(hours=hours, hours_word=hours_word, minutes=minutes, minutes_word=minutes_word)
    
    tts_debug('print', text=text)

def g4f_image(promt, client):

    response = client.images.generate(
        model=JarvisMetaConfig.g4f_image_model_name,
        prompt=promt,
        response_format="url"
    )

    image_url = response.data[0].url

    print(f"Generated image URL: {image_url}")
    
    text = g4f_image_voices[randint(0, len(g4f_image_voices)-1)]
    
    tts_debug('print', text=text)
    
    return image_url
    
    
def g4f_chat(transcribe = None, client = None):

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": transcribe}],
        model=JarvisMetaConfig.g4f_chat_model_name,
    )
    gpt_response = response.choices[0].message.content
    
    tts_debug('print', text=gpt_response)
    
    return {'assistant':gpt_response}
            
def create_note(title, text):

    import subprocess

    body = '''tell application "Notes"
        activate
        tell account "iCloud"
            make new note at folder "Notes" with properties {{body:"{}"}}
        end tell
    end tell'''

    title_template = r'<div><b><span style=\"font-size: 24px\">{}</span></b></div>'
    chapter_template = r'<div><span style=\"font-size: 18px\">{}</span><br></div>'
    
    title[0] = title[0].upper()

    els = {
        'title': title,
        'body': text
    }

    text = title_template.format(els.get('title'))

    lst = els.get('body')

    text += chapter_template.format(f'{lst}')

    cmd = body.format(text)
    out = subprocess.run(['osascript', '-e', cmd.encode()], capture_output=True)
    
    text = create_note_voices[randint(0, len(create_note_voices)-1)]
    
    tts_debug('print', text=text) 
    
    
def search_google(text: str = None, num: int = 1, gen: bool = None):
    
    from googlesearch import search
    import webbrowser
    
    if gen is not None and text is None:
        
        res = 0
        
        for i, el in enumerate(gen):
            if i == num-1:
                res = el
                break
            
        if res != 0:
            
            text = search_google_voices[randint(0, len(search_google_voices)-1)]
            
            tts_debug('print', text=text)
            
            webbrowser.open(res)
        
    else:

        d = search(text, lang='ru', num_results=10)

        res = 0

        for i, el in enumerate(d):
            if i == num-1:
                res = el
                break
            
        if res != 0:
            
            text = search_google_voices[randint(0, len(search_google_voices)-1)]
            
            tts_debug('print', text=text)

            webbrowser.open(res)
    
        return d
    
def Abstract(context):
    
    import subprocess

    body = '''tell application "Notes"
        activate
        tell account "iCloud"
            make new note at folder "Notes" with properties {{body:"{}"}}
        end tell
    end tell'''

    title_template = r'<div><b><span style=\"font-size: 24px\">{}</span></b></div>'
    chapter_template = r'<div><span style=\"font-size: 18px\">{}</span><br></div>'

    text = title_template.format(f'Конспект {0}')
    
    text += r'<div></div>'

    for message in context:
        
        if 'user' in message.keys():

            text += chapter_template.format(f'user: {message.get('user')}')
            text += r'<div></div>'
            
        elif 'assistant' in message.keys():
            
            text += chapter_template.format(f'assistant: {message.get('assistant')}')
            text += r'<div></div>'
    
    cmd = body.format(text)
    
    subprocess.run(['osascript', '-e', cmd.encode()], capture_output=True)
    
    text = abstract_voice[randint(0, len(abstract_voice)-1)]
    
    tts_debug('print', text=text) 
    
            
