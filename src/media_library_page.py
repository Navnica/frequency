import flet


class MediaLibraryPage(flet.SafeArea):
    def __init__(self, content = None):
        super().__init__(content)

    def build(self):
        self.expand = True
        self.content = flet.Text(
            'Media library Page'
        )