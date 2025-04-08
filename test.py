import self

import Key
import Main


import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Appelle le constructeur de QMainWindow
        uic.loadUi("windowapp.ui", self)  # Charge l'interface Qt
        self.initUI()  # Appelle une méthode pour initialiser les éléments

    def initUI(self):
        self.pushButton_1.clicked.connect(self.on_button_click_shift)
        self.pushButton_2.clicked.connect(self.on_button_click_vigenere)
        self.pushButton_3.clicked.connect(self.on_button_click_RSA)

    def on_button_click_shift(self):
        self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="shift", e_d="encode"))

    def on_button_click_vigenere(self):
        self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="vigenere", e_d="encode"))

    def on_button_click_RSA(self):
        self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="RSA", e_d="encode"))

    def on_button_click_Listen(self):
        while True:
            msg = Main.s.recv(65000000)
            self.textBrowser.append(Key.cleanMsg(msg))
            if self.on_button_click_StopListening(): False

    def on_button_click_StopListening(self): ()




if __name__ == "__main__":
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()


    app.exec()
    sys.exit(app.exec())



