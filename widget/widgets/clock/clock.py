from ...widget import DesktopWidget
from ...properties import Properties
from .settings import SettingsDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog
from datetime import datetime
from . import default

def callback(widget:DesktopWidget):
    current_time = datetime.now().strftime('%H:%M:%S')
    widget.label.setText(current_time)
    
def template(widget:DesktopWidget):
    widget.label = QLabel(widget)
    widget.label.setFont(QFont(default.font_families[0], default.font_size_min))
    widget.label.setStyleSheet("color: white;")
    widget.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(widget.label)
    widget.setLayout(layout)
    
def settings_window(widget:DesktopWidget):
    widget:QDialog = SettingsDialog(widget.label)
    widget.exec()
    
clock = Properties(template, callback, settings_window)