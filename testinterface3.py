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
        loadUi('testinterface3.ui', self)
        self.setWindowTitle('Process the doc')
        self.pushButton_ok.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_ok_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_process.clicked.connect(self.getText)


        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        query = "SELECT DISTINCT subject FROM addassignment"
        cursor.execute(query)

        results = cursor.fetchall()
        for i in range(0, len(results)):
            self.comboBox_type.addItem(results[i][0])
            self.tableWidget.cellClicked.connect(self.cell_was_clicked)

        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor1 = cnx.cursor()
        query1 = "SELECT DISTINCT subject FROM markingscheme"
        cursor1.execute(query1)

        results1 = cursor1.fetchall()
        for i in range(0, len(results1)):
            self.comboBox_type_2.addItem(results[i][0])
            self.tableWidget_2.cellClicked.connect(self.cell_2_was_clicked)


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
        file = dd







    def on_pushButton_2_clicked(self):
        subject = self.comboBox_type_2.currentText()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor1 = cnx.cursor()
        sql = """SELECT DISTINCT mscheme_id,description FROM markingscheme WHERE subject= '%s' """ % (subject)
        cursor1.execute(sql)
        re = cursor1.fetchall()
        self.tableWidget_2.setRowCount(0)
        for row_number, row_data in enumerate(re):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        cnx.commit()
        cursor1.close()
        cnx.close()

    def cell_2_was_clicked(self, row, column):
        items1 = self.tableWidget_2.currentItem()
        ddd = items1.text()
        file=ddd



    def getText(self):
        filename = self.textEdit.toPlainText()
        symb_remove = RegexpTokenizer(r'\w+')
        list1 = symb_remove.tokenize(filename)
        print("-----------------------------------")
        filename = self.items1.toPlainText()
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
                    print(str(word1) + " second word" + str(word2))
                    print(s)
            print(initialList)

app = QApplication(sys.argv)
widget = P()
widget.show()
sys.exit(app.exec_())



