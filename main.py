from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import sqlite3
from random import choice

CONN = sqlite3.connect('Progress.db')


class TensesWindow(QtWidgets.QMainWindow):  # Выбор группы времён
    def __init__(self):
        super().__init__()
        uic.loadUi('TensesWindow.ui', self)

        self.SelectionWindow = None

        self.pushButton.clicked.connect(self.open_SelectionWindow)
        self.pushButton_2.clicked.connect(self.open_SelectionWindow)
        self.pushButton_3.clicked.connect(self.open_SelectionWindow)

    def open_SelectionWindow(self):
        self.close()
        self.SelectionWindow = SelectionWindow(self.sender().text())
        self.SelectionWindow.show()


class SelectionWindow(QtWidgets.QMainWindow):  # Выбор между теорией и практикой
    def __init__(self, tense):
        super().__init__()
        uic.loadUi('SelectionWindow.ui', self)

        self.TensesWindow = None
        self.TheoryWindow = None
        self.TasksWindow = None
        self.tense = tense
        average_value = CONN.cursor().execute(
            f"SELECT value, count FROM Results WHERE tense = '{self.tense}'").fetchone()
        try:
            self.label.setText(f"Средний результат: {average_value[0] // average_value[1]}/5")
        except ZeroDivisionError:
            self.label.setText('Средний результат: 0/5')

        self.pushButton.clicked.connect(self.open_TheoryWindow)
        self.pushButton_2.clicked.connect(self.open_TasksWindow)
        self.pushButton_3.clicked.connect(self.back)

    def open_TheoryWindow(self):
        self.close()
        self.TheoryWindow = TheoryWindow(self.tense)
        self.TheoryWindow.show()

    def open_TasksWindow(self):
        self.close()
        self.TasksWindow = TasksWindow(self.tense)
        self.TasksWindow.show()

    def back(self):
        self.close()
        self.TensesWindow = TensesWindow()
        self.TensesWindow.show()


class TheoryWindow(QtWidgets.QMainWindow):  # Теория
    def __init__(self, tense):
        super().__init__()
        uic.loadUi('TheoryWindow.ui', self)

        self.SelectionWindow = None
        self.tense = tense
        self.file_name_3 = CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Simple'").fetchone()[0]
        self.file_name_4 = CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Continuous'").fetchone()[0]
        self.file_name_5 = CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect'").fetchone()[0]
        self.file_name_6 = CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect Continuous'").fetchone()[0]

        self.plainTextEdit.appendPlainText(CONN.cursor().execute(
            f"SELECT theory FROM Theories WHERE tense = '{self.tense}'").fetchone()[0])

        self.label.setPixmap(QPixmap(CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Simple'").fetchone()[0]))
        self.label_2.setPixmap(QPixmap(CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Continuous'").fetchone()[0]))
        self.label_3.setPixmap(QPixmap(CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect'").fetchone()[0]))
        self.label_4.setPixmap(QPixmap(CONN.cursor().execute(
            f"SELECT image_path FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect Continuous'").fetchone()[0]))

        self.plainTextEdit_2.appendPlainText(CONN.cursor().execute(
            f"SELECT example FROM ImagesAndExamples WHERE tense = '{self.tense} Simple'").fetchone()[0])
        self.plainTextEdit_3.appendPlainText(CONN.cursor().execute(
            f"SELECT example FROM ImagesAndExamples WHERE tense = '{self.tense} Continuous'").fetchone()[0])
        self.plainTextEdit_4.appendPlainText(CONN.cursor().execute(
            f"SELECT example FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect'").fetchone()[0])
        self.plainTextEdit_5.appendPlainText(CONN.cursor().execute(
            f"SELECT example FROM ImagesAndExamples WHERE tense = '{self.tense} Perfect Continuous'").fetchone()[0])

        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.choose_picture)
        self.pushButton_4.clicked.connect(self.choose_picture)
        self.pushButton_5.clicked.connect(self.choose_picture)
        self.pushButton_6.clicked.connect(self.choose_picture)

    def choose_picture(self):
        object_name = self.focusWidget().objectName()
        file_name = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.png)')[0]

        if object_name == 'pushButton_3':
            self.file_name_3 = file_name
            self.label.setPixmap(QPixmap(f"{self.file_name_3}"))
        elif object_name == 'pushButton_4':
            self.file_name_4 = file_name
            self.label_2.setPixmap(QPixmap(f"{self.file_name_4}"))
        elif object_name == 'pushButton_5':
            self.file_name_5 = file_name
            self.label_3.setPixmap(QPixmap(f"{self.file_name_5}"))
        elif object_name == 'pushButton_6':
            self.file_name_6 = file_name
            self.label_4.setPixmap(QPixmap(f"{self.file_name_6}"))

    def save(self):
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET image_path = '{self.file_name_3}' "
                              f"WHERE tense = '{self.tense} Simple'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET image_path = '{self.file_name_4}' "
                              f"WHERE tense = '{self.tense} Continuous'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET image_path = '{self.file_name_5}' "
                              f"WHERE tense = '{self.tense} Perfect'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET image_path = '{self.file_name_6}' "
                              f"WHERE tense = '{self.tense} Perfect Continuous'")

        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET example = '{self.plainTextEdit_2.toPlainText()}' "
                              f"WHERE tense = '{self.tense} Simple'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET example = '{self.plainTextEdit_3.toPlainText()}' "
                              f"WHERE tense = '{self.tense} Continuous'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET example = '{self.plainTextEdit_4.toPlainText()}' "
                              f"WHERE tense = '{self.tense} Perfect'")
        CONN.cursor().execute(f"UPDATE ImagesAndExamples SET example = '{self.plainTextEdit_5.toPlainText()}' "
                              f"WHERE tense = '{self.tense} Perfect Continuous'")

        CONN.commit()

    def back(self):
        self.close()
        self.SelectionWindow = SelectionWindow(self.tense)
        self.SelectionWindow.show()


class TasksWindow(QtWidgets.QMainWindow):  # Задания
    def __init__(self, tense):
        super().__init__()
        uic.loadUi('TasksWindow.ui', self)

        self.ResultsWindow = None
        self.tense = tense
        self.number_question = 1
        self.quantity_correct_answer = 0
        self.list_sentences = [sentence[0] for sentence in CONN.cursor().execute(
            f"SELECT sentence FROM {self.tense}").fetchall()]
        self.sentence = choice(self.list_sentences)

        self.display_question_and_answers()

        self.pushButton.clicked.connect(self.check_answer)

    def check_answer(self):
        self.plainTextEdit.clear()

        if self.buttonGroup.checkedButton() and self.pushButton.text() == 'Проверить':
            if self.buttonGroup.checkedButton().text() == CONN.cursor().execute(
                    f"SELECT correct_answer FROM {self.tense} WHERE sentence = '{self.sentence}'").fetchone()[0]:
                self.plainTextEdit.appendPlainText('Ответ Верный!')
                self.quantity_correct_answer += 1
            else:
                self.plainTextEdit.appendPlainText(CONN.cursor().execute(
                    f"SELECT explanation FROM {self.tense} WHERE sentence = '{self.sentence}'").fetchone()[0])

            self.list_sentences.remove(self.sentence)
            try:
                self.sentence = choice(self.list_sentences)
            except IndexError:
                pass
            self.number_question += 1
            self.pushButton.setText('Дальше') if self.number_question != 6 else self.pushButton.setText('Закончить')

        elif self.pushButton.text() == 'Дальше':
            self.pushButton.setText('Проверить')
            self.display_question_and_answers()

        elif self.pushButton.text() == 'Закончить':
            self.close()
            self.ResultsWindow = ResultsWindow(self.tense, self.quantity_correct_answer)
            self.ResultsWindow.show()

        else:
            self.plainTextEdit.appendPlainText('Вы не ответили на вопрос!')

    def display_question_and_answers(self):
        self.label_3.setText(f"Вопрос {self.number_question}/5")
        self.label_2.setText(self.sentence)

        for i, radioButton in enumerate([self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4]):
            radioButton.setText(CONN.cursor().execute(
                f"SELECT answer_{i + 1} FROM {self.tense} WHERE sentence = '{self.sentence}'").fetchone()[0])


class ResultsWindow(QtWidgets.QMainWindow):  # Результаты
    def __init__(self, tense, quantity_correct_answer):
        super().__init__()
        uic.loadUi('ResultsWindow.ui', self)

        self.SelectionWindow = None
        self.tense = tense

        self.label.setText(f"Правильных ответов {quantity_correct_answer}/5")
        CONN.cursor().execute(f"UPDATE Results SET value = value + {quantity_correct_answer}, "
                              f"count = count + 1 WHERE tense = '{self.tense}'")

        CONN.commit()

        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.close()
        self.SelectionWindow = SelectionWindow(self.tense)
        self.SelectionWindow.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TensesWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
