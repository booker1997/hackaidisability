import re
from openai import AzureOpenAI


client = AzureOpenAI(
  azure_endpoint = "https://openai-csailhackdisability2024.openai.azure.com/", 
  api_key="609643279a40447cbb98c2b25d5c602c",  
  api_version="2024-02-15-preview"
)

def convert_xml(text):
    prompt = f'''You will be given a text message with one or more sentences, each sentence can be followed with emoji(s).
    You are asked to first classify each sentence with its emoji(s) into a specific emotion label among the following:
    "angry","cheerful","calm","depressed","excited","fearful","friendly","sad","serious","unfriendly"
    

    And then, transform the text message into xml format as below:
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-JennyNeural">
            <mstts:express-as style="cheerful" styledegree="2">
                That'd be just amazing!
            </mstts:express-as>
            <mstts:express-as style="calm" styledegree="0.01">
                What's next?
            </mstts:express-as>
        </voice>
    </speak>

    You are only allowed to change the style tag, styledegree tag (which indicate the degree of that emotion, from 0 to 2), and text content and leave others the same as in the format. 
    And please disregard emoji in the output.

    The text message:
    {text}

    XML output:

    '''
    
    message_text = [{"role":"system","content":prompt}]

    completion = client.chat.completions.create(
      model="gpt-35-turbo", # model = "deployment_name"
      messages = message_text,
      temperature=0,
      max_tokens=800,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    output = completion.choices[0].message.content
    match = re.search(r'<[\s\S]*>', output)
    return match.group(0)