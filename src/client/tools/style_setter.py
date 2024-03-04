import settings
from PySide6.QtWidgets import QWidget


def set_style_sheet(widget: QWidget, file: str):
    with open(f'{settings.STYLE_DIR}/{file}', 'r') as file:
        widget.setStyleSheet(file.read())
