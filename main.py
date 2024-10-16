import sys
from widget import DesktopWidget
from widget.widgets import Clock, CpuLoadGraph, PriceGraph
from PyQt6.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # w = DesktopWidget(Clock())
    # w.show()
    
    # w2 = DesktopWidget(CpuLoadGraph())
    # w2.show()

    w3 = DesktopWidget(PriceGraph(interval=PriceGraph.Interval._1m))
    w3.show()
    
    sys.exit(app.exec())

# import websocket
# import json

# def on_message(ws, message):
#     data = json.loads(message)
#     print(f"BTC/USDT Price: {data['p']}")

# def on_error(ws, error):
#     print(error)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# def on_open(ws):
#     params = {
#         "method": "SUBSCRIBE",
#         "params": [
#             "btcusdt@trade"
#         ],
#         "id": 1
#     }
#     ws.send(json.dumps(params))

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.on_open = on_open
#     ws.run_forever()

# print(eval("50*30"))