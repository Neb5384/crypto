import sys
import time

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
import websockets

import Main
import Key


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Charge l'interface utilisateur
        uic.loadUi("Screen01.ui.qml", self)

        # Connecter les signaux aux slots
        self.setup_connections()

        # Initialiser les variables
        self.current_method = None

        #écouter le serveur
        self.serverListening()

    def setup_connections(self):
        # Connecter les boutons radio aux méthodes
        self.radioButton.toggled.connect(lambda: self.set_method("shift"))
        self.radioButton1.toggled.connect(lambda: self.set_method("vigenere"))
        self.radioButton2.toggled.connect(lambda: self.set_method("RSA"))
        self.radioButton3.toggled.connect(lambda: self.set_method("hash"))
        self.radioButton4.toggled.connect(lambda: self.set_method("DifHel"))

        # Connecter les boutons d'action
        self.taskEncode.clicked.connect(self.send_task)
        self.taskHash.clicked.connect(lambda: self.send_short_task("hash"))
        self.taskVerify.clicked.connect(lambda: self.send_short_task("verify"))
        self.button.clicked.connect(self.send_custom_message)

    def set_method(self, method):
        self.current_method = method
        print(f"Méthode sélectionnée: {method}")


    def send_task(self):
        if not self.current_method:
            self.label.append("Veuillez sélectionner une méthode d'encryption")
            return

        try:
            # Récupérer la longueur depuis le SpinBox
            length = self.spinBox.value()

            # Exécuter la tâche avec la longueur spécifiée
            result = Main.InteractionWithServer(
                length,
                encode=self.current_method,
                e_d="encode" if self.switch1.checked else "decode"
            )
            self.label.append(result)
        except Exception as e:
            self.label.append(f"Erreur: {str(e)}")

    def send_short_task(self, task_type):
        try:
            result = Main.InteractionWithServerShort(task_type)
            self.label.append(str(result))
        except Exception as e:
            self.label.append(f"Erreur: {str(e)}")

    def send_custom_message(self):
        message = self.textField2.text()
        if not message:
            self.label.append("Veuillez entrer un message")
            return

        try:
            # Envoyer le message personnalisé selon la méthode sélectionnée
            if self.current_method in ["shift", "vigenere"]:
                key = self.textField1.text()  # Pour les méthodes nécessitant une clé
                Key.sendMessage(
                    message,
                    ask='s',
                    s=Main.s,
                    encode=self.current_method,
                    key=key
                )
            elif self.current_method == "RSA":
                # Vous devrez implémenter la logique RSA spécifique
                pass
            elif self.current_method == "DifHel":
                # Vous devrez implémenter la logique Diffie-Hellman spécifique
                pass
            else:
                Key.sendMessage(
                    message,
                    ask='s',
                    s=Main.s,
                    encode="none"
                )

        except Exception as e:
            self.label.append(f"Erreur lors de l'envoi: {str(e)}")

    def serverListening(self):
        while True:
            data = Main.s.recv(1024)  # Reçoit jusqu'à 1024 octets
            if not data:
                break  # Si le serveur ferme la connexion
            print(f"Message reçu : {data.decode('utf-8')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())