from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QMouseEvent
from .properties import Properties

class DesktopWidget(QWidget):
    __need_drag_widget = True

    def __init__(self, properties:Properties):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 200);
                border-radius: 5px;
            }
        """)
        
        self.__properties = properties
        self.__properties.init_widget_template(self)

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__update_time)
        self.__timer.start(1000)
        
        self.setGeometry(1,1,*properties.get_start_size())
        self.drag_position = None
        
    def __update_time(self):
        self.__properties.callback()

    def set_drag_widget(self, need_drag_widget:bool) -> None:
        self.__need_drag_widget = need_drag_widget

    def mousePressEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
        if event.button() == Qt.MouseButton.MiddleButton:
            self.set_drag_widget(not self.__need_drag_widget)
            
        if event.button() == Qt.MouseButton.RightButton:
            self.__properties.settings_window(self)

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        if self.__need_drag_widget and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()