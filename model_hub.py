import flet as ft
from ollama import list
from ollama import pull
from ollama import delete
from ollama import ProgressResponse
from time import sleep

model_hub_view = ft.View()

settings_banner_text = ft.Text(value='Download Models', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=30)
settings_banner_image = ft.Image(src=f"logos/combined_logos.png",
                      width=75,
                      height=75,
                      fit=ft.ImageFit.CONTAIN,
                      )

settings_banner_view = ft.Row([
    settings_banner_image,
    settings_banner_text
], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

coming_soon_view = ft.Column([
    ft.Text(value='Coming Soon!', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=50)
], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

ollama_download_text = ft.Markdown(' 💡 Refer [Ollama Model Library](https://ollama.com/library) to copy the model name', auto_follow_links=True)
ollama_download_help_text = ft.Markdown(' 💡 Just paste the model name, PyOllaMx will perform `ollama pull <model name>` for you 😎', auto_follow_links=True)

dlg = ft.AlertDialog()

def display_alert(e):
    e.page.dialog = dlg
    dlg.title = ollama_download_help_text
    dlg.open = True
    e.page.update()

def useModel(e: ft.ControlEvent):
    e.page.session.set('selected_model', e.control.key)
    e.page.dialog = dlg
    dlg.title = 'Done'
    dlg.open = True
    e.page.update()

def use_this_model(e):
    print(f'Used Model is {e.control.key}')
    e.page.dialog = dlg
    dlg.title = 'Done'
    dlg.open = True
    e.page.update()
        
def delete_this_model(e):
    delete(e.control.key)
    ollama_models_table.rows = generate_model_rows(list())
    e.page.update()


def generate_model_rows(rawData: dict):
    total_models = rawData['models']
    data = {}
    rows=[]
    for model in total_models:
        data[model['name']] = model['details']['parameter_size']

    for k,v in data.items():
        rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(k)),
            ft.DataCell(ft.Text(v)),
            ft.DataCell(ft.IconButton(
                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                    icon_color="pink600",
                    icon_size=20,
                    tooltip="Delete this model",
                    key=k,
                    on_click=delete_this_model
                ))
        ]))
    return rows

ollama_models_table = ft.DataTable(
        border_radius=10,
        sort_column_index=0,
        sort_ascending=True,
        heading_text_style=ft.TextStyle(font_family='CabinSketch-Bold', size=15),
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=True,
        divider_thickness=0,
        columns=[
        ft.DataColumn(ft.Text('Model Name')),
        ft.DataColumn(ft.Text('Parameters Size')),
        ft.DataColumn(ft.Text('')),
    ])

ollama_models_table.rows = generate_model_rows(list())

ollama_download_hint_button = ft.TextButton("more info", icon="info", on_click=display_alert)
ollama_spacer_text = ft.Text('')
ollama_download_textField = ft.TextField(width=500, height=50, label='Enter model name eg mistral:7b', expand=True)
ollama_download_pbar = ft.ProgressBar(bar_height=20, color="green")
ollama_download_pbar_text = ft.Text(max_lines=2)
ollama_download_pbar.visible = False
ollama_download_pbar_text.visible = False
restart_required_container = ft.Text('Restart PyOllaMx to reload new models', size=15, bgcolor=ft.colors.RED_400, color=ft.colors.YELLOW_ACCENT)
restart_required_container.visible = False

def return_pb_value(total, current):
    if total == 0 or current == 0:
        return 0.0
    if total == current:
        return 1.0
    return (round((current / total), 2))

def download_from_ollama(e: ft.ControlEvent):
    ollama_download_pbar.visible = True
    ollama_download_pbar_text.visible = True
    model_name = ollama_download_textField.value
    ollama_download_pbar_text.value = f'Contacting Ollama Library to pull {model_name} ⏳ .....'
    e.page.update()
    try:
        status = pull(model=model_name,stream=True)
        for s in status:
            #print(f"S is {s}")
            if 'total' in s and 'completed' in s:
                #print("### Inside If")
                ollama_download_pbar_text.value = s['status']
                ollama_download_pbar.value = return_pb_value(float(s['total']), float(s['completed']))
                e.page.update()
                #print(f"ollama_download_pbar_text {ollama_download_pbar_text.value}")
                #print(f"ollama_download_pbar {ollama_download_pbar.value}")
            if s['status'] == 'success':
                ollama_download_pbar_text.value = f'Pulled {model_name} ✅ . Model list Refreshed ✅'
                ollama_download_pbar.value = 1.0
                ollama_models_table.rows = generate_model_rows(list())
                restart_required_container.visible = True
                e.page.update()
    except:
        ollama_download_pbar.value = 1.0
        ollama_download_pbar_text.value = f'🚨 Error occured while pulling {model_name}. Double check model name or whether Ollama 🦙 is running 💡'
        e.page.update()


    

ollama_download_button = ft.IconButton(ft.icons.DOWNLOAD_FOR_OFFLINE_ROUNDED,
                                       icon_color="green600",
                                       icon_size=60,
                                       tooltip="Download Models",
                                       on_click=download_from_ollama)
ollama_available_models_text = ft.Text('Downladed models')
ollama_models_list = ft.Column()

mlx_download_text = ft.Text('Download MlX Model from 🤗')
mlx_download_textField = ft.TextField(width=500, height=50)
mlx_download_button = ft.IconButton(ft.icons.DOWNLOAD)

ollama_control = ft.Column([
        ft.Row([
            ollama_download_text,
            ollama_download_hint_button
        ]),
        ft.Row([
            ollama_download_textField,
            ollama_download_button,
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    ollama_download_pbar_text,
    ollama_download_pbar,
    restart_required_container,
    ft.Column([
        ollama_models_table
    ], scroll=ft.ScrollMode.ADAPTIVE, height=350),
],alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=10)

coming_soon_view = ft.Column([
    ft.Text(value='Coming Soon!', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=50)
], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

mlx_control = ft.Column([
        mlx_download_text,
        ft.Row([
            mlx_download_textField,
            mlx_download_button,
    ]),
], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)


model_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Ollama Models 🦙",
                content = ollama_control,
            ),
            ft.Tab(
                text="Mlx Models 🤗",
                content = coming_soon_view
            ),            
        ],
        height=490,
        width=700,
        scrollable=True,
    )

def modelHubView(theme: str) -> ft.View:
    if theme == 'dark':
        ollama_download_textField.border_color="white"
        mlx_download_textField.border_color="white"
    else:
        ollama_download_textField.border_color="black"
        mlx_download_textField.border_color="black"
    
    model_hub_view.route = "/model_hub"
    model_hub_view.controls = [
        ft.AppBar(title=""),
        settings_banner_view,
        #coming_soon_view,
        model_tabs
    ]
    return model_hub_view