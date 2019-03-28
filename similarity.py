from collections import defaultdict
import mysql.connector
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QLineEdit,QTextEdit,QComboBox
from PyQt5.uic import loadUi
from nltk.tokenize import RegexpTokenizer
import nltk

from gensim import corpora,models,similarities
import logging
from nltk.corpus import stopwords


class Check(QDialog):

    def __init__(self):
        super(Check,self).__init__()
        loadUi('check.ui',self)
        self.setWindowTitle('Check Assignment ')
        self.pushButton_2.clicked.connect(self.check_category)
        self.pushButton.clicked.connect(self.file_open)

        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        query = ("SELECT subject FROM addassignment")
        cursor.execute(query)

        result = cursor.fetchall()
        for i in range(0, len(result)):
            self.comboBox.addItem(result[i][0])
        cnx.commit()
        cursor.close()
        cnx.close()

    def file_open(self):
       options= QFileDialog.Options()
       name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options = options)
       self.textEdit.setText(name)
       file=open(name,'r')
       with file:
          text=file.read()
          self.textEdit.setText(text)

    @pyqtSlot()
    def check_category(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        subject = self.comboBox.currentText()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        sql = "SELECT description FROM markingscheme WHERE subject= '%s' " % (subject)
        cursor.execute(sql)

        result = cursor.fetchall()
        print(result[0])
        raw_corpus = [self.textEdit.toPlainText()]
        for i in range(0, len(result)):
            raw_corpus += result[i]
        print(raw_corpus)


        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix= tfidf_vectorizer.fit_transform(raw_corpus)
        from sklearn.metrics.pairwise import cosine_similarity
        print(cosine_similarity(tfidf_matrix[0:1],tfidf_matrix))
        similarity=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix)
        print(similarity)
        length=tfidf_matrix.shape[0]
        sim=[]
        for i in range(0,length):
            sim.append((i ,similarity[0][i]))
        print(sim, "Checking Similarity")
        sims = sorted(sim, key=lambda item: -item[1])
        print(sims, "Checking Sorted Similarity")

        Range=[]
        f = 0

        for j in range(0,1):
            Range.append((sims[j][0]))
        print(Range)

        for i in Range:
            e=result[i]
            query = "SELECT subject,no_of_words,no_of_stopwords,no_of_uniquewords,no_of_sentences,no_of_paragraphs FROM document_data WHERE subject= '%s' " % (e)
            cursor.execute(query)
            result2 = cursor.fetchone()
            #print(result2)
            #print(result2[0])
            assignment = self.textEdit.toPlainText()

            # no of words
            tokenizer = RegexpTokenizer(r'\w+')  # without punctuations
            tokenizer.tokenize(assignment)
            words = len(tokenizer.tokenize(assignment))
            print("Words",words)

            # no of stoppwords
            stoplist = set(stopwords.words('english'))
            texts = [word for word in assignment.lower().split() if word in stoplist]
            no_stopwords = len(texts)
            print("Stop Words = ",no_stopwords)

            # no of unique words
            texts = [word for word in tokenizer.tokenize(assignment) if word not in stoplist]
            no_unique = list(set(texts))
            unique = len(no_unique)
            print("Unique Words = ",unique)

            # no of sentences
            sents = nltk.sent_tokenize(assignment)
            sentences = len(sents)
            print("Sentences = ",sentences)

            # No of paragraphs
            para = assignment.splitlines()
            paragraphs = len(para)
            print( "Paragraphs = ",paragraphs)


            TagPatterngrammer = ""
            Tagpattern = []
            text = nltk.word_tokenize(assignment)
            results = nltk.pos_tag(text)
            for (word, tag) in results:
                Tagpattern.append(tag)
                TagPatterngrammer += "<" + tag + ">"
            convertstring = ','.join(Tagpattern)
            print("tag",tag)
            print(convertstring, "\n")
            print("Tag Pattern Grammer = ", TagPatterngrammer)
            print(len(Tagpattern))
            print("\n")


            if words>=250:
                mark1=round((words/result2[paragraphs,1]))*result2[0]
                print(mark1)
                mark2=round((no_stopwords/result2[2]))*result2[0]
                print(mark2)
                mark3=round((unique/result2[3]))*result2[0]
                print(mark3)
                mark4=round((sentences/result2[4]))*result2[0]
                print(mark4)
                mark5=round((paragraphs/result2[5]))*result2[0]
                print(mark5)
                mark6 = round((len(Tagpattern) / result2[6])) * result2[0]
                print(mark6)
                fin = round((mark1 + mark2 + mark3 + mark4 + mark5 + mark6) / 6)
                f = f+fin
                print("Marks = ",fin,f)

        print("Final Score",f/2)
        cnx.commit()
        cursor.close()
        cnx.close()
app=QApplication(sys.argv)
widget=Check()
widget.show()
sys.exit(app.exec_())