import sys
from PyQt6.QtWidgets import (QFormLayout, QComboBox, QSpinBox, QPushButton, QDialog, QLabel)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from . import default
# from .clock import Clock

class SettingsDialog(QDialog):
    def __init__(self, properties, widget):
        super().__init__()
        self.__properties = properties
        self.__widget = widget

        self.setWindowTitle('Font settings')
        self.setGeometry(QCursor.pos().x(), QCursor.pos().y(), 0, 0)
        self.setFixedSize(200,100)
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.fontComboBox = QComboBox(self)
        self.fontComboBox.addItems(default.font_families)
        self.fontComboBox.setCurrentText(self.__properties.label.font().family())

        self.sizeSpinBox = QSpinBox(self)
        self.sizeSpinBox.setRange(default.font_size_min, default.font_size_max)
        self.sizeSpinBox.setValue(self.__properties.label.font().pointSize())
        
        self.applyButton = QPushButton('Apply', self)
        self.applyButton.clicked.connect(self.apply_font_settings)

        layout = QFormLayout()
        layout.addRow(QLabel('Type:', self), self.fontComboBox)
        layout.addRow(QLabel('Size:', self), self.sizeSpinBox)
        layout.addWidget(self.applyButton)

        self.setLayout(layout)
        
    def apply_font_settings(self):
        self.__properties.label.setFont(QFont(self.fontComboBox.currentText(), self.sizeSpinBox.value()))
        self.__widget.adjustSize()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SettingsDialog(None)
    widget.show()
    sys.exit(app.exec())