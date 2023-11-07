import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sqlite3


class Change(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UILayouts/Change.ui', self)
        self.modified = {}
        self.lst = None
        self.loadb.clicked.connect(self.load_user_db)
        self.updateb.clicked.connect(self.update_data)
        # Подключение БД по умолчанию
        self.con = sqlite3.connect('ScriptFiles/Buttons.sqlite')
        self.cur = self.con.cursor()
        self.load_db()

    def load_db(self):
        result = self.cur.execute('SELECT * FROM events').fetchall()
        try:
            self.database.setRowCount(len(result))
            self.database.setColumnCount(len(result[0]))
            self.lst = [i[0] for i in self.cur.description]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.database.setItem(i, j, QTableWidgetItem(str(val)))
        except IndexError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Пустая БД')
            msg.setWindowTitle('Error')
            msg.exec_()

    def load_user_db(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать Базу данных', '', 'База данных (*.sqlite)')[0]
        self.con = sqlite3.connect(fname)
        self.cur = self.con.cursor()
        result = self.cur.execute('SELECT * FROM events').fetchall()
        try:
            self.database.setRowCount(len(result))
            self.database.setColumnCount(len(result[0]))
            self.lst = [i[0] for i in self.cur.description]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.database.setItem(i, j, QTableWidgetItem(str(val)))
        except IndexError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Пустая БД')
            msg.setWindowTitle('Error')
            msg.exec_()
        except sqlite3.OperationalError:
            pass

    def update_data(self):
        try:
            user_id = self.id.text()
            user_action = self.action.currentText()
            if user_action == 'кликнуть':
                values = (user_action, int(user_id),)
            else:
                user_action += f'({self.duration.text()})'
                values = (user_action, int(user_id),)
            seq = 'UPDATE events SET action=? WHERE id=?'
            self.cur.execute(seq, values)
            self.con.commit()
            result = self.cur.execute('SELECT * FROM events').fetchall()
            self.database.setRowCount(len(result))
            self.database.setColumnCount(len(result[0]))
            self.lst = [i[0] for i in self.cur.description]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.database.setItem(i, j, QTableWidgetItem(str(val)))
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Неправильный или пустой id! Введите целочисленный id')
            msg.setWindowTitle('Error')
            msg.exec_()

    def closeEvent(self, event):
        try:
            self.con.close()
        except AttributeError:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Change()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
