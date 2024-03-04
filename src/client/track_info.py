from PySide6 import QtWidgets, QtGui
from src.client.tools.style_setter import set_style_sheet
import settings
from eyed3 import AudioFile


class TrackInfo(QtWidgets.QFrame):
    def __init__(self) -> None:
        super(TrackInfo, self).__init__()
        self.__init_ui()

    def __init_ui(self):
        self.setObjectName("TrackInfo")
        set_style_sheet(self, 'track_info.qss')

        main_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        self.track_image: QtWidgets.QLabel = QtWidgets.QLabel()
        self.track_name: QtWidgets.QLabel = QtWidgets.QLabel()

        self.track_image.setObjectName("TrackImage")
        self.track_name.setObjectName("TrackName")

        self.track_name.setText("Ничего не играет")
        self.track_image.setFixedSize(45, 45)
        self.track_image.setPixmap(QtGui.QPixmap(f'{settings.CLIENT_DIR}/img/track.png'))
        self.track_image.setScaledContents(True)
        self.track_name.setContentsMargins(10, 0, 0, 0)

        main_layout.addWidget(self.track_image)
        main_layout.addWidget(self.track_name)

    def set_track_info(self, track: AudioFile, pixmap: QtGui.QPixmap) -> None:
        self.track_name.setText(f'{track.tag.title} • {track.tag.artist}')
        self.track_image.setPixmap(pixmap)
