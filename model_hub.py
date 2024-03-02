import flet as ft

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

ollama_download_text = ft.Text('Download Ollama Model from ollama.ai')
ollama_download_textField = ft.TextField(width=500, height=50)
ollama_download_button = ft.IconButton(ft.icons.DOWNLOAD)

mlx_download_text = ft.Text('Download MlX Model from 🤗')
mlx_download_textField = ft.TextField(width=500, height=50)
mlx_download_button = ft.IconButton(ft.icons.DOWNLOAD)

ollama_control = ft.Column([
        ollama_download_text,
        ft.Row([
            ollama_download_textField,
            ollama_download_button,
    ]),
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
                content = mlx_control
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

    return ft.View(
        "/model_hub",
        controls = [
            ft.AppBar(title=""),
            settings_banner_view,
            coming_soon_view,
            #model_tabs
        ]
    )