from socket import socket
from threading import Lock

from PyQt6.QtCore import QTimer

import Key
import Main

import socket
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QTextBrowser, QListWidget, QLabel,
                            QSpinBox, QPushButton, QPlainTextEdit)
from PyQt6.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Appelle le constructeur de QMainWindow
        loadUi("windowapp.ui", self)  # Charge l'interface Qt

        # Configuration du socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.1)  # Timeout pour les opérations de socket
        self.s.connect(("vlbelintrocrypto.hevs.ch", 6000))


        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start(250)  # Check every 250ms

        self.pushButton.clicked.connect(lambda: self.onButtonClickedSend(methode= (self.listWidget.currentItem().text() if self.listWidget.currentItem() else "Aucune méthode sélectionnée"), message= self.plainTextEdit.toPlainText(), key= self.plainTextEdit_2.toPlainText()))
        self.pushButton_2.clicked.connect(lambda: self.onButtonClickedTask(methode= self.listWidget.currentItem().text() if self.listWidget.currentItem() else "Aucune méthode sélectionnée"))

    def timer_callback(self):
        """Check for incoming messages periodically"""
        try:
            data = self.s.recv(1024)
            if data:
                message = self.clean_message(data.decode('utf-8'))
                self.textBrowser.append(f"Server: {message}")
        except socket.timeout:
            pass  # Pas de données disponibles
        except ConnectionResetError:
            self.textBrowser.append("Connection lost!")
            self.timer.stop()
        except Exception as e:
            self.textBrowser.append(f"Error receiving: {str(e)}")
    def onButtonClickedTask(self,methode = str):
        match methode:
            case "Shift":
                self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="shift", e_d="encode"))
            case "Vigenere":
                self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="vigenere", e_d="encode"))
            case "RSA":
                self.textBrowser.append(Main.InteractionWithServer(self.spinBox.value(), encode="RSA", e_d="encode"))
            case "Hash":
                self.textBrowser.append(Main.InteractionWithServerShort("hash"))
                #self.textBrowser.append(Main.InteractionWithServerShort("verify"))
            case "Diffie-Hellman":
                self.textBrowser.append(Main.InteractionWithServerShort("DifHel"))
            case _: self.textBrowser.append("None encryption method selected")

    def onButtonClickedSend(self, methode, message, key):
        if not message:
            self.textBrowser.append("No message to send!")
            return

        str(Key)
        key.replace(" ", "")
        if key == "" and methode != "Hash":
            # Key.sendMessage(message, "s", s = Main.s, encode = "none")
            self.textBrowser.append(message)
        else:
            match methode:
                case "Shift":
                    try :
                        nombre = int(key)
                        Key.sendMessage(message, "s", s = Main.s, encode = "shift", key = nombre)
                        self.textBrowser.append("You: " + Key.cleanMsg(Key.shiftEncode(message, nombre)))
                    except ValueError:
                        self.textBrowser.append("An error occurred while processing your request.")
                case "Vigenere":
                    Key.sendMessage(message, "s", s = Main.s, encode = "vigenere", key = key)
                    self.textBrowser.append("You: Message send")
                case "Hash":
                    Key.sendMessage(message.encode("UTF-"), ask= "s", s = Main.s, encode= "hashing")
                    self.textBrowser.append("You: " + Key.cleanMsg(Key.Hashing(message.encode("UTF-8"))))
                case "RSA":
                    l = key.split("/")
                    if len(l) == 2:
                        try :
                            n = int(l[0])
                            q = int(l[1])
                            if Key.is_prime(n) and Key.is_prime(q):
                                Key.RSAMessage(message, ask= "s", s= Main.s, n= n, e = n*q)
                                self.textBrowser.append("You : " + Key.cleanMsg(Key.RSAencode(message, n, n*q)))
                            else: self.textBrowser.append("The Keys are not prime numbers.")
                        except ValueError:
                            self.textBrowser.append("At least one LKey is not a number.")
                    else: self.textBrowser.append("Invalid Key. Must be \"n/q\".")
                case _:
                    self.textBrowser.append(message)
                    Key.sendMessage(message, ask= "s", s= Main.s, encode="none")


if __name__ == "__main__":
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()


    app.exec()
    sys.exit(app.exec())


