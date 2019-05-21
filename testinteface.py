
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QLineEdit,QTextEdit,QComboBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nltk import RegexpTokenizer
from itertools import product
from nltk.corpus import wordnet

class C(QDialog):
    def __init__(self):
        super(C, self).__init__()
        loadUi('testinterface.ui', self)
        self.setWindowTitle('Add Assignment')
        self.btn_select.clicked.connect(self.file_open)
        self.btn_select_2.clicked.connect(self.file_openx)
        self.pushButton_process.clicked.connect(self.getText)

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


    def file_openx(self):
        options = QFileDialog.Options()
        name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        self.textEdit_2.setText(name)
        file = open(name, 'r')
        with file:
            text = file.read()
            self.textEdit_2.setText(text)


    def getText(self):
        filename = self.textEdit.toPlainText()
        symb_remove = RegexpTokenizer(r'\w+')
        list1 = symb_remove.tokenize(filename)
        print("-----------------------------------")
        filename = self.textEdit_2.toPlainText()
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





app=QApplication(sys.argv)
widget=C()
widget.show()
sys.exit(app.exec_())