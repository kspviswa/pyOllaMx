import flet as ft

class Avatar(ft.UserControl):
    def __init__(self, type:str ='assistant'):
        super().__init__()
        self.image = 'logos/pyollama_2.jpeg' if type == 'assistant' else 'logos/vk_logo.pngs'
        self.ctrl = ft.CircleAvatar(foreground_image_url=self.image)
    
    def build(self):
        return self.ctrl

class Message():
    def __init__(self, user: str, text: str):
        self.user = user
        self.text = text
