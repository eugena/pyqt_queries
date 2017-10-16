#!/usr/bin/python3

import sys
import sqlite3

from PyQt5.QtCore import Qt, pyqtSlot, QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from ui.main import Ui_SQLQueries

__appname__ = "SQL queries"


class TableModel(QAbstractTableModel):

    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent)
        self.list, self.header = args[:2]

    def rowCount(self, parent=None, *args, **kwargs):
        """
        rowCount(self, parent: QModelIndex = QModelIndex()) -> int
        """
        return len(self.list)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        columnCount(self, parent: QModelIndex = QModelIndex()) -> int
        """
        return len(self.header)

    def data(self, QModelIndex, role=None):
        """
        data(self, QModelIndex, role: int = Qt.DisplayRole) -> Any
        """
        if not QModelIndex.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.list[QModelIndex.row()][QModelIndex.column()]

    def headerData(self, p_int, Qt_Orientation, role=None):
        """
        headerData(self, int, Qt.Orientation, role: int = Qt.DisplayRole) -> Any
        """
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[p_int]
        return None


class MainWindow(QDialog, Ui_SQLQueries):
    def __init__(self):
        """
        Main Window initialization
        """
        super().__init__()
        self.setupUi(self)

        self._conn_open()

        # setting of signals
        self.connString.editingFinished.connect(self.update_conn)
        self.execute.clicked.connect(self.execute_query)

    @pyqtSlot()
    def update_conn(self):
        """
        Waiting for connection string changing
        :return: void
        """
        if self.conn:
            self.conn.close()
        self._conn_open()

    def _conn_open(self):
        """
        Oppens a connection to a database
        :return: void
        """
        try:
            self.conn = sqlite3.connect(self.connString.text())
        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, 'Operational Error', e.__str__())

    @pyqtSlot()
    def execute_query(self):
        """
        Executing a query on click Execute button
        :return: void
        """
        try:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            if not len(self.query.toPlainText()):
                raise sqlite3.OperationalError ("Can\'t execute empty query")

            cursor.execute(self.query.toPlainText())
            if cursor.description:
                model = TableModel(
                    None,
                    cursor.fetchall(),
                    [c[0] for c in cursor.description])
                self.results.setModel(model)
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


if __name__ == '__main__':
    QApplication.setApplicationName(__appname__)
    QApplication.setApplicationVersion("0.01")
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
