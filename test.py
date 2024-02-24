from text_to_speech_utils import *
from input_w_emoji_to_xml import *


xml_str_sample = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
                <voice name="en-US-JennyNeural">
                    <mstts:express-as style="cheerful" styledegree="2">
                        I have been through a wonderful day!
                    </mstts:express-as>
                    <mstts:express-as style="angry" styledegree="2">
                        But my grandkids were annoying.
                    </mstts:express-as>
                </voice>
            </speak>'''
text = 'Hey team! 😆 I had a great weekend. 💯 We went to the park! 😆 On the other hand, my dog died.😭'
xml_str = convert_xml(text)
print(xml_str)
# speek_input= [TextEmotion(text_1,'cheerful'),TextEmotion(text_2,'excited')]


voice_ai = BeMyVoice(xml_str)
voice_ai.speak()