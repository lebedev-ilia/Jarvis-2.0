from flet import *
import time
import math
import torch
import pyaudio
import numpy as np
from utils import normalaize_signal, remove_jarvis_from_transcribe
from jarvis_text_classifier.utils import convert_example_to_input_infer
from configs import JSTT_config, JTC_config
from classes import classes
import logging
import os

logging.getLogger('nemo_logger').setLevel(logging.ERROR)
logging.getLogger('nemo_logging').setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['CURL_CA_BUNDLE'] = JSTT_config.os_environ

streaming_voice = []
stop_voice = None
stop_voice_cnt = 0
data_fr = []
stop_streaming = None
start = None
wait = 0
chatgpt = None
chatgpt_context = []
search_google = None
search_google_wait = 0

chat_mesage = ''
reactor_off = False
chat_mesage_voice_flag = None
chat_mesage_flag = None

def main(page: Page):
    
    BG = '#191919'
    
    def particles_creator(animate_offset, animate_opacity, width, height, offset):
        return Container(
            animate_offset=animation.Animation(animate_offset, AnimationCurve.EASE_IN_OUT),
            animate_opacity=animation.Animation(animate_opacity, AnimationCurve.EASE_IN_CUBIC),
            bgcolor='#ffffff', 
            width=width, 
            height=height, 
            border_radius=10, 
            offset=offset)
    
    p1 = particles_creator(2000, 1200, 1.1,1.1, (36,40))
    p2 = particles_creator(1600, 1200, 1.1,1.1, (33,44))
    p3 = particles_creator(700, 1200, 1.1,1.1, (26,51))
    p4 = particles_creator(1400, 1200, 1.1,1.1, (21,58))
    p5 = particles_creator(2100, 1200, 1.1,1.1, (18,64))
    p6 = particles_creator(2200, 1200, 1.1,1.1, (16,71))
    p7 = particles_creator(1200, 1200, 1.1,1.1, (15,77))
    p8 = particles_creator(1400, 1200, 1.1,1.1, (15,83))
    p9 = particles_creator(1700, 1200, 1.1,1.1, (17,90))
    p10 = particles_creator(1800, 1200, 1.1,1.1, (19,96))
    p11 = particles_creator(1900, 1200, 1.1,1.1, (21,102))
    p12 = particles_creator(2200, 1200, 1.1,1.1, (25,108))
    p13 = particles_creator(700, 1200, 1.1,1.1, (28,114))
    p14 = particles_creator(1900, 1200, 1.1,1.1, (32,120))
    p15 = particles_creator(2100, 1200, 1.1,1.1, (36,126))
    p16 = particles_creator(2000, 1200, 1.1,1.1, (41,132))
    p17 = particles_creator(1300, 1200, 1.1,1.1, (45,137))
    p18 = particles_creator(1600, 1200, 1.1,1.1, (51,142))
    p19 = particles_creator(1700, 1200, 1.1,1.1, (57,146))
    p20 = particles_creator(1800, 1200, 1.1,1.1, (63,150))
    p21 = particles_creator(900, 1200, 1,1, (69,152))
    p22 = particles_creator(2200, 1200, 1,1, (76,153))
    p23 = particles_creator(2300, 1200, 1,1, (84,153))
    p24 = particles_creator(1400, 1200, 1,1, (91,153))
    p25 = particles_creator(1400, 1200, 1,1, (98,152))
    p26 = particles_creator(1400, 1200, 1,1, (105,150))
    p27 = particles_creator(1400, 1200, 1,1, (112,146))
    p28 = particles_creator(1400, 1200, 1,1, (119,142))
    p29 = particles_creator(1400, 1200, 1,1, (126,137))
    p30 = particles_creator(1400, 1200, 1,1, (132,133))
    p31 = particles_creator(1400, 1200, 1,1, (136,126))
    p32 = particles_creator(1400, 1200, 1,1, (139,120))
    p33 = particles_creator(1400, 1200, 1,1, (142,114))
    p34 = particles_creator(1400, 1200, 1,1, (145,108))
    p35 = particles_creator(1400, 1200, 1,1, (148,102))
    p36 = particles_creator(1400, 1200, 1,1, (150,96))
    p37 = particles_creator(1400, 1200, 1,1, (152,90))
    p38 = particles_creator(1400, 1200, 1,1, (152,83))
    p39 = particles_creator(1400, 1200, 1,1, (150,77))
    p40 = particles_creator(1400, 1200, 1.1,1.1, (148,71))
    p41 = particles_creator(1400, 1200, 1.1,1.1, (146,64))
    p42 = particles_creator(1400, 1200, 1.1,1.1, (144,58))
    p43 = particles_creator(1400, 1200, 1.1,1.1, (142,51))
    p44 = particles_creator(1400, 1200, 1.1,1.1, (138,44))
    p45 = particles_creator(1400, 1200, 1.1,1.1, (134,39))
    p46 = particles_creator(1400, 1200, 1.1,1.1, (130,35))
    p47 = particles_creator(1400, 1200, 1.1,1.1, (124,31))
    p48 = particles_creator(1400, 1200, 1.1,1.1, (118,28))
    p49 = particles_creator(1400, 1200, 1.1,1.1, (112,28))
    p50 = particles_creator(1400, 1200, 1.1,1.1, (106,26))
    p51 = particles_creator(1400, 1200, 1.1,1.1, (100,24))
    p52 = particles_creator(1400, 1200, 1.1,1.1, (92,23))
    p53 = particles_creator(1400, 1200, 1.1,1.1, (86,22))
    p54 = particles_creator(1400, 1200, 1.1,1.1, (79,22))
    p55 = particles_creator(1400, 1200, 1.1,1.1, (72,23))
    p56 = particles_creator(1400, 1200, 1.1,1.1, (66,24))
    p57 = particles_creator(1400, 1200, 1.1,1.1, (59,26))
    p58 = particles_creator(1400, 1200, 1.1,1.1, (52,28))
    p59 = particles_creator(1400, 1200, 1.1,1.1, (46,31))
    p60 = particles_creator(1400, 1200, 1.1,1.1, (40,34))
    
    par = {
    "p1":(p1,(0,0)),
    "p2":(p2,(-23,24)),
    "p3":(p3,(5,21)),
    "p4":(p4,(21,10)),
    "p5":(p5,(-40,0)),
    "p6":(p6,(-17,51)),
    "p7":(p7,(-24,65)),
    "p8":(p8,(-40,66)),
    "p9":(p9,(-40,42)),
    "p10":(p10,(-32,82)),
    "p11":(p11,(-18,95)),
    "p12":(p12,(-35,108)),
    "p13":(p13,(-48,128)),
    "p14":(p14,(-23,128)),
    "p15":(p15,(-21,146)),
    "p16":(p16,(3,152)),
    "p17":(p17,(23,210)),
    "p18":(p18,(20,180)),
    "p19":(p19,(38,166)),
    "p20":(p20,(50,200)),
    "p21":(p21,(65,188)),
    "p22":(p22,(106,203)),
    "p23":(p23,(89,189)),
    "p24":(p24,(110,180)),
    "p25":(p25,(126,188)),
    "p26":(p26,(136,175)),
    "p27":(p27,(156,184)),
    "p28":(p28,(177,199)),
    "p29":(p29,(169,152)),
    "p30":(p30,(175,173)),
    "p31":(p31,(176,130)),
    "p32":(p32,(189,144)),
    "p33":(p33,(81,220)),
    "p34":(p34,(-15,178)),
    "p35":(p35,(197,125)),
    "p36":(p36,(190,96)),
    "p37":(p37,(200,90)),
    "p38":(p38,(192,110)),
    "p39":(p39,(181,77)),
    "p40":(p40,(192,58)),
    "p41":(p41,(203,29)),
    "p42":(p42,(150,0)),
    "p43":(p43,(185,14)),
    "p44":(p44,(168,20)),
    "p45":(p45,(155,-24)),
    "p46":(p46,(180,-20)),
    "p47":(p47,(138,220)),
    "p48":(p48,(127,-20)),
    "p49":(p49,(85,-17)),
    "p50":(p50,(106,-19)),
    "p51":(p51,(100,-38)),
    "p52":(p52,(68,-40)),
    "p53":(p53,(60,-22)),
    "p54":(p54,(36,-40)),
    "p55":(p55,(31,-13)),
    "p56":(p56,(205,172)),
    "p57":(p57,(218,70)),
    "p58":(p58,(-2,-28)),
    "p59":(p59,(-60,70)),
    "p60":(p60,(225,135)),
    }
    
    def particle_update_offset(p, offset):
        p.offset = offset
        p.opacity = 1
        p.update()
    
    def particle_back_offset(p, offset):
        p.offset = offset
        p.update()

    def animate_particles():
        for i in range(0, 60, 10):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        
        from utils import load_ready_model
        from configs import JSTT_config
        JSTT_config = JSTT_config()
        asr_model = load_ready_model('JSTT', JSTT_config)
        
        for i in range(1, 60, 9):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        
        for i in range(1, 60, 8):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)

        chat_cont.opacity = 1
        chat_cont.update()
        
        from configs import JTC_config
        JTC_config = JTC_config()
        tc_model, tokenizer = load_ready_model('JTC', JTC_config)
        
        for i in range(1, 60, 7):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        
        import g4f
        client = g4f.client.Client()
        
        for i in range(1, 60, 6):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        time.sleep(1)
        for i in range(1, 60, 5):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        time.sleep(1)
        for i in range(1, 60, 4):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        time.sleep(1)
        for i in range(1, 60, 3):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        time.sleep(1)
        for i in range(1, 60, 2):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        time.sleep(1)
        for i in range(1, 60, 1):
            p, offset = par.get(f'p{i+1}')
            particle_update_offset(p, offset)
        
        return asr_model, tc_model, tokenizer, client
    
    def back_particles():
        particle_back_offset(p1, (36,40))
        particle_back_offset(p2, (33,44))
        particle_back_offset(p3, (26,51))
        particle_back_offset(p4, (21,58))
        particle_back_offset(p5, (18,64))
        particle_back_offset(p6, (16,71))
        particle_back_offset(p7, (15,77))
        particle_back_offset(p8, (15,83))
        particle_back_offset(p9, (17,90))
        particle_back_offset(p10, (19,96))
        particle_back_offset(p11, (21,102))
        particle_back_offset(p12, (25,108))
        particle_back_offset(p13, (28,114))
        particle_back_offset(p14, (32,120))
        particle_back_offset(p15, (36,126))
        particle_back_offset(p16, (41,132))
        particle_back_offset(p17, (45,137))
        particle_back_offset(p18, (51,142))
        particle_back_offset(p19, (57,146))
        particle_back_offset(p20, (63,150))
        particle_back_offset(p21, (69,152))
        particle_back_offset(p22 , (76,153))
        particle_back_offset(p23 , (84,153))
        particle_back_offset(p24 , (91,153))
        particle_back_offset(p25 , (98,152))
        particle_back_offset(p26 , (105,150))
        particle_back_offset(p27 , (112,146))
        particle_back_offset(p28 , (119,142))
        particle_back_offset(p29 , (126,137))
        particle_back_offset(p30 , (132,133))
        particle_back_offset(p31 , (136,126))
        particle_back_offset(p32 , (139,120))
        particle_back_offset(p33 , (142,114))
        particle_back_offset(p34 , (145,108))
        particle_back_offset(p35 , (148,102))
        particle_back_offset(p36 , (150,96))
        particle_back_offset(p37 , (152,90))
        particle_back_offset(p38 , (152,83))
        particle_back_offset(p39 , (150,77))
        particle_back_offset(p40, (148,71))
        particle_back_offset(p41, (146,64))
        particle_back_offset(p42, (144,58))
        particle_back_offset(p43, (142,51))
        particle_back_offset(p44, (138,44))
        particle_back_offset(p45, (134,39))
        particle_back_offset(p46, (130,35))
        particle_back_offset(p47, (124,31))
        particle_back_offset(p48, (118,28))
        particle_back_offset(p49, (112,28))
        particle_back_offset(p50, (106,26))
        particle_back_offset(p51, (100,24))
        particle_back_offset(p52, (92,23))
        particle_back_offset(p53, (86,22))
        particle_back_offset(p54, (79,22))
        particle_back_offset(p55, (72,23))
        particle_back_offset(p56, (66,24))
        particle_back_offset(p57, (59,26))
        particle_back_offset(p58, (52,28))
        particle_back_offset(p59, (46,31))
        particle_back_offset(p60, (40,34))

    fon = Container(
        width=156,
        height=156,
        border_radius=85,
        bgcolor=BG,
        margin=margin.only(top=6, left=6)
    )
    
    light = Container(
        opacity=0,
        animate_opacity=400,
        margin=margin.only(top=-46, left=-44),
        content=Image(
            src='/Users/user/Downloads/lightt2.png',
            width=255,
            fit=ImageFit.CONTAIN,
        ))
    
    img_on = Image(
            opacity=0,
            src='/Users/user/Downloads/1.png',
            width=170,
            fit=ImageFit.CONTAIN,
            animate_opacity=400,
        )
    
    img_off = Image(
            opacity=1,
            src='/Users/user/Downloads/2.png',
            width=170,
            fit=ImageFit.CONTAIN,
            animate_opacity=400,
        )
    
    stack_particles = Stack(
        controls=[p1,
                    p2,
                    p3,
                    p4,
                    p5,
                    p6,
                    p7,
                    p8,
                    p9,
                    p10,
                    p11,
                    p12,
                    p13,
                    p14,
                    p15,
                    p16,
                    p17,
                    p18,
                    p19,
                    p20,
                    p21,
                    p22,
                    p23,
                    p24,
                    p25,
                    p26,
                    p27,
                    p28,
                    p29,
                    p30,
                    p31,
                    p32,
                    p33,
                    p34,
                    p35,
                    p36,
                    p37,
                    p38,
                    p39,
                    p40,
                    p41,
                    p42,
                    p43,
                    p44,
                    p45,
                    p46,
                    p47,
                    p48,
                    p49,
                    p50,
                    p51,
                    p52,
                    p53,
                    p54,
                    p55,
                    p56,
                    p57,
                    p58,
                    p59,
                    p60]
    )
    
    def message_create(bot, t):
        
        global chat_mesage, chat_mesage_voice_flag
        
        border_radius = 15
        max_lines = 1
        height = 37
        width = (len(t) * 10) if (len(t) * 10) > 150 else 150
        p_left, p_top, p_right, p_bottom = 7,5,7,5
            
        if width > 330:
            ratio = math.ceil(width / 330)
            width = 330
            height = 37 + (30 * ratio * 0.65)
            max_lines=ratio
            border_radius = 30
            p_left, p_top, p_right, p_bottom = 12,3,12,3
            
        if bot:
            border_color = 'blue'
        else:
            border_color = '#FF00FF'
        
        if chat_mesage_voice_flag is False:
            chat_mesage = t
            
        return Container(
            padding=padding.only(p_left,p_top,p_right,p_bottom),
            alignment=Alignment(0,0),
            width=width,
            height=height,
            bgcolor=BG,
            border=border.all(3, border_color),
            border_radius=border_radius,
            content=Text(
                max_lines=max_lines,
                value=t
            ),
            key=t
        )
            
    def chat_input_submit(e):
        global chat_mesage_voice_flag
        chat_mesage_voice_flag = False
        mesage_cont_column.controls.append(
            message_create(False, chat_input.value)
        )
        mesage_cont_column.update()
        mesage_cont_column.scroll_to(key=chat_input.value, duration=400)
        chat_input.value = ''
        chat_input.update()
        
    def chat_input_transcribe(transcribe):
        mesage_cont_column.controls.append(
            message_create(False, transcribe)
        )
        mesage_cont_column.update()
        mesage_cont_column.scroll_to(key=transcribe, duration=400)
        chat_input.value = ''
        chat_input.update()
        
    def reactor_on(e):
        
        global start, wait, chatgpt, search_google, stop_streaming, data_fr, chat_mesage, chat_mesage_flag, stop_voice, reactor_off, chat_mesage_voice_flag
        from utils import load_ready_model
        
        start = True
        reactor_off = False
        
        vad_model = load_ready_model('JVAD')
        
        audio = pyaudio.PyAudio()

        def stream_callback(input_data, frame_count, time_info, flags):
            global chat_mesage, chat_mesage_flag, reactor_off, stop_streaming
            
            if chat_mesage != '':
                chat_mesage_flag = True
            if reactor_off:
                stop_streaming = True
            
            global data_fr, streaming_voice, stop_voice_cnt, stop_voice
            data = torch.tensor(np.fromstring(input_data, dtype=np.int16))
            speech_prob = vad_model(data, JSTT_config.RATE).item()
            sp = round(speech_prob, 3)
            data_fr.append(data)
            if len(streaming_voice) > 50 and stop_voice == None:
                streaming_voice = []
                data_fr = []
            elif stop_voice:
                streaming_voice.append(sp)
                if sp < 0.31:
                    stop_voice_cnt += 1
                if stop_voice_cnt > 60:
                    streaming_voice = []
                    stop_voice = None
                    stop_voice_cnt = 0
                    stop_streaming = True
                elif sp > 0.81:
                    stop_voice_cnt = 0
            elif sp >= 0.81:
                stop_voice = True
                streaming_voice.append(sp)
            return input_data, pyaudio.paContinue

        stream = audio.open(format=JSTT_config.FORMAT, channels=JSTT_config.CHANNELS,rate=JSTT_config.RATE, input=True, input_device_index=0, stream_callback=stream_callback,frames_per_buffer=JSTT_config.CHUNK)
        
        if img_on.opacity == 0:
            
            img_on.opacity = 1
            img_on.update()
            light.opacity = 1
            light.update()
            cont_img.on_click = None
            
            asr_model, tc_model, tokenizer, client = animate_particles()
            
            cont_img.on_click = reactor_on
            
            with torch.no_grad():

                while start:
                        
                    stream.start_stream()
                    
                    while stream.is_active:
                        if stop_streaming or chat_mesage_flag:
                            stream.stop_stream()
                            if reactor_off == True:
                                start = None
                            stop_streaming = None
                            break
                        
                    if reactor_off:
                        
                        break
                    
                    else:
                        
                        if chat_mesage_flag:
                            
                            transcribe = chat_mesage
                            chat_mesage_flag = None
                            chat_mesage = ''
                        
                        else:
                            
                            data = normalaize_signal(data_fr)
                            transcribe = ((asr_model.transcribe(data))[0]).text.lower()
                            chat_mesage_voice_flag = True
                            chat_input_transcribe(transcribe)
                        
                        data_fr = []

                        if len(transcribe) == 0:
        
                            wait += 1
                        
                        else:
                            
                            wait = 0
                                            
                            func = None
                            
                            transcribe, jarvis_name_flag = remove_jarvis_from_transcribe(transcribe)
                            
                            if jarvis_name_flag == False:
                                
                                if wait <= 3:
                                    
                                    jarvis_name_flag = True
                                    
                            if jarvis_name_flag:
                                
                                transcribe_list = transcribe.split(' ')
                                
                                if search_google and 'выключи поиск гугл' not in transcribe and \
                                    'загугли' not in transcribe or 'найди в гугл' not in transcribe and \
                                        search_google_wait == 0:
                                            
                                    nums_res = {
                                        'первый': 1,
                                        'второй': 2,
                                        'третий': 3,
                                        'четвертый': 4,
                                        'пятый': 5,
                                        'шестой': 6,
                                        'седьмой': 7,
                                        'восьмой': 8,
                                        'девятый': 9,
                                        'десятый': 10,
                                    }
                                    
                                    for i, key in enumerate(nums_res.keys()):
                                        if key in transcribe:
                                            num = nums_res.get(key)
                                            
                                            func(text=None, num=num, gen=search_google)
                                            break
                                        
                                        elif i == 9:
                                            
                                            search_google_wait += 1
                                            
                                elif 'загугли' in transcribe or 'найди в гугл' in transcribe:
                                    
                                        transcribe = transcribe[transcribe.index('загугли')+8:]
                                        
                                        search_google_wait == 0

                                        search_google = func(transcribe, num=1, gen=None)

                                elif transcribe_list[0] == 'что' or \
                                    (transcribe_list[0] == 'что' and transcribe_list[0] == 'делать') or \
                                    (transcribe_list[0] == 'что' and transcribe_list[0] == 'такое'):
                                    
                                    if len(gpt_context) > 15:
                                        
                                        gpt_context.pop(0)
                                        gpt_context.pop(1)
                                    
                                    gpt_context.append({'user':transcribe})
                                    gpt_context.append(func(transcribe, client))
                                    
                                elif 'создай' in transcribe and 'заметку' in transcribe:
                                    
                                    title = transcribe[transcribe.index('заголовок')+10:transcribe.index('текст')-1]
                                    text = transcribe[transcribe.index('текст')+6:]
                                    
                                    func(title, text)
                                    
                                elif 'создай' in transcribe and 'конспект' in transcribe:
                                
                                    func(gpt_context)
                                    
                                    gpt_context = []
                                
                                else:
                                    
                                    if isinstance(func, tuple):
                                        
                                        func[0](func[1])
                                        
                                    else:
                                        
                                        func()
                
        else:
            
            reactor_off = True
            stream.stop_stream()
            audio.terminate()
            
            cont_img.on_click = None
            cont_img.update()
            back_particles()
            chat_cont.opacity = 0
            chat_cont.update()
            cont_img.on_click = reactor_on
            cont_img.update()
            img_on.opacity = 0
            img_on.update()
            light.opacity = 0
            light.update()
    
    cont_img = Container(
        offset=(0.81,1.1),
        content=Stack(
            controls=[
                stack_particles,
                fon,
                img_off,
                img_on,
                light,
                ]
            ),
        on_click=reactor_on
    )
    
    chat_input = TextField(
        text_size=14.5,
        on_submit=chat_input_submit
    )
    
    input_mesage = Container(
        width=400,
        height=41,
        border=border.all(1, 'white'),
        content=chat_input
    )
    
    mesage_cont_column = Column(
        scroll='auto',
    )
    
    mesage_cont = Container(
        margin=margin.only(top=20),
        padding=padding.only(left=20),
        width=400,
        height=478,
        content=mesage_cont_column
    )
    
    chat_column = Column(
        controls=[
            mesage_cont,
            input_mesage
        ]
    )
    
    chat_cont = Container(
        animate_opacity=animation.Animation(1000, AnimationCurve.EASE_IN_OUT),
        opacity=1,
        width=400,
        height=550,
        bgcolor=BG,
        border=border.all(1, '#ffffff'),
        border_radius=10,
        offset=(0.215,0.65),
        content=chat_column
    )
    
    title = Image(
        src='/Users/user/Downloads/jarvis_app_name.png',
        opacity=0,
        width=300,
        offset=(0.344, 0.1)
    )
    
    def settings(e):
        main_row.controls.append(
            settings_fon
        )
        main_row.update()
    
    menu_button = Container(
        margin=margin.only(left=30, top=30),
        content=Icon(
            Icons.MENU,
            size=30,
        ),
        on_click=settings
    )
    
    menu_column = Column(
        controls=[
            menu_button
        ]
    )
        
    first_wrapper = Container(
        offset=(-0.018,-0.011),
        height=914,
        width=499,
        # border=border.all(1, 'red'),
        # border_radius=10,
        content=menu_column
    )    
        
    second_wrapper_column = Column(
        controls=[
            title,
            cont_img
        ]
    )   
        
    second_wrapper = Container(
        offset=(-0.038,-0.0114),
        height=913,
        width=499,
        # border=border.all(1, 'blue'),
        # border_radius=10,
        content=second_wrapper_column
    )

    third_wrapper = Container(
        height=915,
        width=499,
        # border=border.all(1, 'white'),
        # border_radius=10,
        offset=(-0.057,-0.009),
        content=Column(
            controls=[
                chat_cont
            ]
        )
    )    

    settings_items = {
        'JarvisMeta':{
            'len':2,
            'g4f_image_model_name':TextField(value='flux', border=border.all(0.2, 'black'), border_radius=22),
            'g4f_chat_model_name':TextField(value='gpt-4', border=border.all(0.2, 'black'), border_radius=22),
            },
        'JTTS':{
            'len':11,
            'seed':TextField(value='1234', border=border.all(0.2, 'black'), border_radius=22),
            'main_path':TextField(value='/Users/user/Desktop/jarvis/Jarvis', border=border.all(0.2, 'black'), border_radius=22),
            'ratio_set':TextField(value='[80, 20]', border=border.all(0.2, 'black'), border_radius=22),
            'batch_size':TextField(value='1', border=border.all(0.2, 'black'), border_radius=22),
            'lr':TextField(value='0.001', border=border.all(0.2, 'black'), border_radius=22),
            'wd':TextField(value='0.00001', border=border.all(0.2, 'black'), border_radius=22),
            'epoch':TextField(value='50', border=border.all(0.2, 'black'), border_radius=22),
            'log_interval':TextField(value='2', border=border.all(0.2, 'black'), border_radius=22),
            'speaker_wav':TextField(value='/Users/user/Desktop/jarvis/Jarvis/jarvis_dataset/jar58_out.wav', border=border.all(0.2, 'black'), border_radius=22, width=550),
            'MODEL_NAME':TextField(value='tts_models/multilingual/multi-dataset/xtts_v2', border=border.all(0.2, 'black'), border_radius=22),
            'USE_GPU':TextField(value='False', border=border.all(0.2, 'black'), border_radius=22),
            },
        'JSTT':{
            'len':6,
            'FORMAT':TextField(value='t_per1', border=border.all(0.2, 'black'), border_radius=22),
            'CHANNELS':TextField(value='1', border=border.all(0.2, 'black'), border_radius=22),
            'RATE':TextField(value='16000', border=border.all(0.2, 'black'), border_radius=22),
            'CHUNK':TextField(value='512', border=border.all(0.2, 'black'), border_radius=22),
            'os_environ':TextField(value='', border=border.all(0.2, 'black'), border_radius=22),
            'MODEL_NAME':TextField(value='nvidia/stt_ru_conformer_ctc_large', border=border.all(0.2, 'black'), border_radius=22),
            },
        'JTC':{
            'len':13,
            'BERT_MODEL':TextField(value='bert-base-uncased', border=border.all(0.2, 'black'), border_radius=22),
            'MAX_SEQ_LENGTH':TextField(value='100', border=border.all(0.2, 'black'), border_radius=22),
            'BATCH_SIZE':TextField(value='16', border=border.all(0.2, 'black'), border_radius=22),
            'GRADIENT_ACCUMULATION_STEPS':TextField(value='1', border=border.all(0.2, 'black'), border_radius=22),
            'NUM_TRAIN_EPOCHS':TextField(value='20', border=border.all(0.2, 'black'), border_radius=22),
            'LEARNING_RATE':TextField(value='5e-5', border=border.all(0.2, 'black'), border_radius=22),
            'WARMUP_PROPORTION':TextField(value='0.1', border=border.all(0.2, 'black'), border_radius=22),
            'MAX_GRAD_NORM':TextField(value='5', border=border.all(0.2, 'black'), border_radius=22),
            'OUTPUT_DIR':TextField(value='/Users/user/Desktop/jarvis/Jarvis/', border=border.all(0.2, 'black'), border_radius=22),
            'MODEL_FILE_NAME':TextField(value='textclass{epoch}.pt', border=border.all(0.2, 'black'), border_radius=22),
            'PATIENCE':TextField(value='2', border=border.all(0.2, 'black'), border_radius=22),
            'CHECKPOINT_PATH':TextField(value='/Users/user/Desktop/jarvis/Jarvis/jarvis_text_classifier/checkpoints/textclass19.pt', border=border.all(0.2, 'black'), border_radius=22, width=600),
            'NUM_LABELS':TextField(value='9', border=border.all(0.2, 'black'), border_radius=22),
            }
    }
    
    def create_settings_start_page():
        values = [val for val in settings_items.get('JarvisMeta').keys()][1:]
        for i in range(settings_items.get('JarvisMeta').get('len')):
            settings_text_column.controls.append(
                Container(
                    content=Row(
                        controls=[
                            Text(values[i]),
                            settings_items.get('JarvisMeta').get(values[i])
                        ]
                    )
                )
            )
    
    def settings_row_first_button_click(e):
        settings_text_column.controls.clear()
        create_settings_start_page()
        page.update()
        
    def settings_row_second_button_click(e):
        settings_text_column.controls.clear()
        values = [val for val in settings_items.get('JTTS').keys()][1:]
        for i in range(settings_items.get('JTTS').get('len')):
            settings_text_column.controls.append(
                Container(
                    content=Row(
                        controls=[
                            Text(values[i]),
                            settings_items.get('JTTS').get(values[i])
                        ]
                    )
                )
            )
        page.update()
    
    def settings_row_third_button_click(e):
        settings_text_column.controls.clear()
        values = [val for val in settings_items.get('JSTT').keys()][1:]
        for i in range(settings_items.get('JSTT').get('len')):
            settings_text_column.controls.append(
                Container(
                    content=Row(
                        controls=[
                            Text(values[i]),
                            settings_items.get('JSTT').get(values[i])
                        ]
                    )
                )
            )
        page.update()
    
    def settings_row_four_button_click(e):
        settings_text_column.controls.clear()
        values = [val for val in settings_items.get('JTC').keys()][1:]
        for i in range(settings_items.get('JTC').get('len')):
            settings_text_column.controls.append(
                Container(
                    content=Row(
                        controls=[
                            Text(values[i]),
                            settings_items.get('JTC').get(values[i])
                        ]
                    )
                )
            )
        page.update()
        
    def settings_row_button_create(num, oc):
        return Container(
            width=120,
            border=border.all(1,'white12'),
            border_radius=15,
            content=TextButton(
                num,
                on_click=oc
            )
        )
    
    def back_to_menu_button_click(e):
        main_row.controls.remove(settings_fon)
        main_row.update()
    
    back_to_menu_button = Container(
        margin=margin.only(right=320),
        content=IconButton(
            icon=Icons.ARROW_BACK_IOS_NEW,
            on_click=back_to_menu_button_click,
        )
    )
    
    settings_row = Container(
        margin=margin.only(top=30),
        content=Row(
            controls=[
                back_to_menu_button,
                settings_row_button_create('JarvisMeta', settings_row_first_button_click),
                settings_row_button_create('JTTS', settings_row_second_button_click),
                settings_row_button_create('JSTT', settings_row_third_button_click),
                settings_row_button_create('JTC', settings_row_four_button_click),
            ]
        )
    )
    
    settings_text_column = Column(scroll='auto')
    
    create_settings_start_page()
    
    settings_text_column_cont = Container(
        width=1100,
        height=640,
        margin=margin.only(left=100, top=40),
        content=settings_text_column
    )
    
    def settings_submit_button_save(e):
        page.update()
    
    settings_submit_button = Container(
        margin=margin.only(left=675, top=35),
        content=ElevatedButton(
            text='Submit', 
            style=ButtonStyle(
                color='white',
                bgcolor='red'
            ),
            width=100, 
            height=40,
            on_click=settings_submit_button_save
        )
    )
    
    settings_column = Column(
        controls=[
            settings_row,
            settings_text_column_cont,
            settings_submit_button
        ]
    )
    
    settings_cont = Container(
        border_radius=15,
        content=settings_column
    )
    
    settings_fon = Container(
        offset=(-1.025,-0.01),
        animate_opacity=animation.Animation(1700, AnimationCurve.EASE_IN_OUT),
        opacity=1,
        padding=padding.only(50, 15, 50, 50),
        width=1500,
        height=916,
        bgcolor=BG,
        content=settings_cont
    )
    
    page.bgcolor = BG
    
    main_row = Row(
        controls=[
            first_wrapper,
            second_wrapper,
            third_wrapper,
        ]
    )
        
    page.add(main_row)
     
    page.window.width = 1500 
    page.window.height = 950
    page.update()
    
    
app(target=main)