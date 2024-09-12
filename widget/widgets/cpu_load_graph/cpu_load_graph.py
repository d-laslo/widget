from ...widget import DesktopWidget
from ...properties import Properties
from PyQt6.QtWidgets import QVBoxLayout

import psutil
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import mplcyberpunk 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from threading import Thread

def callback(widget:DesktopWidget):
    cpu_load = psutil.cpu_percent(interval=1)
    widget.data = widget.data[1:] + [cpu_load]

    Thread(target=update_graph, args=(widget,), daemon=True).start()

def update_graph(widget:DesktopWidget):
    widget.ax.clear()
    plt.style.use("cyberpunk")
    widget.ax.set_facecolor('#2E2E2E')
    widget.figure.patch.set_facecolor('#1C1C1C')

    widget.ax.plot(widget.data, color='cyan', linewidth=2)
    widget.ax.fill_between(range(len(widget.data)), widget.data, color='cyan', alpha=0.3)

    widget.ax.set_ylim(0, 100)
    widget.ax.set_xlim(0, len(widget.data) - 1)
    
    widget.ax.set_xticks([])
    widget.ax.set_yticks([])

    mplcyberpunk.add_glow_effects()
    widget.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    widget.canvas.draw()
    
def template(widget:DesktopWidget):
    widget.data = [0] * 100

    widget.figure, widget.ax = plt.subplots()
    widget.canvas = FigureCanvas(widget.figure)
    layout = QVBoxLayout()
    layout.addWidget(widget.canvas)
    widget.setLayout(layout)
    
    update_graph(widget)
    
def settings_window(widget:DesktopWidget):
    pass

cpu_load_graph = Properties(template, callback, settings_window)