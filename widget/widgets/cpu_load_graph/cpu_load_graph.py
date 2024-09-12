from ...widget import DesktopWidget
from ...properties import Properties
from PyQt6.QtWidgets import QVBoxLayout

import psutil
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import mplcyberpunk 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class CustomFigureCanvas(FigureCanvas):
    def __init__(self, figure, parent):
        super().__init__(figure)
        self.parent = parent

    def mousePressEvent(self, event):
        self.parent.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.parent.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.parent.mouseMoveEvent(event)

class CpuLoadGraph(Properties):
    def __init__(self, ):
        self.__data = [0] * 100
        self.__figure, self.__ax = plt.subplots()
    
    def callback(self):
        self.__data = self.__data[1:] + [psutil.cpu_percent(interval=0)]
        self.update_graph()
    
    def init_widget_template(self, widget:DesktopWidget):
        self.__canvas = CustomFigureCanvas(self.__figure, widget)
        layout = QVBoxLayout()
        layout.addWidget(self.__canvas)
        widget.setLayout(layout)
        self.update_graph()
    
    def settings_window(self, widget:DesktopWidget):
        pass
    
    def get_start_size(self):
        return 200,100
    
    @property
    def is_resizable(self):
        return True

    def update_graph(self):
        self.__ax.clear()
        plt.style.use("cyberpunk")        
        self.__ax.set_facecolor((0.18, 0.18, 0.18, 0.1))
        self.__figure.patch.set_facecolor((0.11, 0.11, 0.11, 0.1))

        self.__ax.plot(self.__data, color='cyan', linewidth=2)
        self.__ax.fill_between(range(len(self.__data)), self.__data, color='cyan', alpha=0.3)

        self.__ax.set_ylim(0, 100)
        self.__ax.set_xlim(0, len(self.__data) - 1)
        
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        mplcyberpunk.add_glow_effects()
        self.__figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.__canvas.draw()