import flet as ft

history_banner_text = ft.Text(value='Conversation History', style=ft.TextStyle(font_family='CabinSketch-Bold'), size=30)
history_banner_image = ft.Image(src=f"logos/combined_logos.png",
                      width=75,
                      height=75,
                      fit=ft.ImageFit.CONTAIN,
                      )

history_banner_view = ft.Row([
    history_banner_image,
    history_banner_text
], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

history_mock_data = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date/Time")),
                ft.DataColumn(ft.Text("Topic")),
                ft.DataColumn(ft.Text("Content"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("April 12")),
                        ft.DataCell(ft.Text("Topic 1")),
                        ft.DataCell(ft.Text(f"""
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
""")),
                    ],
                ),
                 ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("April 12")),
                        ft.DataCell(ft.Text("Topic 1")),
                        ft.DataCell(ft.Text(f"""
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
""")),
                    ],
                ),
                 ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("April 12")),
                        ft.DataCell(ft.Text("Topic 1")),
                        ft.DataCell(ft.Text(f"""
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
User : xxxxx
AI : xxxxx
""")),
                    ],
                ),
                
            ],
        )

history_data_view =  ft.Container(content=history_mock_data)

def historyView(theme: str) -> ft.View:

    return ft.View(
        "/history",
        controls = [
            ft.AppBar(title=""),
            history_banner_view,
            history_data_view
        ]
    )