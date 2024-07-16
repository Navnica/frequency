import flet
from settings import Settings as settings


class SettingsPage(flet.SafeArea):
    def __init__(self, content=None):
        super().__init__(content)

    def on_pick_path_click(self) -> None:
        def pick_path_result(event: flet.FilePickerResultEvent) -> None:
            settings.config_manager.update_value(
                key='music_dir',
                new_value=event.path
            )
            self.build()
            self.update()

        self.page.overlay.append(
            flet.FilePicker(
                on_result=pick_path_result,
            )
        )
        self.page.update()
        self.page.overlay[-1].get_directory_path()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            controls=[
                flet.Container(
                    border_radius=15,
                    padding=5,
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    content=flet.Column(
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Icon(
                                        name=flet.icons.SETTINGS
                                    ),
                                    flet.Text(
                                        value='Основные'
                                    )
                                ]
                            ),
                            flet.Divider(height=10),
                            flet.Row(
                                controls=[
                                    flet.Text(
                                        value='Путь к музыке',
                                    ),
                                    flet.Container(
                                        height=30,
                                        expand=True,
                                        content=flet.TextField(
                                            text_size=14,
                                            text_align=flet.TextAlign.START,
                                            text_vertical_align=flet.VerticalAlignment.START,
                                            dense=True,
                                            read_only=True,
                                            value=settings.config_manager.get_value('music_dir')
                                        )
                                    ),
                                    flet.IconButton(
                                        icon=flet.icons.MORE_HORIZ,
                                        on_click=lambda _: self.on_pick_path_click()
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
