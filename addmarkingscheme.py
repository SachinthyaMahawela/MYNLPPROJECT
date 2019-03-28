import mysql.connector
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLineEdit, QTextEdit, QComboBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class mscheme(QDialog):
    def __init__(self):
        super(mscheme, self).__init__()
        loadUi('markingscheme.ui', self)
        self.setWindowTitle('Add Marking Scheme to Database')
        self.pushButton_select.clicked.connect(self.mscheme_open)
        self.pushButton_save.clicked.connect(self.mscheme_save)

    @pyqtSlot()
    def mscheme_open(self):
        options = QFileDialog.Options()
        name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        self.textEdit.setText(name)
        file = open(name, 'r')
        with file:
            text = file.read()
            self.textEdit.setText(text)

    def mscheme_save(self):
        sub = self.comboBox_subject.currentText()
        lec = self.comboBox_lecturer.currentText()
        level = self.comboBox_level.currentText()
        sem = self.comboBox_sem.currentText()
        date = self.dateEdit.date()
        myDate=date.toPyDate()
        assno = self.comboBox_assignmentno.currentText()
        scheme = self.textEdit.toPlainText()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        add_markingscheme = "INSERT INTO markingscheme " "(subject, lecturer, level, semester, date, assignmentno, description) ""VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mscheme_data = (sub, lec, level, sem, myDate, assno, scheme)
        cursor.execute(add_markingscheme, mscheme_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Marking Scheme Answer Saved")


app = QApplication(sys.argv)
widget = mscheme()
widget.show()
sys.exit(app.exec_())
