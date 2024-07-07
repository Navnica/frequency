import flet


class SettingsPage(flet.SafeArea):
    def __init__(self, content=None):
        super().__init__(content)

    def build(self):
        self.expand = True
        self.content = flet.Text(
            'Settings Page'
        )
