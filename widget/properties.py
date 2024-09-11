
class Properties:    
    def __init__(self, widget_template, callback):
        self.__widget_template = widget_template
        self.__callback = callback
    
    
    @property
    def callback(self):
        return self.__callback
    
    @property
    def widget_template(self):
        return self.__widget_template