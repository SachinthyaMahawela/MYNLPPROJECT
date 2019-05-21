import sys

from PyQt5.QtGui import *

import mysql.connector

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication

# import login
from PyQt5.uic import loadUi

cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
cursor = cnx.cursor()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class login(QDialog):
    def __init__(self):
        super(login, self).__init__()
        loadUi('login.ui', self)
        self.pushButton_login.clicked.connect(self.loginWithPassword)

    def loginWithPassword(self):
        username = self.lineEdit_user_name.text()
        password = self.lineEdit_password.text()

        user = cursor.execute("""SELECT username,password FROM login where username=%s and password=%s""",(username,password,))
        print('user>>> ', user)

        #cursor.fetchall()
        #cnx.commit()
        #cursor.close()
        #cnx.close()

        if (user == 1):
            QtGui.QMessageBox.information(self, '', "Login success...!!")
            global myTrueFalseVar
            myTrueFalseVar = True
            QDialog.setVisible(self, False)



        elif (user == 0):
            QtGui.QMessageBox.information(self, '', "Can't Login ...!!")


app = QApplication(sys.argv)
widget = login()
widget.show()
sys.exit(app.exec_())

