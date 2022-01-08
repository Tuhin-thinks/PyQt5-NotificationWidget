import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from notif_widget import BellWidget


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.resize(QtCore.QSize(450, 350))
        self.setWindowTitle("demo - notification widget")

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("centralWidget")

        self.central_widget.setStyleSheet("#centralWidget{ background-color: cyan; }")
        self.setCentralWidget(self.central_widget)

        self.vBoxLayout_main = QtWidgets.QVBoxLayout(self.central_widget)
        # self.central_widget.setLayout(self.vBoxLayout_main)

        self.bell_widget = BellWidget(self.central_widget)
        self.vBoxLayout_main.addWidget(self.bell_widget, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        self.info_label = QtWidgets.QLabel(self.central_widget)
        self.vBoxLayout_main.addWidget(self.info_label, 0, Qt.AlignHCenter | Qt.AlignBottom)
        self.info_label.setText("You have some notifications to check...")

        self.info_label_2 = QtWidgets.QLabel(self.central_widget)
        self.vBoxLayout_main.addWidget(self.info_label_2, 0, Qt.AlignHCenter | Qt.AlignBottom)
        self.info_label_2.setStyleSheet("color: grey;")
        self.info_label_2.setText("<scroll over notification bell to see>")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
