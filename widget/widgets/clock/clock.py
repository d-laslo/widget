from ...widget import DesktopWidget
from ...properties import Properties
from .settings import SettingsDialog
from . import default
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog
from datetime import datetime


class Clock(Properties):
    def __init__(self, time_format:str = '%H:%M:%S'):
        self.__time_format = time_format

    def callback(self):
        self.__label.setText(datetime.now().strftime(self.__time_format))
    
    def init_widget_template(self, widget:DesktopWidget):
        self.__label = QLabel(widget)
        self.__label.setFont(QFont(default.font_families[0], default.font_size_min))
        self.__label.setStyleSheet("color: white;")
        self.__label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__label)
        widget.setLayout(self.__layout)
    
    def settings_window(self, widget:DesktopWidget):
        widget:QDialog = SettingsDialog(self, widget)
        widget.exec()
        
    def get_start_size(self):
        return 1,1
    
    @property
    def is_resizable(self):
        return False
    
    @property
    def label(self):
        return self.__label