import requests  
import json  
import os 
from dotenv import load_dotenv
from audio_utils import convert_to_wav 

load_dotenv()

class ClovaSpeechClient:
    def __init__(self):
        self.invoke_url = os.getenv('INVOKE_URL')  
        self.secret = os.getenv('SECRET_KEY')  

    
    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'enko',  
            'completion': completion,  
            'callback': callback,  
            'userdata': userdata, 
            'wordAlignment': wordAlignment,  
            'fullText': fullText,  
            'forbiddens': forbiddens, 
            'boostings': boostings, 
            'diarization': diarization,  
            'sed': sed,  
        }
        headers = {
            'Accept': 'application/json;UTF-8',  
            'X-CLOVASPEECH-API-KEY': self.secret  
        }
        files = {
            'media': (file, open(file, 'rb'), 'audio/ogg'),  
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')  # 요청 바디
        }
        
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response
