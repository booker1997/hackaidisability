import azure.cognitiveservices.speech as speechsdk
import keyboard
import sounddevice as sd
import numpy as np
import pyaudio
import wave
import threading
import asyncio
import aiofile
priv_key = open('SPEECH_KEY.txt', 'r')
priv_key = priv_key.read()
service_region = "eastus"

# def callback(indata,frames,time,status):
#     global recording
#     recording = np.append(recording,indata)
# def record():
#     global recording
#     recording = np.array([])
#     with stream:
#         while not keyboard.is_pressed('s'):
#             pass
# stream = sd.InputStream(callback=callback)

class ListenAndWrite(object):
    def __init__(self):
        self.transcript = ''
        self.start_record = True
        self.stop_record = False
        self.n_audios = 0
    async def write_to_wav(self, data):
        async with aiofile.AIOFile(f'output_{self.n_audios}.wav', 'wb') as afp:
            writer = aiofile.Writer(afp)
            await writer(data)
            await afp.fsync()
    def listen_and_write(self):

    # Set up the microphone stream
    
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        # Set up the Azure Speech SDK
        speech_config = speechsdk.SpeechConfig(subscription=priv_key, region=service_region)
        push_stream = speechsdk.audio.PushAudioInputStream()
        audio_input = speechsdk.audio.AudioConfig(stream=push_stream)
        speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "log.txt")
        speech_config.request_word_level_timestamps()
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

        # Set up the WAV file
        # self.wav_file = wave.open(f'output_{self.n_audios}.wav', 'wb')
        # self.wav_file.setnchannels(1)
        # self.wav_file.setsampwidth(mic.get_sample_size(pyaudio.paInt16))
        # self.wav_file.setframerate(16000)

        done = threading.Event()

        # def stop_cb(evt):
        #     """callback that stops continuous recognition upon receiving an event `evt`"""
        #     print('CLOSING on {}'.format(evt))
        #     done.set()

        def recognized(evt):
            print("Recognized: {}".format(evt.result.text))

            recognized_speech_json = evt.result.json
            text = evt.result.text
            # # print(recognized_speech_json)

            # self.wav_file.close()

            # self.n_audios+=1

            # # Open a new WAV file
            # # print('new file made')
            # # self.wav_file = wave.open(f'output_{self.n_audios}.wav', 'wb')
            # # self.wav_file.setnchannels(1)
            # # self.wav_file.setsampwidth(mic.get_sample_size(pyaudio.paInt16))
            # # self.wav_file.setframerate(16000)

            # # Stop the current recognition session
            # speech_recognizer.stop_continuous_recognition()

            # # Start a new recognition session
            # speech_recognizer.start_continuous_recognition()

        speech_recognizer.recognized.connect(recognized)
        # speech_recognizer.session_stopped.connect(stop_cb)
        # speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        print("Start speaking...")
        speech_recognizer.start_continuous_recognition()

        try:
            while True:
                # Read data from the microphone
                data = stream.read(1024)

                # Write the data to the WAV file
                

                # Push the data to the Speech SDK
                push_stream.write(data)

                if keyboard.is_pressed('q'):
                    break
        except KeyboardInterrupt:
            pass
        finally:
            # Stop and close everything
            speech_recognizer.stop_continuous_recognition()
            self.wav_file.close()
            stream.stop_stream()
            stream.close()
            mic.terminate()

        # -------------------



        # Create a recognizer using microphone as audio input.
        # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # # Start continuous speech recognition. 
        # result = speech_recognizer.recognize_once_async().get()

        # # Check the result.
        # if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #     print("Recognized: {}".format(result.text))
        #     print(result)
        #      # Create an AudioDataStream for the recognized speech.
             
        #     result_stream = speechsdk.AudioDataStream(result)
        #     result_stream.detach_input()  # stop any more data from input getting to the stream
        #     save_future = result_stream.save_to_wav_file_async("AudioFromRecognizedKeyword.wav")
        #     print('Saving file...')
        #     save_future.get()
        #     # Save the recognized speech to a .wav file.
        #     stream.save_to_wav_file("output.wav")
        # elif result.reason == speechsdk.ResultReason.NoMatch:
        #     print("No speech could be recognized")
        # elif result.reason == speechsdk.ResultReason.Canceled:
        #     cancellation_details = result.cancellation_details
        #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
        #         print("Error details: {}".format(cancellation_details.error_details))

       


        # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # def recognized(evt):
        #     print("Recognized: {}".format(evt.result.text))
        #     print(evt.result)
        #     # time.sleep(2)  # give some time so the stream is filled
        #     result_stream = speechsdk.audio.AudioDataStream(evt.result)
        #     print('here',result_stream.can_read_data())
        #     # result_stream.detach_input()  # stop any more data from input getting to the stream
        #     result_stream.save_to_wav_file_async("output_audio.wav")
        #     # save_future = result_stream.save_to_wav_file_async("output_audio.wav")
        #     print('Saving file...')
        #     self.stop_record = True
        #     self.transcript += ' ' + evt.result.text

        # speech_recognizer.recognized.connect(recognized)

        # print("Speak into your microphone. Press 's' to stop.")
        # # self.start_record_func()
        
        # speech_recognizer.start_continuous_recognition()

        # # Keep running while 's' is not pressed
        # while not keyboard.is_pressed('s'):
        #     pass
        #     # data = self.stream.read(1024)
        #     # self.frames.append(data)
        #     # if self.stop_record:
        #     #     self.stop_recording()
            

        # # If 's' is pressed, stop the recognition
        # speech_recognizer.stop_continuous_recognition()
        # print(self.transcript)


transcripter = ListenAndWrite()
transcripter.listen_and_write()

