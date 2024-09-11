from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QMouseEvent
from .properties import Properties

class DesktopWidget(QWidget):
    __callback = None
    __settings_window = None
    __need_drag_widget = True

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 200);
                border-radius: 5px;
            }
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__update_time)
        self.timer.start(1000)
        
        self.setGeometry(1,1,1,1)
        self.drag_position = None
        
    def __update_time(self):
        if self.__callback is None:
            return
        self.__callback(self)
        
    def set_properties(self, properties:Properties):
        properties.widget_template(self)
        self.__callback = properties.callback
        self.__settings_window = properties.settings_window
        
    def set_drag_widget(self, need_drag_widget:bool) -> None:
        self.__need_drag_widget = need_drag_widget

    def mousePressEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
        if event.button() == Qt.MouseButton.MiddleButton:
            self.set_drag_widget(not self.__need_drag_widget)
            
        if self.__settings_window and event.button() == Qt.MouseButton.RightButton:
            self.__settings_window(self)

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()