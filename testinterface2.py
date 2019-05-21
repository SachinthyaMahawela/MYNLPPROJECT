import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtCore, QtGui
from nltk.tokenize import RegexpTokenizer
import mysql.connector
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QLineEdit,QTextEdit,QComboBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nltk import RegexpTokenizer
from itertools import product
from nltk.corpus import wordnet




try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)





class P(QDialog):
    def __init__(self):
        super(P, self).__init__()
        loadUi('testinterface2.ui', self)
        self.setWindowTitle('Process the doc')
        self.pushButton_ok.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_process.clicked.connect(self.getText)
        self.btn_select.clicked.connect(self.file_open)

        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        query = "SELECT DISTINCT subject FROM addassignment"
        cursor.execute(query)

        results = cursor.fetchall()
        for i in range(0, len(results)):
         self.comboBox_type.addItem(results[i][0])
         self.tableWidget.cellClicked.connect(self.cell_was_clicked)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        subject = self.comboBox_type.currentText()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        sql = """SELECT DISTINCT ass_id,description FROM addassignment WHERE subject= '%s' """ % (subject)
        cursor.execute(sql)
        re = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(re):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        cnx.commit()
        cursor.close()
        cnx.close()

    def cell_was_clicked(self, row, column):
        items = self.tableWidget.currentItem()
        dd = items.text()
        #self.textEdit.setText(dd)
        file = dd

    def file_open(self):
        options = QFileDialog.Options()
        name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        self.textEdit.setText(name)
        file = open(name, 'r')
        with file:
            text = file.read()
            self.textEdit.setText(text)


    def getText(self):
        filename = self.textEdit.toPlainText()
        symb_remove = RegexpTokenizer(r'\w+')
        list1 = symb_remove.tokenize(filename)
        print("-----------------------------------")
        filename = self.textEdit.toPlainText()
        symb_remove = RegexpTokenizer(r'\w+')
        list2 = symb_remove.tokenize(filename)

        print("following is the wordlist of the file")
        print(list1)
        print(list2)

        sims = []
        initialList = []

        for word1, word2 in product(list1, list2):
            syns1 = wordnet.synsets(word1)
            print(syns1)
            syns2 = wordnet.synsets(word2)
            print(syns2)
            for word1 in syns1:
                for word2 in syns2:
                    s = word1.wup_similarity(word2)
                    if str(s) == 'None':
                        s = 0


                    initialList.append(s)
                    print(str(word1) + " second word"+  str(word2))
                    print(s)
            print(initialList)





app = QApplication(sys.argv)
widget = P()
widget.show()
sys.exit(app.exec_())








