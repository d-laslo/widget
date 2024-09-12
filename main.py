import sys
from widget import DesktopWidget
from widget.widgets import Clock, CpuLoadGraph
from PyQt6.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DesktopWidget(Clock())
    w.show()
    
    w2 = DesktopWidget(CpuLoadGraph())
    w2.show()
    sys.exit(app.exec())