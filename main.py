import flet as ft
from flet_core.control_event import ControlEvent
from prompt import *
from models import *
from utils import Avatar, Message
from model_hub import *
from settings import *
from history import *
import time


def main(page: ft.Page) -> None:
    page.title = 'PyOllaMx'
    page.theme_mode = 'light'
    page.scroll = ft.ScrollMode.ADAPTIVE
    #page.bgcolor = '#C7F9D6'
    page.window.resizable = False

    page.theme = ft.Theme(
        font_family="CabinSketch-Regular",
        color_scheme=ft.ColorScheme(primary='black')
    )
    page.dark_theme = ft.Theme(
        font_family="CabinSketch-Regular",
        color_scheme=ft.ColorScheme(primary='#ffde03')
    )

    page.window.height = 880
    page.window.width= 872

    #page.theme = ft.theme.Theme(font_family="CabinSketch-Regular")
    page.fonts = {
    "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    "Homemade Apple" : "fonts/HomemadeApple-Regular.ttf",
    "CabinSketch-Bold" : "fonts/CabinSketch-Bold.ttf",
    "CabinSketch-Regular" : "fonts/CabinSketch-Regular.ttf"
    }

    #initialize page state
    page.session.set('selected_model', 'N/A')
    page.session.set('selected_temp', 0.0)
    page.session.set('isMlx', False)

    banner_image = ft.Image(src=f"logos/pyollama_1.png",
                      width=75,
                      height=75,
                      fit=ft.ImageFit.CONTAIN,
                      )
    banner_text = ft.Text(value='PyOllaMx', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=30)
    subbanner_text = ft.Text(value='Your gateway to both Ollama & Apple MlX models')
    chat_messages = ft.Column(
                              alignment=ft.MainAxisAlignment.CENTER,
                              horizontal_alignment=ft.CrossAxisAlignment.START,
                              scroll=ft.ScrollMode.ADAPTIVE,
                              height=450,
                              width=695,
                              )
    search_messages = ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            height=450,
                            width=695,
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
        height=488,
        width=700,
        scrollable=True,
    )

    def get_check_color() -> str:
        if page.theme_mode == 'dark' :
            print('dark')
            return 'black'
        else:
            print('light')
            return 'white'
        
    user_text = ft.Text(value='Enter your prompt', style=ft.TextStyle(font_family='CabinSketch-Bold'))
    enable_streaming = ft.CupertinoCheckbox(label='Enable Streaming', value=False, check_color=get_check_color())
    user_text_field = ft.TextField(multiline=True,
                                   width=675, autofocus=True, label='Enter your prompt')
    user_text_field.border_color = 'white' if page.theme_mode == 'dark' else 'black'
    send_button = ft.ElevatedButton("Send", icon=ft.icons.ROCKET_LAUNCH, tooltip='Select a model in the settings menu & type in a prompt to enable this control')
    clear_button = ft.ElevatedButton("chats", icon=ft.icons.DELETE_FOREVER, icon_color="pink600", tooltip='Atleast one response from AI should be available to delete this conversation')
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

    # BottomBar
    selected_model = ft.Text('None', style=ft.TextStyle(size=15))
    selected_temp = ft.Text('N/A', style=ft.TextStyle(size=15))
    selected_model_image = ft.Image(src='logos/combined_logos.png', width=35, height=35)
    bottom_control = ft.Row([
        ft.Text('Model Selected: ', style=ft.TextStyle(size=15)),
        selected_model,
        selected_model_image,
        ft.Text('Temperature: ', style=ft.TextStyle(size=15)),
        selected_temp
    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    bottom_appbar = ft.BottomAppBar(content=bottom_control)

    def open_url(e):
        page.launch_url(e.data)

    def updateChat(message: Message, controlHandle: ft.Column, ai_response: bool = False):
        #print(f'message {message} ai_response {ai_response} controlHandle {controlHandle}')
        if ai_response:
            ai_thinking_text = re.sub(r"</think>.*$", "", message.text, flags=re.DOTALL) if "</think>" in message.text else ""
            ai_non_thinking_text = message.text

            #print(f'### {ai_thinking_text}')
            ai_message_container = ft.Container(width=550)
            ai_message_md = ft.Markdown(value="", extension_set="gitHubWeb", code_theme='obsidian', code_style=ft.TextStyle(font_family='Roboto Mono'), on_tap_link=open_url, auto_follow_links=True)
            ai_message_md_selectable = ft.SelectionArea(content=ai_message_md)
            ai_message_thinking_md = ft.ExpansionTile(
            title=ft.Text("Thinking tokens 🤔", font_family="RobotoSlab"),
            subtitle=ft.Text("Expand to reveal the model's thinking tokens", theme_style=ft.TextThemeStyle.BODY_SMALL, font_family="RobotoSlab"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=False,
            collapsed_text_color=ft.Colors.BLUE,
            text_color=ft.Colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_SMALL,
                    font_family="RobotoSlab",
                )),
            ],
        )
            if ai_thinking_text :
                ai_message_container.content = ft.Column([ai_message_thinking_md,
                                                      ai_message_md_selectable,
                                                      ])
                ai_non_thinking_text = ''.join(message.text.split("</think>")[1:])
            else:
                ai_message_container.content = ai_message_md_selectable

            controlHandle.controls.append(
                ft.Row([
                    ft.Image(src=getAILogo(page.session.get('isMlx')),
                             width=50,
                             height=50,
                             fit=ft.ImageFit.CONTAIN),
                             ai_message_container
                ],
                width=500, vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
            ai_message_thinking_md.controls[0].title.value = ai_thinking_text
            if enable_streaming.value:
                full_r = ""
                for chunk in ai_non_thinking_text.split(sep=" "):
                    full_r += chunk + " "
                    ai_message_md.value = full_r
                    # controlHandle.scroll_to(offset=-1, duration=100, curve=ft.AnimationCurve.EASE_IN_OUT)
                    page.update()
                    time.sleep(0.05)
            else:
                ai_message_md.value = ai_non_thinking_text
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
        #controlHandle.scroll_to(offset=-1, duration=100, curve=ft.AnimationCurve.EASE_IN_OUT)
        page.update()

    def getAILogo(isMlx: bool) -> str:
        return f'logos/mlx_logo.png' if isMlx else f'logos/pyollama_1.png'

    def getBottomBarModelLogo(isMlx: bool) -> str:
        return f'logos/mlx.png' if isMlx else f'logos/ollama.png'

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
        isMlx = page.session.get('isMlx')
        res, keys = firePrompt(prompt=prompt, model=page.session.get('selected_model'), temp=page.session.get('selected_temp'), isMlx=isMlx, chat_mode=isChat)
        if keys != "":
            res = res + f'\n\n Keywords used for search : {keys} '
        updateChat(Message(user='assistant', text=res), controlHandle=ctrlHandle, ai_response=True)
        end_spinning()
        page.update()
    
    def enableSend(e: ControlEvent) -> None:
        if user_text_field.value != "" and page.session.get('selected_model') != "N/A":
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
            clearChatHistory()
        else:
            del search_messages.controls[:]
            clearSearchHistory()
        page.update()
    
    def showModelSettings(e: ControlEvent) -> None:
        page.go('/settings')

    def toggleTheme(e: ControlEvent) -> None:
        icon : ft.IconButton = e.control
        if icon.icon == ft.icons.DARK_MODE_SHARP:
            page.theme_mode = "dark"
            icon.icon = ft.icons.SUNNY
            user_text_field.border_color = 'white'
            enable_streaming.check_color = 'black'
        else: 
            #icon.icon == ft.icons.DARK_MODE_OUTLINED
            page.theme_mode = "light"
            icon.icon = ft.icons.DARK_MODE_SHARP
            user_text_field.border_color = 'dark'
            enable_streaming.check_color = 'white'
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    def showModelHub(e: ControlEvent):
        page.go('/model_hub')
    
    def showHistory(e: ControlEvent):
        page.go('/history')


    send_button.on_click = send
    clear_button.on_click = clear
    send_button.disabled = True
    clear_button.disabled = True
    user_text_field.on_change = enableSend
    model_dropdown.on_change = enableSend
    select_mlX_models.on_change = swapModels
    temp_slider.on_change = displayTemp

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
            enable_streaming,
            user_text_field
        ],alignment=ft.MainAxisAlignment.SPACE_AROUND, horizontal_alignment=ft.CrossAxisAlignment.END),
        ft.Column([
            send_button,
            clear_button
        ], alignment=ft.MainAxisAlignment.START),
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_AROUND)
    
    top_banner_view = ft.Row([
        ft.IconButton(ft.icons.SETTINGS, on_click=showModelSettings, tooltip='Expand Model Settings'),
        ft.Container(),
        ft.Row([ft.Column([ft.Row([banner_image, banner_text]), subbanner_text], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.IconButton(ft.icons.DARK_MODE_SHARP, on_click=toggleTheme, tooltip='Toggle Dark Mode'),
            ft.IconButton(ft.icons.INSTALL_DESKTOP, on_click=showModelHub, tooltip='Download Models'),
            ft.IconButton(ft.icons.HISTORY, on_click=showHistory, tooltip='Conversation History'),
            #ft.PopupMenuButton()
        ], alignment="spacearound"),
    ], alignment="spacebetween")

    spinner_view = ft.Row([pr,pr_ph], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()
        page.views.append(
            ft.View(
                route = "/",
                controls=[
                    top_banner_view,
                    #controls_view,
                    tabs,
                    spinner_view,
                    user_input_view,
                    #enable_streaming,
                ],
                auto_scroll=True,
                scroll=ft.ScrollMode.ADAPTIVE,
                bottom_appbar=bottom_appbar,
            )
        )

        if page.route == "/":
            selected_model.value = page.session.get('selected_model')
            selected_temp.value = page.session.get('selected_temp')
            selected_model_image.src = getBottomBarModelLogo(page.session.get('isMlx'))
            banner_image.src = getAILogo(page.session.get('isMlx'))


        if page.route == "/settings":
            page.views.append(settingsView(page))

        if page.route == "/model_hub":
            page.views.append(modelHubView(page.theme_mode))
        
        if page.route == "/history":
            page.views.append(historyView(page.theme_mode))

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    #page.overlay.append(controls_bottom_sheet)
    page.go(page.route)

    #page.add(top_banner_view)
    #page.add(controls_view)
    #page.add(chat_messages)
    #page.add(tabs)
    #page.add(spinner_view)
    #page.add(user_input_view)


if __name__ == '__main__':
    ft.app(target=main)