
class Properties:    
    def __init__(self, widget_template, callback = None, settings_window = None):
        self.__widget_template = widget_template
        self.__callback = callback
        self.__settings_window = settings_window
    
    
    @property
    def callback(self):
        return self.__callback
    
    @property
    def widget_template(self):
        return self.__widget_template
    
    @property
    def settings_window(self):
        return self.__settings_window