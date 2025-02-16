import flet as ft
from models import *

PYOLLAMX_VERSION = '0.0.5'

def clearState(e: ft.ControlEvent) -> None:
    model_dropdown.value = "N/A"
    e.page.session.set('selected_model', 'N/A')
    e.page.session.set('isMlx', False)
    e.page.session.set('selected_temp', 0)    

def updateIsMlxInfo(e: ft.ControlEvent) -> None:
    clearState(e)
    if select_mlX_models.value:
        model_dropdown.options = retModelOptions(True)
    else:
        model_dropdown.options = retModelOptions()
    saveState(e)
    e.page.update()

def saveState(e: ft.ControlEvent) -> None:
    e.page.session.set('selected_model', model_dropdown.value)
    e.page.session.set('isMlx', select_mlX_models.value)
    e.page.session.set('selected_temp', temp_slider.value)

def updateTempInfo(e: ft.ControlEvent) -> None:
    temp_value_label.value = temp_slider.value
    saveState(e)
    e.page.update()

def updateModelInfo(e: ft.ControlEvent) -> None:
    saveState(e)

model_dropdown = ft.Dropdown(
    label = "Load a model^",
    hint_text= "Choose from available models",
    options = retModelOptions(),
    value = "unselected",
    dense=True,
)

select_mlX_models = ft.Switch(label='Load 🖥️ mlX models from HF',
                                value=False,
                                adaptive=True,
                                label_position=ft.LabelPosition.LEFT)
temp_label = ft.Text(value='Temperature')
temp_slider = ft.CupertinoSlider(min=0.0, max=1.0, divisions=10, value=0.3)
temp_value_label = ft.Text(value=temp_slider.value)
model_help_text = ft.Text('^Ollama models are loaded by default', style=ft.TextStyle(size=10), text_align=ft.TextAlign.LEFT)

model_control_view = ft.Row([
    ft.Column([model_dropdown]),
    ft.Column([select_mlX_models, model_help_text], horizontal_alignment=ft.CrossAxisAlignment.START)
], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

temp_control_view = ft.Column([
    temp_slider,
    ft.Row([
        temp_label,
        temp_value_label
    ])
])

controls_view = ft.Row([
    temp_control_view,
    model_control_view
], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

select_mlX_models.on_change = updateIsMlxInfo
model_dropdown.on_change = updateModelInfo
temp_slider.on_change = updateTempInfo

settings_banner_text = ft.Text(value='PyOllaMx Settings', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=30)
settings_banner_image = ft.Image(src=f"logos/combined_logos.png",
                      width=75,
                      height=75,
                      fit=ft.ImageFit.CONTAIN,
                      )
settings_pyollmx_version_text = ft.Text(value=f'v{PYOLLAMX_VERSION}', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=10)

settings_banner_view = ft.Row([
    settings_banner_image,
    settings_banner_text,
    settings_pyollmx_version_text
], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

def display_model_warning_if_needed(page: ft.Page):
    if len(model_dropdown.options) < 1:

        def handle_close(e):
            page.close(dlg_modal)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Unable to get model information"),
            content=ft.Text("Please check if Ollama / PyOMlx is running. If not, restart Ollama / PyOMlx and restart PyOllaMx as well."),
            actions=[
                ft.TextButton("OK", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dlg_modal)

def settingsView(page: ft.Page) -> ft.View:
    display_model_warning_if_needed(page)
    return ft.View(
        "/settings",
        controls = [
            ft.AppBar(title=""),
            settings_banner_view,
            controls_view
        ]
    )