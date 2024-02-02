import flet as ft
from flet_core.control_event import ControlEvent
from prompt import firePrompt
from models import retModelOptions
from utils import Avatar, Message


def main(page: ft.Page) -> None:
    page.title = 'pyOllama'
    page.theme_mode = 'light'
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = '#C7F9D6'
    page.window_max_height = 600
    page.window_max_width= 800
    page.window_min_height = 600
    page.window_min_width= 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.theme.Theme(font_family="CabinSketch-Regular")
    page.fonts = {
    "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    "Homemade Apple" : "fonts/HomemadeApple-Regular.ttf",
    "CabinSketch-Bold" : "fonts/CabinSketch-Bold.ttf",
    "CabinSketch-Regular" : "fonts/CabinSketch-Regular.ttf"
    }
    page.appbar = ft.AppBar(
        title=ft.Text("pyOllama"),
        center_title=True,
        bgcolor='#C7F9D6',
    )
    chat_messages = ft.Column(
                              alignment=ft.MainAxisAlignment.CENTER,
                              tight=True,
                              wrap=True
                              )
    user_text = ft.Text(value='Enter your prompt', style=ft.TextStyle(font_family='CabinSketch-Bold'))
    user_text_field = ft.TextField(multiline=True,
                                   width=200,
                                   expand=True)
    send_button = ft.ElevatedButton(text="Send")
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
    pr.value = 0
    pr_ph = ft.Text()
    model_dropdown = ft.Dropdown(
        label = "Load a model^",
        hint_text= "Choose from available models",
        options = retModelOptions(),
        value = "unselected",
        dense=True,
        focused_bgcolor='pink',
    )
    select_mlX_models = ft.Switch(label='Load 🖥️ mlX models from HF',
                                  value=False,
                                  adaptive=True)
    temp_label = ft.Text(value='Temperature')
    temp_slider = ft.CupertinoSlider(min=0.0, max=1.0, divisions=10, value=0.3)
    temp_value_label = ft.Text(value=temp_slider.value)

    def updateChat(message: Message, ai_response: bool = False):
        if ai_response:
            chat_messages.controls.append(
                ft.Row([
                    ft.Image(src=f"logos/pyollama_1.png",
                             width=50,
                             height=50,
                             fit=ft.ImageFit.CONTAIN),
                    ft.Container(content=ft.Markdown(value=message.text, extension_set="gitHubWeb", code_theme='obsidian', code_style=ft.TextStyle(font_family='Roboto Mono'),selectable=True),
                                 width=550)
                ],
                
                width=500
                )
            )
        else:
            chat_messages.controls.append(
                ft.Row([
                    ft.Image(src=f"logos/vk_logo.png",
                             width=50,
                             height=50,
                             fit=ft.ImageFit.CONTAIN),
                    ft.Text(message.text)
                ],
                auto_scroll=True,
                width=500
                )
            )
        page.update()


    def show_spinning():
        pr_ph.value='Thinking... 💭💭💭'
        pr.value = None
        user_text_field.disabled = True
        page.update()
    
    def end_spinning():
        pr_ph.value=""
        pr.value = 0
        user_text_field.disabled = False
        page.update()

    def send(e: ControlEvent) -> None:
        print('prompting...')
        prompt = user_text_field.value
        updateChat(Message(user='user', text=prompt))
        user_text_field.value = ""
        show_spinning()
        isMlx = select_mlX_models.value
        res = firePrompt(prompt=prompt, model=model_dropdown.value, temp=temp_slider.value, isMlx=isMlx)
        updateChat(Message(user='assistant', text=res), ai_response=True)
        end_spinning()
        page.update()
    
    def enableSend(e: ControlEvent) -> None:
        if user_text_field.value != "" and model_dropdown.value != "unselected":
            send_button.disabled = False
            page.update()
    
    def swapModels(e: ControlEvent) -> None:
        if select_mlX_models.value:
            model_dropdown.options = retModelOptions(True)
        else:
            model_dropdown.options = retModelOptions()
        page.update()
    
    def displayTemp(e: ControlEvent) -> None:
        temp_value_label.value = temp_slider.value
        page.update()

    send_button.on_click = send
    send_button.disabled = True
    user_text_field.on_change = enableSend
    model_dropdown.on_change = enableSend
    select_mlX_models.on_change = swapModels
    temp_slider.on_change = displayTemp
    page.add(ft.Row([ft.Image(src=f"logos/pyollama_1.png",
                      width=150,
                      height=150,
                      fit=ft.ImageFit.CONTAIN,
                      )],
                      alignment=ft.MainAxisAlignment.CENTER))
    page.add(chat_messages)
    page.add(ft.Row([
        user_text,
        ft.Row([temp_slider, temp_label, temp_value_label]
        ),
    ]))
    page.add(ft.Row([
        user_text_field,
        send_button,
    ]))
    page.add(ft.Row([
        model_dropdown,
        ft.Column([
            select_mlX_models,
            ft.Text('^Ollama models are loaded by default', style=ft.TextStyle(size=14), text_align=ft.TextAlign.RIGHT),
        ]),
    ],
    ))
    page.add(ft.Column([pr,pr_ph]))
    print(f'Window  width {page.width}')
    print(f'Window  height {page.height}')



if __name__ == '__main__':
    ft.app(target=main)