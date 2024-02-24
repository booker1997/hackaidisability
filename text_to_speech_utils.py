'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''
import os
import azure.cognitiveservices.speech as speechsdk
import xml.etree.ElementTree as ET
import difflib
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

