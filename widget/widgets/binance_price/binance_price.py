from ...widget import DesktopWidget
from ...properties import Properties
from PyQt6.QtWidgets import QVBoxLayout

import matplotlib
matplotlib.use('agg')
from threading import Thread
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


import json
import websocket
import requests
from enum import Enum
from datetime import datetime


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

class PriceGraph(Properties):
    __is_started = True

    class Interval(Enum):
        _1s = "1s"
        _1m = "1m"
        _3m = "3m"
        _5m = "5m"
        _15m = "15m"
        _30m = "30m"
        _1h = "1h"
        _2h = "2h"
        _4h = "4h"
        _6h = "6h"
        _8h = "8h"
        _12h = "12h"
        _1d = "1d"
        _3d = "3d"
        _1w = "1w"
        _1M = "1M"

    def __init__(self, width:int=200, heigh:int=100, interval:Interval=Interval._1s, symbol:str="SUNUSDT"):
        self.__data = [0] * 100
        self.__width = width
        self.__heigh = heigh
        self.__symbol = symbol
        self.__interval = interval
    
        self.__figure, self.__ax = plt.subplots()    
        self.__ax.set_facecolor((0.18, 0.18, 0.18, 0.1))
        self.__figure.patch.set_facecolor((0.11, 0.11, 0.11, 0.1))
        self.__figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.__figure.set_size_inches(*self.__pixels_to_inches(self.__width, self.__heigh, self.__figure.dpi))
        
        Thread(target=self.__start, daemon=True).start()

    def callback(self):
        self.__update_graph()

    def init_widget_template(self, widget:DesktopWidget):
        self.__canvas = CustomFigureCanvas(self.__figure, widget)
        layout = QVBoxLayout()
        layout.addWidget(self.__canvas)
        widget.setLayout(layout)
        self.__create_graph()

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
        return 1000
        # return eval(self.__frequency_update.value \
        #     .replace("s", "") \
        #     .replace("m", "*60") \
        #     .replace("h", "*60*60") \
        #     .replace("d", "*60*60*24") \
        #     .replace("w", "*60*60*24*7") \
        #     .replace("M", "*60*60*24*30")) * 1000

    def __create_graph(self):
        (self.__line,) = self.__ax.plot(self.__data, color='cyan', linewidth=1)

        self.__ax.set_ylim(0, 10)
        self.__ax.set_xlim(0, len(self.__data) - 1)
        
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])
        
        self.__canvas.draw()

    def __update_graph(self):
        self.__ax.set_ylim(min(self.__data), max(self.__data))
        self.__line.set_ydata(self.__data)
        self.__canvas.draw()
        self.__canvas.flush_events()
    
    def __on_message(self, ws, message):
        data = json.loads(message)['k']
        self.__data[-1] = float(data['c'])
        print(self.__data)
        if data["x"]:
            self.__data = self.__data[1:] + [float(data['c'])]
    
    def __on_error(self, ws, error):
        pass

    def __on_close(self, ws, close_status_code, close_msg):
        pass

    def __on_open(self, ws:websocket.WebSocketApp):
        self.__data = [float(i[4]) for i in self.__load_history()]
        params = {
            "method": "SUBSCRIBE",
            "params":
            [f"{self.__symbol.lower()}@kline_{self.__interval.value}"],
            "id": 1
        }

        ws.send(json.dumps(params))

    def __load_history(self):
        params = {
            "symbol": self.__symbol,
            "interval": self.__interval.value,
            "limit": 100
        }
        response = requests.get(url="https://api.binance.com/api/v3/klines", params=params)
        return json.loads(response.text)
    
    def __pixels_to_inches(self, width_px, height_px, dpi):
        return width_px / dpi, height_px / dpi
    
    def __start(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                                    on_message=self.__on_message,
                                    on_error=self.__on_error,
                                    on_close=self.__on_close)
        ws.on_open = self.__on_open
        ws.run_forever()