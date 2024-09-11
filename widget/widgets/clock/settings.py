import sys
from PyQt6.QtWidgets import (QFormLayout, QComboBox, QSpinBox, QPushButton, QDialog, QLabel)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor
from . import default

class SettingsDialog(QDialog):
    def __init__(self, label: QLabel):
        super().__init__()
        
        self.__label = label

        self.setWindowTitle('Font settings')
        self.setGeometry(QCursor.pos().x(), QCursor.pos().y(), 0, 0)
        self.setFixedSize(200,100)

        self.fontComboBox = QComboBox(self)
        self.fontComboBox.addItems(default.font_families)
        self.fontComboBox.setCurrentText(label.font().family())

        self.sizeSpinBox = QSpinBox(self)
        self.sizeSpinBox.setRange(default.font_size_min, default.font_size_max)
        self.sizeSpinBox.setValue(label.font().pointSize())
        
        self.applyButton = QPushButton('Apply', self)
        self.applyButton.clicked.connect(self.apply_font_settings)

        layout = QFormLayout()
        layout.addRow(QLabel('Type:', self), self.fontComboBox)
        layout.addRow(QLabel('Size:', self), self.sizeSpinBox)
        layout.addWidget(self.applyButton)

        self.setLayout(layout)
        
    def apply_font_settings(self):
        self.__label.setFont(QFont(self.fontComboBox.currentText(), self.sizeSpinBox.value()))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SettingsDialog(None)
    widget.show()
    sys.exit(app.exec())