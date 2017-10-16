# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SQLQueries(object):
    def setupUi(self, SQLQueries):
        SQLQueries.setObjectName("SQLQueries")
        SQLQueries.resize(590, 448)
        self.connString = QtWidgets.QLineEdit(SQLQueries)
        self.connString.setGeometry(QtCore.QRect(10, 10, 471, 21))
        self.connString.setCursorPosition(0)
        self.connString.setObjectName("connString")
        self.query = QtWidgets.QPlainTextEdit(SQLQueries)
        self.query.setGeometry(QtCore.QRect(10, 40, 471, 131))
        self.query.setObjectName("query")
        self.execute = QtWidgets.QPushButton(SQLQueries)
        self.execute.setGeometry(QtCore.QRect(480, 90, 111, 32))
        self.execute.setObjectName("execute")
        self.results = QtWidgets.QTableView(SQLQueries)
        self.results.setGeometry(QtCore.QRect(10, 180, 571, 261))
        self.results.setObjectName("results")

        self.retranslateUi(SQLQueries)
        QtCore.QMetaObject.connectSlotsByName(SQLQueries)

    def retranslateUi(self, SQLQueries):
        _translate = QtCore.QCoreApplication.translate
        SQLQueries.setWindowTitle(_translate("SQLQueries", "SQL queries"))
        self.connString.setPlaceholderText(_translate("SQLQueries", "sqlite3 connection string"))
        self.query.setPlaceholderText(_translate("SQLQueries", "Query"))
        self.execute.setText(_translate("SQLQueries", "Execute"))

