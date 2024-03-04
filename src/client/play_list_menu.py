import eyed3
from PySide6 import QtWidgets, QtCore, QtGui
import settings
from src.client.tools.style_setter import set_style_sheet
from src.client.tools.config_manager import ConfigManager
from src.client.animated_panel import AnimatedPanel
from src.client.tools.track_loader import get_tracks_in_music_dir
from io import BytesIO


class PlayListMenu(AnimatedPanel):
    tracks: list = []

    def __init__(self, parent) -> None:
        super(PlayListMenu, self).__init__(parent)
        self.__init_ui()
        self.hide()

    def __init_ui(self) -> None:
        self.setObjectName("PlayListMenu")
        set_style_sheet(self, 'play_list_menu.qss')
        self.main_layout.setContentsMargins(0, 10, 0, 10)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if ConfigManager.get_config()['music_dir'] == '':
            self.set_notification('Похоже, папка с музыкой не указана')
            return

        scroll_area: QtWidgets.QScrollArea = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.verticalScrollBar().setMaximumWidth(6)
        scroll_area.verticalScrollBar().setObjectName('ScrollBar')
        scroll_area.setObjectName('ScrollArea')

        scroll_widget: QtWidgets.QWidget = QtWidgets.QWidget()
        scroll_widget.setObjectName('ScrollWidget')
        self.scroll_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_layout.setContentsMargins(10, 0, 10, 0)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        self.main_layout.addWidget(scroll_area)

        self.load_music()

    def set_notification(self, message: str) -> None:
        title: QtWidgets.QLabel = QtWidgets.QLabel()
        title.setText(message)
        title.setObjectName("TitleLabel")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title)
        self.main_layout.addItem(QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Policy.Fixed))
        button: QtWidgets.QPushButton = QtWidgets.QPushButton()
        button.setText('Настройки')
        self.main_layout.addWidget(button)
        button.clicked.connect(self.set_music_dir)
        button.setObjectName('ToSettingsButton')
        button.setMinimumSize(250, 30)

    def reload(self, only_clear: bool = False) -> None:
        layout = self.main_layout
        self.tracks.clear()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not only_clear:
            self.__init_ui()

    def set_music_dir(self) -> None:
        self.parent().side_menu.on_settings_pressed()

    def load_music(self) -> None:
        files: list = get_tracks_in_music_dir(True)

        if not files:
            self.reload(only_clear=True)
            self.set_notification('Тут как-то тихо..')
            return

        for track in files:
            new_track_frame: PlayListMenu.TrackFrame = PlayListMenu.TrackFrame(track=track)

            self.scroll_layout.addWidget(new_track_frame)
            new_track_frame.size_expand()
            self.tracks.append(new_track_frame)

    def size_expand(self) -> None:
        self.resize(self.parent().width() - 20, self.parent().height() - 70)
        for track in self.tracks:
            track.size_expand()

    class TrackFrame(QtWidgets.QFrame):
        track: eyed3.AudioFile

        def __init__(self, track: eyed3.AudioFile) -> None:
            super(PlayListMenu.TrackFrame, self).__init__()

            self.track = track

            self.__init_ui()

        def __init_ui(self) -> None:
            self.setObjectName("TrackFrame")
            self.main_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
            self.main_layout.setContentsMargins(5, 5, 5, 5)
            self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.setLayout(self.main_layout)
            self.setFixedHeight(40)

            label_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

            self.pixmap_label: QtWidgets.QLabel = QtWidgets.QLabel()
            self.track_name_label: QtWidgets.QLabel = QtWidgets.QLabel()
            self.info_label: QtWidgets.QLabel = QtWidgets.QLabel()

            self.pixmap_label.setScaledContents(True)
            self.pixmap_label.setFixedSize(30, 30)
            self.pixmap_label.setObjectName('PixmapLabel')

            self.track_name_label.setText(self.track.tag.title)
            self.info_label.setText(f'{self.track.tag.artist} • {self.track.tag.album}')
            self.info_label.setObjectName('InfoLabel')

            if self.track.tag.images:
                pixmap: QtGui.QPixmap = QtGui.QPixmap()
                pixmap.loadFromData(BytesIO(self.track.tag.images[0].image_data).getvalue())
                self.image = pixmap
                self.pixmap_label.setPixmap(pixmap)

            else:
                self.image = QtGui.QPixmap(f'{settings.CLIENT_DIR}/img/track.png')
                self.pixmap_label.setPixmap(self.image)

            self.main_layout.addWidget(self.pixmap_label)
            self.main_layout.addItem(QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Policy.Fixed))
            self.main_layout.addLayout(label_layout)

            label_layout.addWidget(self.track_name_label)
            label_layout.addWidget(self.info_label)

        def mousePressEvent(self, event) -> None:
            self.setStyleSheet('background-color: rgb(60, 60, 60)')
            main_window = self.parent().parent().parent().parent().parent()
            main_window.side_menu.on_play_list_pressed()
            main_window.play_frame.set_track(self.track)

            if not main_window.play_frame.play_button_state:
                main_window.play_frame.toggle_play_button()

        def mouseReleaseEvent(self, event) -> None:
            self.setStyleSheet('''
            QFrame#TrackFrame{background-color: rgb(70, 70, 70);} 
            QFrame#TrackFrame::hover{background-color: rgb(75, 75, 75);}
            ''')

        def size_expand(self) -> None:
            self.setFixedWidth(self.parent().parent().parent().parent().width() - 20)
