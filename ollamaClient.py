from ollama import chat

class OllamaClient():

    def __init__(self):
        self.messages = []
    
    def clear_history(self):
        self.messages.clear()
    
    def append_history(self, message):
        self.messages.append(message)
    
    def chat(self, prompt:str, model: str, temp: float, system:str = "default") -> str:
        options = dict({'temperature' : temp})
        message = {}
        if system != 'default':
            sMessage = dict({'role' : 'system', 'content' : system})
            self.messages.append(sMessage)
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        response = chat(model=model, messages=self.messages, options=options)
        self.messages.append(response['message'])
        return response['message']['content']

    def chat_stream(self, prompt:str, model: str, temp: float) -> str:
        message = {}
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        stream = chat(model=model, messages=self.messages, options={'temperature' : temp}, stream=True)
        return stream


if __name__ == '__main__':
    client = OllamaClient()
    while True:
        print('You :')
        response = client.chat_stream(model='dolphin-mistral:latest', temp=0.8, prompt=input())
        contents = ""
        AiMessage = {}
        for chunk in response:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            contents += content
        AiMessage['role'] = 'assistant'
        AiMessage['content'] = contents
        client.append_history(AiMessage)