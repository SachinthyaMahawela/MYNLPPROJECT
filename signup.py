

from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *




class Ui_signup(QDialog):
    def __init__(self):
        super(Ui_signup, self).__init__()
        loadUi('signup.ui', self)
        self.setWindowTitle('Sign Up')
        self.pushButton_signup.clicked.connect(self.signup)
        self.pushButton_back.clicked.connect(self.loginwindowshow)

    def loginwindowshow(self):
        self.log = QtWidgets.QDialog()
        self.ui = log()
        self.ui.setupUi(self.login)
        self.signup.show()


    @pyqtSlot()
    def signup(self):
        name = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        signupuser = "INSERT INTO login "  "(username, email,  password) ""VALUES (%s, %s, %s)"
        data = (name,email,password)
        cursor.execute(signupuser,data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("New User Added")




app=QApplication(sys.argv)
widget=Ui_signup()
widget.show()
sys.exit(app.exec_())

