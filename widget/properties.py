from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QWidget
class Properties(ABC):    
    @abstractmethod
    def callback(self):
        pass
    
    @abstractmethod
    def init_widget_template(self, widget:QWidget):
        pass
    
    @abstractmethod
    def settings_window(self, widget:QWidget):
        pass
    
    @abstractmethod
    def get_start_size(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @property
    @abstractmethod
    def is_resizable(self):
        pass
    
    @property
    @abstractmethod
    def frequency_update(self):
        '''how often the widget should be updated (in milliseconds)'''
        pass