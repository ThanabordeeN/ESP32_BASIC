import sys
from PyQt5 import QtWidgets, QtCore
from Excercise_3 import Ui_MainWindow
from serial import Serial
import pyqtgraph as pg
from datetime import datetime


class Exercise_3_code(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        self._setup_signal()
        self._graph_init_()
        self.x = []
        self.y = []
        self._timer_setup()

    def _setup_signal(self):
        self.STOP_BT.clicked.connect(self.STOP_SENT)
        self.LED_ON.clicked.connect(self.LED_ON_SENT)
        self.LED_COUNT_DOWN.clicked.connect(self.LED_COUNT_DOWN_SENT)

    def SENT_SIGNAL(self,
                    data: str):
        payload = "{task}{value}".format(task=data, value=self.GET_VALUE())
        SER.write(payload.encode())
        timestamp = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        self.LOG_TEXT.appendPlainText(f"SENT: {data}, TIMESTAMP: {timestamp}, DATE: {date}\n")
        self.GRAPH_PLOT()

    def _graph_init_(self):
        self.main_graph = pg.PlotWidget(self.centralwidget)
        self.main_graph.setGeometry(QtCore.QRect(60, 150, 600, 180))
        self.main_graph.setObjectName("graphview")
        self.main_graph.setBackground((60, 60, 60))
        self.main_graph.showGrid(x=True, y=True)

        self.main_graph.setTitle("LED Control")
        self.main_graph.setLabel("left", "LED Voltage")
        self.main_graph.setLabel("bottom", "Time")

    def GRAPH_PLOT(self):
        self.x.append(datetime.now().timestamp())
        self.main_graph.plot(self.x, self.y, pen='y', symbol='o')  # Plot the data

    def RECIEVE_SIGNAL(self):
        recieve_data = SER.readline().decode().strip()
        self.y.append(int(recieve_data))
        self.GRAPH_PLOT()

    def _timer_setup(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.RECIEVE_SIGNAL)
        timer.start(1000)

    def GET_VALUE(self) -> int:
        value = self.LED_SLIDER.value()
        return value

    def SET_TEXT(self, task: str):
        text = "{task}{value}".format(task=task, value=self.GET_VALUE())
        self.TASK.setText(text)

    def LED_ON_SENT(self):
        self.SET_TEXT("L")
        self.SENT_SIGNAL("L")

    def LED_COUNT_DOWN_SENT(self):
        self.SET_TEXT("C")
        self.SENT_SIGNAL("C")

    def STOP_SENT(self):
        self.SET_TEXT("S")
        self.SENT_SIGNAL('S')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    SER = Serial(port='COM3', baudrate=115200, timeout=1)

    ui = Exercise_3_code()

    MainWindow.show()
    sys.exit(app.exec_())
