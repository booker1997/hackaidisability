'''
torch == 2.1.0+cu121
torchaudio == 2.1.0+cu121
transformers == 4.37.2
librosa == 0.10.1
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor, AutoModelForAudioClassification
import librosa
import IPython.display as ipd
import numpy as np
import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name_or_path = "harshit345/xlsr-wav2vec-speech-emotion-recognition"
config = AutoConfig.from_pretrained(model_name_or_path)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name_or_path)
sampling_rate = feature_extractor.sampling_rate
model = AutoModelForAudioClassification.from_pretrained(model_name_or_path).to(device)

def speech_file_to_array_fn(path, sampling_rate):
    speech_array, _sampling_rate = torchaudio.load(path)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech = resampler(speech_array).squeeze().numpy()
    return speech
def predict(path, sampling_rate):
    '''
    Output format:
    [{'Emotion': 'anger', 'Score': '19.3%'},
     {'Emotion': 'disgust', 'Score': '22.3%'},
     {'Emotion': 'fear', 'Score': '19.9%'},
     {'Emotion': 'happiness', 'Score': '18.2%'},
     {'Emotion': 'sadness', 'Score': '20.2%'}]
    '''
    speech = speech_file_to_array_fn(path, sampling_rate)
    inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    inputs = {key: inputs[key].to(device) for key in inputs}
    with torch.no_grad():
        logits = model(**inputs).logits
    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{"Emotion": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
    return outputs

