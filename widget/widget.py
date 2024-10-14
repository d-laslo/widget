from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QMouseEvent
from .properties import Properties

class DesktopWidget(QWidget):
    __allow_drag_widget = True
    __drag_position = None
    __resizing = False
    __mouse_pos = 0

    def __init__(self, properties:Properties, x = 1, y = 1):
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
        self.setGeometry(x,y,*properties.get_start_size())
        self.adjustSize()
        self.__set_resize_mod(properties.is_resizable)

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__update_time)
        self.__timer.start(self.__properties.frequency_update)
    
    @property      
    def __allow_resize(self):
        return not (self.minimumSize() == self.maximumSize())
        
    def __update_time(self):
        self.__properties.callback()

    def __set_drag_widget(self, allow_drag_widget:bool) -> None:
        self.__allow_drag_widget = allow_drag_widget
        
    def __set_resize_mod(self, allow_resize:bool) -> None:
        if allow_resize:
            self.setMinimumSize(50, 50)
            self.setMaximumSize(16777215, 16777215)
        else:
            self.setFixedSize(self.width(), self.height())

    def __is_near_edge(self, pos):
        margin = 30
        return pos.x() > self.width() - margin and pos.y() > self.height() - margin

    def mousePressEvent(self, event:QMouseEvent) -> None:            
        if event.button() == Qt.MouseButton.LeftButton:
            self.__mouse_pos = event.globalPosition().toPoint()
            if self.__is_near_edge(event.pos()):
                self.__resizing = True
            elif self.__allow_drag_widget:
                self.__drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
        if event.button() == Qt.MouseButton.MiddleButton:
            self.__set_drag_widget(not self.__allow_drag_widget)
            self.__set_resize_mod(not self.__allow_resize and self.__properties.is_resizable)
            
        if event.button() == Qt.MouseButton.RightButton:
            self.__properties.settings_window(self)
        
        event.accept()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if self.__allow_drag_widget and event.buttons() == Qt.MouseButton.LeftButton and self.__drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.__drag_position)
            
        if self.__resizing:
            diff = event.globalPosition().toPoint() - self.__mouse_pos
            self.resize(
                max(self.width() + diff.x(), self.minimumWidth()), 
                max(self.height() + diff.y(), self.minimumHeight())
            )
            self.__mouse_pos = event.globalPosition().toPoint()
        else:
            if self.__is_near_edge(event.pos()):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        self.__resizing = False
        if self.__allow_drag_widget and event.button() == Qt.MouseButton.LeftButton:
            self.__drag_position = None
        event.accept()
    
    def resizeEvent(self, event):
        if not self.__allow_resize:
            return
        super().resizeEvent(event)
        
    def closeEvent(self, event):
        self.__properties.stop()
        super().closeEvent(event)