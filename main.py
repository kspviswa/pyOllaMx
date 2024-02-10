import flet as ft
from flet_core.control_event import ControlEvent
from prompt import firePrompt
from models import retModelOptions
from utils import Avatar, Message


def main(page: ft.Page) -> None:
    page.title = 'pyOllaMx'
    page.theme_mode = 'light'
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = '#C7F9D6'
    page.window_resizable = False

    page.window_height = 880
    page.window_width= 872

    page.theme = ft.theme.Theme(font_family="CabinSketch-Regular")
    page.fonts = {
    "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    "Homemade Apple" : "fonts/HomemadeApple-Regular.ttf",
    "CabinSketch-Bold" : "fonts/CabinSketch-Bold.ttf",
    "CabinSketch-Regular" : "fonts/CabinSketch-Regular.ttf"
    }

    banner_image = ft.Image(src=f"logos/pyollama_1.png",
                      width=125,
                      height=125,
                      fit=ft.ImageFit.CONTAIN,
                      )
    banner_text = ft.Text(value='pyOllaMx', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=30)
    subbanner_text = ft.Text(value='Your gateway to both Ollama & Apple MlX models')
    chat_messages = ft.Column(
                              alignment=ft.MainAxisAlignment.CENTER,
                              horizontal_alignment=ft.CrossAxisAlignment.START,
                              scroll=ft.ScrollMode.ADAPTIVE,
                              height=350,
                              width=700,
                              )
    search_messages = ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            height=350,
                            width=700,
                            )
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Chat",
                icon=ft.icons.CHAT,
                content = chat_messages,
            ),
            ft.Tab(
                text="Search",
                icon=ft.icons.TRAVEL_EXPLORE_OUTLINED,
                content = search_messages
            ),            
        ],
        height=392,
        width=700,
        scrollable=True
    )

    user_text = ft.Text(value='Enter your prompt', style=ft.TextStyle(font_family='CabinSketch-Bold'))
    user_text_field = ft.TextField(multiline=True,
                                   width=675)
    send_button = ft.ElevatedButton("Send", icon=ft.icons.ROCKET_LAUNCH)
    clear_button = ft.ElevatedButton("chats", icon=ft.icons.DELETE_FOREVER, icon_color="pink600")
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
                                  adaptive=True,
                                  label_position=ft.LabelPosition.LEFT)
    temp_label = ft.Text(value='Temperature')
    temp_slider = ft.CupertinoSlider(min=0.0, max=1.0, divisions=10, value=0.3)
    temp_value_label = ft.Text(value=temp_slider.value)
    model_help_text = ft.Text('^Ollama models are loaded by default', style=ft.TextStyle(size=10), text_align=ft.TextAlign.LEFT)

    def open_url(e):
        page.launch_url(e.data)

    def updateChat(message: Message = None, ai_response: bool = False, controlHandle: ft.Column = None):
        if ai_response:
            controlHandle.controls.append(
                ft.Row([
                    ft.Image(src=getAILogo(select_mlX_models.value),
                             width=50,
                             height=50,
                             fit=ft.ImageFit.CONTAIN),
                    ft.Container(content=ft.Markdown(value=message.text, extension_set="gitHubWeb", code_theme='obsidian', code_style=ft.TextStyle(font_family='Roboto Mono'),selectable=True, on_tap_link=open_url, auto_follow_links=True,),
                                 width=550 )
                ],
                width=500, vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        else:
            controlHandle.controls.append(
                ft.Row([
                    ft.Image(src=f"logos/vk_logo.png",
                             width=50,
                             height=50,
                             fit=ft.ImageFit.CONTAIN),
                    ft.Container(content=ft.Text(message.text, selectable=True), width=500)
                ],
                auto_scroll=True,
                width=500
                )
            )
        controlHandle.scroll_to(offset=-1, duration=1000, curve=ft.AnimationCurve.EASE_IN_OUT)
        page.update()

    def getAILogo(isMlx: bool):
        return f'logos/mlx_logo.png' if isMlx else f'logos/pyollama_1.png'

    def show_spinning():
        pr_ph.value='Working...🏃🏻‍♂️⏳'
        pr.value = None
        user_text_field.disabled = True
        send_button.disabled = True
        clear_button.disabled = True
        page.update()
    
    def end_spinning():
        pr_ph.value=""
        pr.value = 0
        user_text_field.disabled = False
        send_button.disabled = False
        clear_button.disabled = False
        page.update()

    def send(e: ControlEvent) -> None:
        prompt = user_text_field.value
        isChat = True if tabs.selected_index == 0 else False
        ctrlHandle = chat_messages if isChat else search_messages
        updateChat(Message(user='user', text=prompt), controlHandle=ctrlHandle, ai_response=False)
        user_text_field.value = ""
        show_spinning()
        isMlx = select_mlX_models.value
        res, keys = firePrompt(prompt=prompt, model=model_dropdown.value, temp=temp_slider.value, isMlx=isMlx, chat_mode=isChat)
        if keys != "":
            res = res + f'\n\n Keywords used for search : {keys} '
        updateChat(Message(user='assistant', text=res), controlHandle=ctrlHandle, ai_response=True)
        end_spinning()
        page.update()
    
    def enableSend(e: ControlEvent) -> None:
        if user_text_field.value != "" and model_dropdown.value != "unselected":
            send_button.disabled = False
            clear_button.disabled = False
            page.update()
    
    def swapModels(e: ControlEvent) -> None:
        if select_mlX_models.value:
            model_dropdown.options = retModelOptions(True)
        else:
            model_dropdown.options = retModelOptions()
        banner_image.src = getAILogo(select_mlX_models.value)
        page.update()
    
    def displayTemp(e: ControlEvent) -> None:
        temp_value_label.value = temp_slider.value
        page.update()
    
    def clear(e: ControlEvent) -> None:
        if tabs.selected_index == 0:
            del chat_messages.controls[:]
        else:
            del search_messages.controls[:]
        page.update()
    

    send_button.on_click = send
    clear_button.on_click = clear
    send_button.disabled = True
    clear_button.disabled = True
    user_text_field.on_change = enableSend
    model_dropdown.on_change = enableSend
    select_mlX_models.on_change = swapModels
    temp_slider.on_change = displayTemp

    top_banner_view = ft.Row([ft.Column([banner_image, banner_text, subbanner_text], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER)

    temp_control_view = ft.Column([
        temp_slider,
        ft.Row([
            temp_label,
            temp_value_label
        ])
    ])

    model_control_view = ft.Row([
        ft.Column([model_dropdown]),
        ft.Column([select_mlX_models, model_help_text], horizontal_alignment=ft.CrossAxisAlignment.START)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    controls_view = ft.Row([
        temp_control_view,
        model_control_view
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    user_input_view = ft.Row([
        ft.Column([
            user_text,
            user_text_field
        ]),
        ft.Column([
            send_button,
            clear_button
        ], alignment=ft.MainAxisAlignment.START),
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(top_banner_view)
    page.add(controls_view)
    #page.add(chat_messages)
    page.add(tabs)
    page.add(ft.Row([pr,pr_ph], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    page.add(user_input_view)


if __name__ == '__main__':
    ft.app(target=main)