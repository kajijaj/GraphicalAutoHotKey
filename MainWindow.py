import sys
import subprocess
import sqlite3
import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from Buttons import Buttons
from Change import Change
from Appearance import Appearance


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UILayouts/MainWindowUI.ui', self)
        self.setFixedSize(800, 575)
        self.widget = self.centralWidget()
        # Преобразование выбранной даты в формат Python
        self.chosendate = self.calendar.selectedDate().toPyDate()
        # Создание классов кнопок, редактирования и таймера
        self.buttons = Buttons()
        self.beauty = Appearance()
        self.timer = QTimer()
        # Показ времени
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.date_label.setText(QDate.currentDate().toString('dd:MM:yy'))
        # Подключение кнопок
        self.Appearance.clicked.connect(self.design)
        self.buttons.send.connect(self.show_event)
        self.AddButton.clicked.connect(self.add_event)
        self.changebutton.clicked.connect(self.change)
        self.write.clicked.connect(self.write_db)
        self.load.clicked.connect(self.open_db)
        self.writefile.clicked.connect(self.write_file)
        self.clear_db.clicked.connect(self.clear)
        self.start.clicked.connect(self.exec)
        self.load_design.clicked.connect(self.load_des)
        # Подключение базы данных по умолчанию
        self.con = sqlite3.connect('ScriptFiles/Buttons.sqlite')
        self.db.setText(f'База данных: ScriptFiles/Buttons.sqlite')
        self.cur = self.con.cursor()
        result = self.cur.execute("""SELECT date, time, event, action FROM events""").fetchall()
        for elem in result:
            self.events.addItem(f'{str(elem[0])}, {str(elem[1])}, {str(elem[2])}, {str(elem[3])}')
        # Подключение уже существующего дизайна
        self.load_des()

    def add_event(self):
        self.buttons.show()

    def show_event(self, event):
        self.events.addItem(f'{self.time.text()}, {self.calendar.selectedDate().toPyDate()}, {event}')

    def write_db(self):
        to_write = tuple([self.events.item(_).text().split(', ') for _ in range(self.events.count())])
        for line in to_write:
            self.cur.execute('INSERT INTO events(date, time, event) VALUES(?, ?, ?)', (line[1], line[0], line[2]))
            self.con.commit()

    def closeEvent(self, event):
        try:
            self.con.close()
            self.p.terminate()
            self.close()
        except AttributeError:
            pass

    def open_db(self):
        self.events.clear()
        fname = QFileDialog.getOpenFileName(self, 'Выбрать Базу данных', '', 'База данных (*.sqlite)')[0]
        self.con = sqlite3.connect(fname)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,'
                         'date TEXT,'
                         'time TEXT,'
                         'event TEXT,'
                         'action TEXT)')
        self.db.setText(f'База данных: {fname}')
        result = self.cur.execute("""SELECT date, time, event, action FROM events""").fetchall()
        for elem in result:
            self.events.addItem(f'{str(elem[0])}, {str(elem[1])}, {str(elem[2])}, {str(elem[3])}')

    def write_file(self):
        seq = 'SELECT time, date, event, action FROM events'
        result = self.cur.execute(seq).fetchall()
        for row in result:
            df = pd.read_sql_query(seq, self.con)
            df.to_csv('ScriptFiles/output.csv', index=False, sep=';')
        self.is_recorded.setText('События записаны в файл!')

    def change(self):
        self.changer = Change()
        self.changer.show()

    def show_time(self):
        current_time = QTime.currentTime()
        str_time = current_time.toString('hh:mm')
        self.time_label.setText(str_time)

    def clear(self):
        self.cur.execute("DELETE FROM events")
        self.con.commit()
        self.events.clear()
        file = open('ScriptFiles/output.csv', mode='w')
        file.close()

    def exec(self):
        self.is_running.setText('Процесс запущен')
        self.cmd = 'python Script.py'
        self.p = subprocess.Popen(self.cmd, shell=True)

    def design(self):
        self.beauty.show()

    def load_des(self):
        try:
            file = open('assets/Design.txt')
            content = list(map(str.strip, file.readlines()))
            image = content[0]
            stylesheet = '#centralwidget' + '{background-image: url(' + f"'{image}'" + '); background-repeat: no-repeat}'
            self.setStyleSheet(stylesheet)
            self.AddButton.setStyleSheet(f'background-color: {content[4]};'
                                         f'color: {content[3]};'
                                         f'font-family: {content[1]};'
                                         f'font-style: {content[2]};'
                                         f'{content[5]};'
                                         f'{content[6]};'
                                         )
            self.changebutton.setStyleSheet(f'background-color: {content[4]};'
                                            f'color: {content[3]};'
                                            f'font-family: {content[1]};'
                                            f'font-style: {content[2]};'
                                            f'{content[5]};'
                                            f'{content[6]};')
            self.write.setStyleSheet(f'background-color: {content[4]};'
                                     f'color: {content[3]};'
                                     f'font-family: {content[1]};'
                                     f'font-style: {content[2]};'
                                     f'{content[5]};'
                                     f'{content[6]};')
            self.load.setStyleSheet(f'background-color: {content[4]};'
                                    f'color: {content[3]};'
                                    f'font-family: {content[1]};'
                                    f'font-style: {content[2]};'
                                    f'{content[5]};'
                                    f'{content[6]};')
            self.writefile.setStyleSheet(f'background-color: {content[4]};'
                                         f'color: {content[3]};'
                                         f'font-family: {content[1]};'
                                         f'font-style: {content[2]};'
                                         f'{content[5]};'
                                         f'{content[6]};')
            self.clear_db.setStyleSheet(f'background-color: {content[4]};'
                                        f'color: {content[3]};'
                                        f'font-family: {content[1]};'
                                        f'font-style: {content[2]};'
                                        f'{content[5]};'
                                        f'{content[6]};')
            self.start.setStyleSheet(f'background-color: {content[4]};'
                                     f'color: {content[3]};'
                                     f'font-family: {content[1]};'
                                     f'font-style: {content[2]};'
                                     f'{content[5]};'
                                     f'{content[6]};')
            self.load_design.setStyleSheet(f'background-color: {content[4]};'
                                           f'color: {content[3]};'
                                           f'font-family: {content[1]};'
                                           f'font-style: {content[2]};'
                                           f'{content[5]};'
                                           f'{content[6]};')
            self.Appearance.setStyleSheet(f'background-color: {content[4]};'
                                          f'color: {content[3]};'
                                          f'font-family: {content[1]};'
                                          f'font-style: {content[2]};'
                                          f'{content[5]};'
                                          f'{content[6]};')
            self.date_label.setStyleSheet(f'color: {content[3]}')
            self.time_label.setStyleSheet(f'color: {content[3]}')
            self.db.setStyleSheet(f'color: {content[3]}')
            self.is_recorded.setStyleSheet(f'color: {content[3]}')
            self.is_running.setStyleSheet(f'color: {content[3]}')
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Отсутствует файл дизайна!')
            msg.setWindowTitle('Error')
            msg.exec_()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
