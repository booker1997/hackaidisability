
from text_to_speech_utils import *
from input_w_emoji_to_xml import *
import time
import socketio



if __name__=="__main__":
    voice = 'en-US-DavisNeural'
    with socketio.SimpleClient() as sio:
        sio.connect('http://localhost:5000')
        sio.emit('cc_provider_get_socket_ids', {})
        time.sleep(0.1)
        
        caller_id = sio.input_buffer[-1][-1]['callers'][0]
        print(caller_id)
        
        while True:
            
            raw_input = input("write what to display: \n\n")
            if sio.input_buffer[-1][0] == 'text_entry':
                text = sio.input_buffer[-1][1]['message']
                style,intensity,text = parse_input(text)
                phrase= StyledPhrase(style,intensity,text)
                xml_str = xml_builder(voice, [phrase])
                voice_ai = BeMyVoice(xml_str)
                voice_ai.speak()
