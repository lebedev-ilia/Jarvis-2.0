import librosa
import os
import numpy as np
from scipy.io.wavfile import write
import pandas as pd
from torch.utils.data import Dataset
from tqdm import tqdm
from typing import List
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import nemo.collections.asr as nemo_asr
from silero_vad import load_silero_vad
from TTS.api import TTS
import sounddevice as sd


class JarvisTTSDataset(Dataset):
    def __init__(self, datapath, train, ratio: List):
        
        self.datapath = datapath
        self.data = pd.read_csv(os.path.join(self.datapath, 'jarvis_dataset/metadata.csv'))
        self.ratio = ratio
        self.train = train
        
        self.dataset = []
        
        if train:
            train_len = round(len(self.data['path']) / 100 * self.ratio[0])
            tqdm_train_len = tqdm(range(train_len), leave=True)
        else:
            train_len = round(len(self.data['path']) / 100 * self.ratio[1])
            tqdm_train_len = tqdm(range(train_len), leave=True)
        for i in tqdm_train_len:
            path = os.path.join(self.datapath, self.data.loc[i]['path'])
            audio = self.wav_unnorm(path)
            self.dataset.append([audio, self.data.loc[i]['sentence']])
            
    
    def __getitem__(self, index):
        print(index)
        audio = self.dataset[index][0]
        sentence = self.dataset[index][1]
        return sentence, audio
    
    def __len__(self):
        if self.train:
            return round(len(self.data['path']) / 100 * self.ratio[0])
        else:
            return round(len(self.data['path']) / 100 * self.ratio[1])
    
    def wav_unnorm(self, path):
        aud, sr = librosa.load(path)
        aud = (aud * 91398).astype(np.float32)
        aud = aud / (32767 / 0.71)
        return aud
    

class ConversionJarvisVoice():
    def __init__(self, path, output):
        self.path = path
        self.output = output
        
    def get_index(self, array, qq):
        lenn = array.shape[0]
        indexes = []
        if qq == 'add':
            add_val = []
            for i in range(lenn):
                if i % 8 == 0:
                    indexes.append(i)
                    add_val.append(array[i])
            return np.array(add_val), np.array(indexes)
        else:
            for i in range(lenn):
                if i % 11 == 0:
                    indexes.append(i)
            return np.array(indexes)

    def conversion_for_index(self, audio: np.ndarray, converion_index: np.ndarray, append_values: np.ndarray, converions_mode: str = ['del', 'add']):
        if converions_mode == 'del':
            conersion_audio = np.delete(audio, converion_index)
        elif converions_mode == 'add':
            conersion_audio = np.insert(audio, converion_index, append_values)
        return conersion_audio


    def create_audio(self, start: int = 1, lenn: int = None, conversion_mode: str = ['add','del'], log: bool = False, file_name: str = None):
        path = os.path.join(self.path, file_name)
        if log:
            for i in range(1, lenn):
                audio, sr = librosa.load(f'{path}_{i+1}_out.wav')
                add_val, indx = self.get_index(audio, conversion_mode)
                converion_audio = self.do_for_index(audio, indx, add_val, conversion_mode)
                write(f"jar{i+self.start}_out.wav", sr, converion_audio)
                self.start += 1
        else:
            for i in range(1, lenn):
                audio, sr = librosa.load(f'/Users/user/Desktop/jarvis/Jarvis/jarvis_dataset/data/jar{i+1}_out.wav')
                add_val, indx = self.get_index(audio, conversion_mode)
                converion_audio = self.do_for_index(audio, indx, add_val, conversion_mode)
                write(f"jar{i+start}_out.wav", sr, converion_audio)
                start += 1
    

def normalaize_signal(data: List) -> torch.FloatTensor:
    r = np.concatenate(data, axis=None)
    r = (1 - (-1))/(np.max(r)-np.min(r))*(r - np.max(r))+1
    r = torch.FloatTensor(r)
    return r

def load_ready_model(model_name, config = None):
    
    if model_name == 'JTC':
        checkpoint = torch.load(config.CHECKPOINT_PATH)
        BERT_MODEL = config.BERT_MODEL
        tokenizer = BertTokenizer.from_pretrained(BERT_MODEL)
        model = BertForSequenceClassification.from_pretrained(BERT_MODEL, num_labels = config.NUM_LABELS)
        model.load_state_dict(checkpoint)
        return model, tokenizer
    
    elif model_name == 'JSTT':
        model = nemo_asr.models.ASRModel.from_pretrained(model_name=config.MODEL_NAME)
        return model
    
    elif model_name == 'JVAD':
        model = load_silero_vad()
        return model
    
    elif model_name == 'JTTS':
        model = TTS(config.MODEL_NAME, gpu=config.USE_GPU, progress_bar=False)
        return model

def play_infer(model, text, sr=24000):
    wav = model.tts(text, speaker_wav='/Users/user/Desktop/jarvis/Jarvis/jarvis_tts_dataset/data/jar49_out.wav', language='ru')
    wav = np.array(wav)
    wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
    wav_norm = wav_norm.astype(np.int16)

    sd.play(wav_norm, sr)
    sd.wait()

def tts_debug(debug_mode, text = None, tts_model = None):
    if debug_mode == 'print':
        print(text)
    else:
        play_infer(tts_model, text)

def remove_jarvis_from_transcribe(transcribe: str) -> str:
    
    if 'Джарвис ' in transcribe:
        
        transcribe = transcribe.replace('Джарвис ', '')
    
    elif 'джарвис ' in transcribe:
        
        transcribe = transcribe.replace('джарвис ', '')
    
    elif 'Джарвис, ' in transcribe:
        
        transcribe = transcribe.replace('Джарвис', '')
    
    elif ', Джарвис, ' in transcribe:
        
        transcribe = transcribe.replace(', Джарвис, ', ' ')
    
    elif ', Джарвис ' in transcribe:
        
        transcribe = transcribe.replace('Джарвис', ' ')
        
    else:
        
        return transcribe, False
    
    return transcribe, True

