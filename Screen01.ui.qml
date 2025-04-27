/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import Crypto_app
import QtQuick.Studio.DesignEffects

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height
    color: "#000000"

    GroupBox {
        id: groupBox
        x: 77
        y: 60
        width: 255
        height: 306
        title: qsTr("Encoding Method")

        RadioButton {
            id: radioButton
            x: 0
            y: 0
            visible: true
            text: qsTr("Shift")
        }

        RadioButton {
            id: radioButton1
            x: 0
            y: 54
            text: qsTr("Vigenere")
        }

        RadioButton {
            id: radioButton2
            x: 0
            y: 108
            text: qsTr("RSA")
        }

        RadioButton {
            id: radioButton3
            x: 0
            y: 162
            text: qsTr("Hashing")
        }


        RadioButton {
            id: radioButton4
            x: 0
            y: 216
            text: qsTr("Diffie-Hellman")
        }


        Button {
            id: taskHash
            x: 340
            y: 10
            width: 150
            height: 115
            opacity: radioButton3.checked
            text: qsTr("Task Hash")
            state: "taskHash"
            checkable: false
            flat: false
        }

        Button {
            id: taskVerify
            x: 559
            y: 10
            width: 150
            height: 115
            opacity: radioButton3.checked
            text: qsTr("Task Verify")
            flat: false
            checkable: false
        }

        Button {
            id: taskEncode
            x: 449
            y: 10
            width: 150
            height: 115
            opacity: radioButton.checked || radioButton1.checked || radioButton2.checked || radioButton4.checked
            text: qsTr("Task Encode")
            state: ""
            flat: false
            checkable: false
        }
    }

    TextField {
        id: textField1
        x: 338
        y: 252
        width: 521
        height: 56
        placeholderText: qsTr("Text Field")
    }

    Button {
        id: button
        x: 865
        y: 252
        width: 206
        height: 114
        text: qsTr("Send Message")
    }

    Switch {
        id: switch1
        x: 1108
        y: 299
        text: qsTr("Encode")
    }

    Label {
        id: label
        x: 77
        y: 372
        width: 1741
        height: 610
    }

    SpinBox {
        id: spinBox
        x: 1010
        y: 130
        to: 20
    }

    TextField {
        id: textField2
        x: 338
        y: 314
        width: 521
        height: 56
        placeholderText: qsTr("Text Field")
    }




    states: [
        State {
            name: "clicked"
        }
    ]
}


