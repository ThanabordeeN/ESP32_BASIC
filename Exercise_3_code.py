import sys
from PyQt5 import QtWidgets,QtCore
from Excercise_3 import Ui_MainWindow
from serial import Serial
import pyqtgraph as pg
import numpy as np

class Exercise_3_code(Ui_MainWindow):

    def __init__(self):
        super().setupUi(MainWindow)
        self._setup_signal()
        self._graph_init()

    def _setup_signal(self):
        #self.STOP_BT.clicked.connect()
        self.LED_ON.clicked.connect(self.LED_ON_SENT)
        self.LED_COUNT_DOWN.clicked.connect(self.LED_COUNT_DOWN_SENT)

    def _graph_init(self):
        self.main_graph = pg.PlotWidget(self.centralwidget)
        self.main_graph.setGeometry(QtCore.QRect(60, 150, 600, 180))
        self.main_graph.setObjectName("graphview")
        self.main_graph.setBackground((60,60,60))
        self.main_graph.showGrid(x=True, y=True)

        self.main_graph.setTitle("LED Control")
        self.main_graph.setLabel("left","LED Voltage")
        self.main_graph.setLabel("bottom","Time")

    def _graph_plot(self):
        pass

    def GET_VALUE(self) -> int:
        value = self.LED_SLIDER.value()
        return value

    def SET_TEXT(self, task: str):
        self.TASK.setText("{task}{value}".format(task=task, value=self.GET_VALUE()))

    def LED_ON_SENT(self):
        self.SET_TEXT("L")

    def LED_COUNT_DOWN_SENT(self):
        self.SET_TEXT("C")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Exercise_3_code()

    MainWindow.show()
    sys.exit(app.exec_())
