# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


import mysql.connector

from PyQt5 import QtCore, QtGui, QtWidgets


from signup import Ui_signup


class Ui_login(object):
    def signupwindowshow(self):
        self.signup=QtWidgets.QDialog()
        self.ui = Ui_signup()
        self.ui.setupUi(self.signup)
        self.signup.show()

    def filesavewindowshow(self):
        self.filesave=QtWidgets.QDialog()
        #self.ui = C()
        self.ui.setupUi(self.filesave)
        self.filesave.show()

    def loginCheck(self):
        username=self.lineEdit_user_name.text()
        password=self.lineEdit_password.text()
        cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
        cursor = cnx.cursor()
        result = cursor.execute("""SELECT username,password FROM login where username=%s and password=%s""",(username, password,))
        #if not len(result.fetchall()) <= 0:
        #print("User Found!")
        #else:
        self.filesavewindowshow()
        #print("User Not  Found!")

    def signupCheck(self, signup):
        self.signupwindowshow()
        print("Sign up Button Clicked !!")

    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(515, 318)
        login.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 234, 220, 221), stop:1 rgba(255, 255, 255, 255))")
        self.groupBox = QtWidgets.QGroupBox(login)
        self.groupBox.setGeometry(QtCore.QRect(60, 50, 381, 211))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_user_name = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_user_name.setGeometry(QtCore.QRect(140, 50, 211, 26))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_user_name.setFont(font)
        self.lineEdit_user_name.setObjectName("lineEdit_user_name")
        self.lineEdit_password = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_password.setGeometry(QtCore.QRect(140, 100, 211, 26))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setInputMask("")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.pushButton_login = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_login.setGeometry(QtCore.QRect(160, 160, 91, 28))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)

        #
        self.pushButton_login.clicked.connect(self.loginCheck)
        #
        self.pushButton_login.setFont(font)
        self.pushButton_login.setStyleSheet("")
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_signup = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_signup.setGeometry(QtCore.QRect(270, 160, 91, 28))


        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)

        self.pushButton_signup.clicked.connect(self.signupCheck)
        self.pushButton_signup.setFont(font)
        self.pushButton_signup.setStyleSheet("")
        self.pushButton_signup.setObjectName("pushButton_signup")

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Dialog"))
        self.groupBox.setTitle(_translate("login", "SignIn"))
        self.label_4.setText(_translate("login", "User Name"))
        self.label_5.setText(_translate("login", "Password"))
        self.pushButton_login.setText(_translate("login", "Login"))
        self.pushButton_signup.setText(_translate("login", "Sign up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = QtWidgets.QDialog()
    ui = Ui_login()
    ui.setupUi(login)
    login.show()
    sys.exit(app.exec_())

