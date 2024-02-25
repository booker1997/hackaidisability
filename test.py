from text_to_speech_utils import *
from input_w_emoji_to_xml import *
import time
import socketio





# xml_str_sample = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
#                 <voice name="en-US-JennyNeural">
#                     <mstts:express-as style="cheerful" styledegree="2">
#                         I have been through a wonderful day!
#                     </mstts:express-as>
#                     <mstts:express-as style="angry" styledegree="2">
#                         But my grandkids were annoying.
#                     </mstts:express-as>
#                 </voice>
#             </speak>'''


chat_txt = 'Hey team! I had a great weekend.'
happy_txt ='My grandkids and I went to the Boston Commons! /e'
sad_text = 'On the other hand, I got food poisoning. /d'

style_chat,intensity_chat,text_chat = parse_input(chat_txt)
style_happy,intensity_happy,text_happy = parse_input(happy_txt)
style_1,intensity_1,text_1 = parse_input(sad_text)
print(style_happy,intensity_happy,text_happy)
phrase_chat = StyledPhrase(style_chat,intensity_chat,text_chat)
phrase_exc = StyledPhrase(style_happy,intensity_happy,text_happy)
phrase_sad = StyledPhrase(style_1,intensity_1,text_1)
voice = 'en-US-DavisNeural' # Guy Jason Davis Tony
xml_str = xml_builder(voice, [phrase_chat,phrase_exc,phrase_sad])
print(xml_str)
# speek_input= [TextEmotion(text_1,'cheerful'),TextEmotion(text_2,'excited')]


voice_ai = BeMyVoice(xml_str)
voice_ai.speak()


# if __name__=="__main__":
#     with socketio.SimpleClient() as sio:
#         sio.connect('http://localhost:5000')
#         sio.emit('cc_provider_get_socket_ids', {})
#         time.sleep(0.1)
        
#         caller_id = sio.input_buffer[-1][-1]['callers'][0]
#         print(caller_id)
        
#         while True:
            
#             raw_input = input("write what to display: \n\n")
#             for ii, caller_id in enumerate(sio.input_buffer[-1][-1]['callers']):
#                 sio.emit('cc_provider', {'id': caller_id, 'message': f'{ii} says: {raw_input}'})