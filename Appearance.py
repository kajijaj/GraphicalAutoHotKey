import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QColorDialog, QFontDialog
from PyQt5.QtGui import QFontInfo
from PyQt5.QtCore import pyqtSignal


class Appearance(QWidget):
    sender = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Настройка внешнего вида главного окна')
        self.initUI()

    def initUI(self):
        #
        self.main_window_label = QLabel(self)
        self.main_window_label.setText('Задний фон главного окна:')
        self.main_window_label.move(25, 50)
        #
        self.background_image_path = QLabel(self)
        self.background_image_path.setText('placeholder')
        self.background_image_path.move(250, 50)
        self.background_image_path.hide()
        #
        self.background_button = QPushButton(self)
        self.background_button.resize(100, 40)
        self.background_button.move(200, 35)
        self.background_button.setText('Выбрать фон')
        self.background_button.clicked.connect(self.open_image)
        #
        self.background_placeholder = QLabel(self)
        self.background_placeholder.move(35, 300)
        self.background_placeholder.setMinimumSize(800, 575)
        self.background_placeholder.setMaximumSize(29999, 2939239)
        #
        self.font_family = QLabel(self)
        self.font_family.move(25, 100)
        self.font_family.setText('Семейство шрифтов:')
        #
        self.font_family_button = QPushButton(self)
        self.font_family_button.clicked.connect(self.choose_font)
        self.font_family_button.move(200, 90)
        self.font_family_button.resize(175, 25)
        self.font_family_button.setText('Выбрать семейство шрифтов')
        #
        self.font_family_example = QLabel(self)
        self.font_family_example.move(400, 90)
        self.font_family_example.setText('Образец')
        self.font_family_example.setMinimumSize(100, 20)
        # Плейсхолдеры для хранения имен
        self.font_color_label = QLabel(self)
        self.font_color_label.move(25, 150)
        self.font_color_label.setText('Цвет текста кнопок:')
        self.font_family_placeholder = QLabel(self)
        self.font_family_placeholder.hide()
        self.font_color_placeholder = QLabel(self)
        self.font_color_placeholder.hide()
        self.font_style_placeholder = QLabel(self)
        self.font_style_placeholder.hide()
        #
        self.font_color_choose = QPushButton(self)
        self.font_color_choose.move(150, 140)
        self.font_color_choose.setText('Выбрать цвет шрифта кнопок')
        self.font_color_choose.setMinimumSize(150, 20)
        self.font_color_choose.clicked.connect(self.font_color)
        #
        self.background_button_color_label = QLabel(self)
        self.background_button_color_label.move(25, 200)
        self.background_button_color_label.setText('Цвет кнопок:')
        #
        self.background_button_color_button = QPushButton(self)
        self.background_button_color_button.move(100, 195)
        self.background_button_color_button.setText('Выбрать цвет кнопок')
        self.background_button_color_button.clicked.connect(self.background_color)
        #
        self.background_button_color_placeholder = QLabel(self)
        self.background_button_color_placeholder.hide()
        #
        self.finish = QPushButton(self)
        self.finish.move(350, 250)
        self.finish.setStyleSheet('background-color: red;'
                                  'color: green')
        self.finish.setText('Завершить')
        self.finish.clicked.connect(self.complete)

    def open_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать фон', 'assets', ''
                                                                           'Изображение (*png);; '
                                                                           'Изображение (*jpg);; Все форматы(*)')[0]

        self.pixmap = QPixmap(fname)
        self.background_placeholder.setPixmap(self.pixmap)
        self.background_image_path.setText(fname)

    def choose_font(self):
        font_name, ok = QFontDialog.getFont()
        if ok:
            self.font_family_example.setFont(font_name)
            self.font_family_placeholder.setText(QFontInfo(font_name).family())
            self.font_style_placeholder.setText(QFontInfo(font_name).styleName())

    def font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_family_example.setStyleSheet(f'color: {color.name()}')
            self.font_color_placeholder.setText(color.name())

    def background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_button_color_button.setStyleSheet(f'background-color: {color.name()}')
            self.background_button_color_placeholder.setText(color.name())

    def complete(self):
        file = open('assets/Design.txt', mode='w')
        file.write(f'{self.background_image_path.text()}\n')
        file.write(f'{self.font_family_placeholder.text()}\n')
        file.write(f'{self.font_style_placeholder.text()}\n')
        file.write(f'{self.font_color_placeholder.text()}\n')
        file.write(f'{self.background_button_color_placeholder.text()}\n')
        file.write('border-radius: 10px\n')
        file.write('border: 2px solid #094065\n')
        file.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Appearance()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
