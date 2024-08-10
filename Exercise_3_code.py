import sys
from PyQt5 import QtWidgets
from Excercise_3 import Ui_MainWindow


class Exercise_3_code(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)

    def _setup_signal(self):
        self.STOP_BT.clicked.connect()
        self.LED_ON.clicked.connect()
        self.LED_COUNT_DOWN.clicked.connect()
        self.LED_SLIDER.valueChanged.connect()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Exercise_3_code()

    MainWindow.show()
    sys.exit(app.exec_())
