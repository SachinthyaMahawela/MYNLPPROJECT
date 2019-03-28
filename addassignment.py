import mysql.connector
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QLineEdit,QTextEdit,QComboBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class C(QDialog):
    def __init__(self):
        super(C, self).__init__()
        loadUi('assignment.ui', self)
        self.setWindowTitle('Add Assignment to Database')
        self.btn_select.clicked.connect(self.file_open)
        self.btn_save.clicked.connect(self.file_save)


    @pyqtSlot()
    def file_open(self):
        options = QFileDialog.Options()
        name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        self.textEdit.setText(name)
        file = open(name, 'r')
        with file:
            text = file.read()
            self.textEdit.setText(text)


    def file_save(self):
        sub = self.comboBox_subject.currentText()
        level = self.comboBox_level.currentText()
        sem = self.comboBox_sem.currentText()
        date = self.dateEdit.date()
        myDate = date.toPyDate()
        assno = self.comboBox_assignmentno.currentText()
        scheme = self.textEdit.toPlainText()

        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        add_assignment = "INSERT INTO addassignment " "(subject, level, semester, date, assignmentno, description) ""VALUES (%s, %s, %s, %s, %s, %s)"
        assignment_data = (sub, level, sem, myDate, assno, scheme)
        cursor.execute(add_assignment, assignment_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Assignment Answer Saved")


app=QApplication(sys.argv)
widget=C()
widget.show()
sys.exit(app.exec_())