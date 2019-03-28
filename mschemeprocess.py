
import mysql.connector
import sys
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLineEdit, QTextEdit
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtCore, QtGui
from nltk.tokenize import RegexpTokenizer

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

class ms(QDialog):
    def __init__(self):
        super(ms, self).__init__()
        loadUi('mschemeprocess.ui', self)
        self.setWindowTitle('Process the Marking Scheme ')
        self.pushButton_ok.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_process.clicked.connect(self.getText)

        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        query = "SELECT subject FROM markingscheme"
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
        sql = """SELECT mscheme_id,description FROM markingscheme WHERE subject= '%s' """ % (subject)
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
        self.textEdit.setText(dd)
        file=dd

    def getText(self):
        filename=self.textEdit.toPlainText()
        symb_remove = RegexpTokenizer(r'\w+')
        words=symb_remove.tokenize(filename)
        print(words)
        mystring =str(words)
        print(mystring)
        print(words)
        aftertokenize = word_tokenize(mystring)
        print(aftertokenize)
        count = len(words)
        print('01.The number of words of the given file:\n', count)
        print("-----------------------------------")


        stop_words = set(stopwords.words("english"))  # Stop words of the english language
        texts=[word for word in filename.lower().split() if word in stop_words]

        print("-----------------------------------")
        print('03.The number of stop words of the file:\n', len(texts))
        print("-----------------------------------")

        # tokenise the sentences...
        print("04.Seperate the sentences of given doc:")
        sent = sent_tokenize(filename)
        print(sent)
        print("-----------------------------------")

        print("05.Number of sentences of given file:\n", len(sent))
        print("-----------------------------------")

        # frequency of stop words separately.....
        print("06.The frequncy of stop words:")
        fdist = nltk.FreqDist(w.lower() for w in texts)
        for m in stop_words:
            if fdist[m] != 0:
                print(m + ':', fdist[m])


        tokens = word_tokenize(filename)  # tokenize the words
        tags = nltk.pos_tag(tokens)  # Taging the words..into verb, adjectives, nouns etc.
        print("08.The pos_tags of the given file:")
        for tag in tags:
            print(tag)

        # count the taging words separately..
        print("09.Number of taging words:")
        count1 = Counter(tag for word, tag in tags)
        print(count1)

        # To get the number of nouns of the file...
        nouns = []
        for word, pos in tags:
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)

        verbs = []
        for word, pos in tags:
            if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ'):
                verbs.append(word)

        # To get the number of adjectives of the file..
        adject = []
        for word, pos in tags:
            if (pos == 'JJ' or pos == 'JJR' or pos == 'JJS'):
                adject.append(word)

        # To get the number of adverbs of the file...
        adverb = []
        for word, pos in tags:
            if pos == 'RB' or pos == 'RBR' or pos == 'RBS':
                adverb.append(word)

        subject = self.comboBox_type.currentText()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        insertSQL = "INSERT INTO mscheme_data(subject,no_of_words,no_of_stopwords,no_of_sentences,no_of_nouns,no_of_verbs,no_of_adjectives,no_of_adverbs)" \
                    "VALUES('" + str(subject) + "','" + str(count) + "','" + str(len(texts)) + "','" + str(len(sent)) + "','" + str(len(nouns)) + "','" + str(len(verbs)) + "','" + str(len(adject)) + "','" + str(len(adverb)) + "')"
        cursor.execute(insertSQL)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Data save to the database")


app = QApplication(sys.argv)
widget = ms()
widget.show()
sys.exit(app.exec_())