import sys

import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

from signup import Ui_signup


class login(QDialog):
    def __init__(self):
        super(login, self).__init__()
        loadUi('login.ui', self)
        self.setWindowTitle('Login User')
        self.pushButton_login.clicked.connect(self.loginCheck)
        self.pushButton_signup.clicked.connect(self.signupCheck)


    @pyqtSlot()
    def loginCheck(self):
        username = self.lineEdit_user_name.text()
        password = self.lineEdit_password.text()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        result = cursor.execute("""SELECT username,password FROM login where username=%s and password=%s""",(username, password,))
        #self.filesavewindowshow()
        #if not len(result.fetchall()) <= 0:
        #print("User Found!")
        #else:
        #print("User Not  Found!")


    def signupCheck(self):
        #self.signupwindowshow()
        print("Sign up Button Clicked !!")

app=QApplication(sys.argv)
widget=login()
widget.show()
sys.exit(app.exec_())