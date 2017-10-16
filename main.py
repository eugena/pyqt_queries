#!/usr/bin/python3

import re
import sys
import sqlite3

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from ui.main import Ui_SQLQueries

__appname__ = "SQL queries"

# Memory limits
__max_page_count__ = 195313
__page_size__ = 512

# Query limits
QUERY_LIMIT = 100


class MainWindow(QDialog, Ui_SQLQueries):
    def __init__(self):
        """
        Main Window initialization
        """
        super().__init__()
        self.setupUi(self)

        self.connString.setText(":memory:")
        self.conn = sqlite3.connect(self.connString.text())

        self.page.setMinimum(1)
        self.page.setMaximum(1)

        # setting of signals
        self.connString.editingFinished.connect(self.update_conn)
        self.execute.clicked.connect(self.execute_query)
        self.page.valueChanged.connect(self.execute_query)

    @pyqtSlot()
    def update_conn(self):
        """
        Waiting for connection string changing
        :return: void
        """
        if self.conn:
            self.conn.close()
        self.conn = sqlite3.connect(self.connString.text())

    @pyqtSlot()
    def execute_query(self):
        """
        Executing a query on click Execute button
        :return: void
        """
        try:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA max_page_count = %s" % __max_page_count__)
            cursor.execute("PRAGMA page_size = %s" % __page_size__)
            if not len(self.query.toPlainText()):
                raise sqlite3.OperationalError ("Can\'t execute empty query")
            model = QStandardItemModel()
            self.results.setModel(model)
            cursor.execute(self._query_decorator())
            self._update_page()
            row = cursor.fetchone()
            if isinstance(row, sqlite3.Row):
                if not model.columnCount():
                    model.setColumnCount(len(row.keys()))
                    model.setHorizontalHeaderLabels(row.keys())
                while row:
                    r = list()
                    for name in row:
                        item = QStandardItem(name.__str__())
                        item.setEditable(False)
                        r.append(item)
                    model.appendRow(r)
                    row = cursor.fetchone()
                self.results.setModel(model)
            else:
                self.conn.commit()
        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, 'Operational Error', '%s. %s' % (
                e.__str__(),
                "Please check the documentation https://www.sqlite.org/lang.html to correct the query."))
        except Exception as e:
            QMessageBox.critical(self, 'Error', e.__str__())
            raise e
        else:
            QMessageBox.information(self, 'Executed', 'It\'s Ok. Done!')

    def closeEvent(self, QCloseEvent):
        """
        Handling of closing of the Main dialog
        :param QCloseEvent:
        :return: void
        """
        super().closeEvent(QCloseEvent)
        self.conn.close()

    @staticmethod
    def _select_checker(query):
        return re.match(r'^select', query, flags=re.I)

    def _update_page(self):
        """
        Calculating quantity of rows in a table and setting a page number
        :return:
        """
        query = self.query.toPlainText()
        if MainWindow._select_checker(query):
            query = re.sub(r'^select .*(?=from)', 'select count(*) ',  query, flags=re.I)
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                row_count = cursor.fetchone()[0]
                self.page.setMaximum(int(row_count / QUERY_LIMIT))
            except (sqlite3.OperationalError, TypeError):
                self.page.setMaximum(1)

    def _query_decorator(self):
        """
        Decorating a SELECT query
        :return:
        """
        query = self.query.toPlainText()
        if MainWindow._select_checker(query):
            query = re.sub(r'limit.*', '', query, flags=re.I)
            query += ' LIMIT %s OFFSET %s' % (
                QUERY_LIMIT,
                (self.page.value() - 1) * QUERY_LIMIT)
        return query


if __name__ == '__main__':
    QApplication.setApplicationName(__appname__)
    QApplication.setApplicationVersion("0.01")
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
