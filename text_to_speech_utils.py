'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''
import os
import azure.cognitiveservices.speech as speechsdk
import xml.etree.ElementTree as ET
import difflib
import enum
from typing import List
import dataclasses


class VoiceStyle(enum.Enum):
    ANGRY = 'angry'
    CHEERFUL = 'cheerful'
    SAD = 'sad'

@dataclasses.dataclass
class StyledPhrase:
    phrase: str
    voice_style: VoiceStyle
    intensity: int  # 0.01 - 2

priv_key = open('priv_key.txt', 'r')
priv_key = priv_key.read()
service_region = "eastus"



class TextEmotion(object):
    def __init__(self,text,emotion):
        self.text = text
        self.emotion = emotion
    def get_text(self):
        return self.text
    def get_emotion(self):
        return self.emotion

def xml_builder(voice_name: str, phrases: List[StyledPhrase]):
    express_as_elems = []
    for phrase in phrases:
        express_as_elems = (
            f'<mstts:express-as style="{phrase.voice_style.value}" styledegree="{phrase.style_intensity.value}">'
            f'{phrase.phrase}'
            f'</mstts:express-as>'
        )

    combined_phrases = f''.join(express_as_elems)
    return (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'
        f'<voice name="{voice_name}">\n'
        f'{combined_phrases}'
        f'</voice>\n'
        f'</speak>\n'
    )


def parse_input(raw_input: str):
    if '/a' in raw_input:
        angry_index = raw_input.find('/a')
        mod_str = raw_input[angry_index:angry_index+raw_input[angry_index:].find(' ')]
        mod_str = mod_str.strip()
        mod_str = mod_str[2:]
        try:
            intensity = int(mod_str)
            intensity = min(2.0, max(0.01, intensity))
            return VoiceStyle.ANGRY, intensity, raw_input.replace('/a', '')
        except ValueError:
            return VoiceStyle.ANGRY, 1.0, raw_input.replace('/a', '')
        
    if '/d' in raw_input:
        angry_index = raw_input.find('/d')
        mod_str = raw_input[angry_index:angry_index+raw_input[angry_index:].find(' ')]
        mod_str = mod_str.strip()
        mod_str = mod_str[2:]
        try:
            intensity = int(mod_str)
            intensity = min(2.0, max(0.01, intensity))
            return VoiceStyle.SAD, intensity, raw_input.replace('/d', '')
        except ValueError:
            return VoiceStyle.SAD, 1.0, raw_input.replace('/d', '')
        
    else:
        return VoiceStyle.CHEERFUL, 1.0, raw_input.replace('/d', '')
        



class BeMyVoice(object):
    def __init__(self,xml_string):
        self.xml_string = xml_string
        # self.voice = voice
        # self.speech_types = {"angry":"angry", 'cheerful':'cheerful','calm':'calm','depressed':'depressed','excited':'excited','fearful':'fearful',
        #                 'friendly':'friendly','sad':'sad','serious':'serious','unfriendly':'unfriendly'}
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_config = speechsdk.SpeechConfig(subscription=priv_key, region=service_region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        # The language of the voice that speaks.
        # speech_config.speech_synthesis_voice_name = self.voice
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    def speak(self):
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(self.xml_string).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format('no error'))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

