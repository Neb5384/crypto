from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vlayout = QVBoxLayout()
        self.text = QLabel()
        self.vlayout.addWidget(self.text)

        self.counter = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start(250)

        self.setLayout(self.vlayout)

    def timer_callback(self):
        self.text.setText(str(self.counter))
        self.counter += 1

if __name__ == "__main__":

    qApp = QApplication([])
    main_window = SimpleWindow()
    main_window.show()
    qApp.exec()