import requests
import json

class MlxClient():

    def __init__(self):
        self.messages = []
        self.llmHost = 'http://127.0.0.1:5000/serve'
    
    def clear_history(self):
        self.messages.clear()
    
    def append_history(self, message):
        self.messages.append(message)
    
    def chat(self, prompt:str, model: str, temp: float, system:str = 'default') -> str:
        message = {}
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        data = {'model': model, 'prompt': prompt, 'temp' : temp}
        try:
            response = requests.post(self.llmHost, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            # print(f'response code {response.status_code}')
            if response.status_code != 200:
                raise requests.ConnectionError
        except Exception as e:
            raise requests.ConnectionError
        ai_message = dict({'role' : 'assistant', 'content' : response.text})
        self.messages.append(ai_message)
        return response.text

    def chat_stream(self, prompt:str, model: str, temp: float) -> str:
        pass