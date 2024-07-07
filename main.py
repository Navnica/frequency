import flet
from src.player_page import PlayerPage
from src.settings_page import SettingsPage
from src.media_library_page import MediaLibraryPage


def main(page: flet.Page):
    pages = (
        MediaLibraryPage(),
        PlayerPage(),
        SettingsPage()
    )

    def on_change_page(event: flet.ControlEvent) -> None:
        page.controls[0].content = pages[int(event.data)]
        page.update()

    page.title = 'Frequency'
    page.window.width = 400
    page.window.height = 600
    page.window.center()

    page.add(
        flet.Container(
            expand=True,
            content=pages[1]
        ),
        flet.Container(
            border_radius=15,
            content=flet.NavigationBar(
                selected_index=1,
                on_change=on_change_page,
                destinations=[
                    flet.NavigationBarDestination(
                        icon=flet.icons.LIBRARY_MUSIC,
                        label='Медиатека'
                    ),

                    flet.NavigationBarDestination(
                        icon=flet.icons.PLAY_CIRCLE,
                        label='Плеер',
                    ),

                    flet.NavigationBarDestination(
                        icon=flet.icons.SETTINGS,
                        label='Настройки'
                    )
                ]
            )
        )
    )


if __name__ == '__main__':
    flet.app(
        target=main
    )
