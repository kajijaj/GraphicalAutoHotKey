import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtMultimedia import QSound


class Buttons(QWidget):
    send = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi('UILayouts/Buttons.ui', self)
        self.sound = QSound('assets/click.wav', self)
        self.event_buttons = []
        self.buttons = list(map(lambda x: x.clicked.connect(self.add), self.KeyboardButtons.buttons()))
        del self.buttons[-1]
        self.end.clicked.connect(self.complete)

    def add(self):
        self.sound.play()
        self.event_buttons.append(self.sender().text())

    def complete(self):
        self.result.setText('_'.join(self.event_buttons))
        self.send.emit(self.result.text())
        self.event_buttons.clear()
        self.result.setText('')
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Buttons()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

