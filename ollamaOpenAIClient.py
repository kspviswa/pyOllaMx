from openai import OpenAI
from typing import List

class OllamaOpenAPIClient():

    def __init__(self):
        self.messages = []
        self.client = OpenAI(base_url='http://127.0.0.1:11434/v1', api_key='pyomlx')
    
    def clear_history(self):
        self.messages.clear()
    
    def append_history(self, message):
        self.messages.append(message)
    
    def chat(self, prompt:str, model: str, temp: float, system:str = 'default') -> str:
        message = {}
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        try:
            response = self.client.chat.completions.create(model=model, 
                                          messages=self.messages)
            response = response.choices[0].message.content
        except Exception as e:
            raise ValueError(e)
        ai_message = dict({'role' : 'assistant', 'content' : response})
        self.messages.append(ai_message)
        return response

    def chat_stream(self, prompt:str, model: str, temp: float) -> str:
        pass

    def list(self) -> List[str]:
        response = self.client.models.list()
        models = []
        for m in response:
            models.append(m.id)
        return models


if __name__ == '__main__':
    print(OllamaOpenAPIClient().list())