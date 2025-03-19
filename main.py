from utils import normalaize_signal, load_ready_model, remove_jarvis_from_transcribe
from jarvis_text_classifier.utils import convert_example_to_input_infer
from configs import JSTT_config, JTC_config
from classes import classes
import numpy as np
import pyaudio
import logging
import torch
import g4f
import os

logging.getLogger('nemo_logger').setLevel(logging.ERROR)
logging.getLogger('nemo_logging').setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
os.environ['CURL_CA_BUNDLE'] = JSTT_config.os_environ

JSTT_config = JSTT_config()
JTC_config = JTC_config()

streaming_voice = []
stop_voice = None
stop_voice_cnt = 0
data_fr = []
stop_streaming = None
start = None
wait = 0
chatgpt = None
gpt_context = []
search_google = None

asr_model = load_ready_model('JSTT', JSTT_config)
vad_model = load_ready_model('JVAD')
tc_model, tokenizer = load_ready_model('JTC', JTC_config)
client = g4f.client.Client()

audio = pyaudio.PyAudio()

def stream_callback(input_data, frame_count, time_info, flags):
  global data_fr, stop_streaming, stop_voice_cnt, stop_voice, streaming_voice, JSTT_config
  data = torch.tensor(np.fromstring(input_data, dtype=np.int16))
  speech_prob = vad_model(data, JSTT_config.RATE).item()
  sp = round(speech_prob, 3)
  data_fr.append(data)
  if len(streaming_voice) > 100 and stop_voice == None:
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
    elif sp > 0.71:
      stop_voice_cnt = 0
  elif sp >= 0.71:
    print('Heard!')
    stop_voice = True
    streaming_voice.append(sp)
  return input_data, pyaudio.paContinue

stream = audio.open(format=JSTT_config.FORMAT, channels=JSTT_config.CHANNELS,rate=JSTT_config.RATE, input=True, input_device_index=0, stream_callback=stream_callback,frames_per_buffer=JSTT_config.CHUNK)
    
with torch.no_grad():

    while True:

        print('Start voice!')
        
        if start:
            
            stream.start_stream()
        
        while stream.is_active:
            if stop_streaming:
                print("Yes")
                stream.stop_stream()
                stop_streaming = None
                break

        data = normalaize_signal(data_fr)
        data_fr = []
        start = True
        
        transcribe = ((asr_model.transcribe(data))[0][0]).lower()
        
        print(transcribe)
        
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
                
                inputs = convert_example_to_input_infer(transcribe, JTC_config.MAX_SEQ_LENGTH, tokenizer)
                outputs = tc_model(inputs.input_ids, attention_mask=inputs.input_mask, token_type_ids=inputs.segment_ids)
                
                if torch.max(outputs.logits[0]) > 6.4:
                    pred_class = ((torch.argmax(outputs.logits[0])).numpy() + 1)
                else:
                    continue

                func = classes.get(pred_class)
                
                if search_google and pred_class != 5:
                    
                    search_google = None

                if pred_class == 3:
                    
                    if len(gpt_context) > 15:
                        
                        gpt_context.pop(0)
                        gpt_context.pop(1)
                    
                    gpt_context.append({'user':transcribe})
                    gpt_context.append(func(transcribe, client))
                    
                elif pred_class == 4:
                    
                    title = transcribe[transcribe.index('заголовок')+10:transcribe.index('текст')-1]
                    text = transcribe[transcribe.index('текст')+6:]
                    
                    func(title, text)
                    
                elif pred_class == 5:
                
                    func(gpt_context)
                    
                    gpt_context = []
                    
                elif pred_class == 6:
                    
                    transcribe = transcribe[transcribe.index('загугли')+8:]
                    
                    if search_google:
                        
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
                        
                        for key in nums_res.keys():
                            if key in transcribe:
                                num = nums_res.get(key)
                                break
                        
                        func(text=None, num=num, gen=search_google)
                    
                    else:
                        
                        search_google = func(transcribe, num=1, gen=None)
                
                else:
                    
                    if isinstance(func, tuple):
                        
                        func[0](func[1])
                        
                    else:
                        
                        func()


                

                

