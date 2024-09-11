from ..widget import DesktopWidget
from ..properties import Properties
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout
from datetime import datetime

def callback(widget:DesktopWidget):
    current_time = datetime.now().strftime('%H:%M:%S')
    widget.label.setText(current_time)
    
def template(widget:DesktopWidget):
    widget.label = QLabel(widget)
    widget.label.setFont(QFont('Helvetica', 20))
    widget.label.setStyleSheet("color: white;")
    widget.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(widget.label)
    widget.setLayout(layout)
    
clock = Properties(template, callback)