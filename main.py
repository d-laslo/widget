import sys
from widget import DesktopWidget
from widget.widgets import clock
from PyQt6.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DesktopWidget()
    widget.set_properties(clock)
    widget.show()
    sys.exit(app.exec())