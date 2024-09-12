import sys
from widget import DesktopWidget
from widget.widgets import clock, cpu_load_graph
from PyQt6.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DesktopWidget()
    widget.set_properties(cpu_load_graph)
    widget.show()
    
    # widget2 = DesktopWidget()
    # widget2.set_properties(clock)
    # widget2.show()
    
    sys.exit(app.exec())