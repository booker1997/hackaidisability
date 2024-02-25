import os
import azure.cognitiveservices.speech as speechsdk
import json


def recognize_from_microphone():
    priv_key = open('SPEECH_KEY.txt', 'r')
    priv_key = priv_key.read()
    service_region = "eastus"

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=priv_key, region=service_region)
    speech_config.speech_recognition_language="en-US"
    speech_config.request_word_level_timestamps()

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    done = False
    while not done:
        speech_recognition_result = speech_recognizer.start_continuous_recognition()
        if input() == 1:
            speech_recognizer.stop_continuous_recognition()
            done = True
    
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        print(speech_recognition_result)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

recognize_from_microphone()


