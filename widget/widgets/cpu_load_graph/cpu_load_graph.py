from ...widget import DesktopWidget
from ...properties import Properties
from PyQt6.QtWidgets import QVBoxLayout

import psutil
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import mplcyberpunk 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from threading import Thread

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
    def __init__(self, width=200, heigh=100, frequency_update = 1000):
        self.__data = [0] * 100
        self.__figure, self.__ax = plt.subplots()
        self.__width = width
        self.__heigh = heigh
        self.__is_started = True
        self.__frequency_update = frequency_update

        self.__figure.set_size_inches(*self.__pixels_to_inches(self.__width, self.__heigh, self.__figure.dpi), True)
        Thread(target=self.__update_cpu_data, daemon=True).start()
    
    def callback(self):
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
        return self.__width, self.__heigh
    
    def stop(self):
        self.__is_started = False
    
    @property
    def is_resizable(self):
        return True
    
    @property
    def frequency_update(self):
        return self.__frequency_update

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
        
    def __update_cpu_data(self):
        while self.__is_started:
            self.__data = self.__data[1:] + [psutil.cpu_percent(interval=(self.__frequency_update // 1000))]
            
    def __pixels_to_inches(self, width_px, height_px, dpi):
        return width_px / dpi, height_px / dpi