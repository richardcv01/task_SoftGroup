#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtSql
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog
from Qtwindow import Ui_MainWindow
import SQL_BD


class Thread_read_db(QtCore.QThread):
    table = pyqtSignal(QtSql.QSqlTableModel)
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        self.db.setDatabaseName('postgres')
        self.db.setHostName('localhost')
        self.db.setUserName('postgres')
        self.db.setPassword('user1')
        self.db.open()

    def run(self):
        self.query = QtSql.QSqlQuery()
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('tbl_data_get_html')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.table.emit(self.model)

class Thread_write_file(QtCore.QThread):
    json_text = pyqtSignal(str)
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.select = SQL_BD.select()

    def run(self):
        dic = {}
        try:
            for t in self.select:
                dic['id'] = t[0]
                dic['title'] = t[1]
                dic['url'] = t[2]
                dic['autor'] = t[3]
                dic['text'] = t[4]
                dic['price'] = t[5]
                dic['currency'] = t[6]
                self.json_text.emit(str(dic))
        except Exception as e:
            print(e)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.thread_read_db = Thread_read_db()
        self.thread_write_file = Thread_write_file()
        self.initUI()

    def initUI(self):
        self.btn_fill.clicked.connect(self.clicfill)
        self.btn_export.clicked.connect(self.clicexport)

    def clicfill(self):
        print('dsfsf')
        self.thread_read_db.start()
        self.thread_read_db.table[QtSql.QSqlTableModel].connect(self.select)

    def select(self,model):
        self.view = self.tableView
        self.view.setModel(model)

    def clicexport(self):
        self.name = QFileDialog.getSaveFileName(self, "Save file", QDir.currentPath(), ".json")
        with open(self.name[0] + self.name[1], 'w', encoding='utf-8') as file:
            file.write('')
        self.thread_write_file.start()
        self.thread_write_file.json_text[str].connect(self.export)

    def export(self,json):
        with open(self.name[0]+self.name[1],'a', encoding='utf-8') as file:
            file.write(json+'\n')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    sys.exit(app.exec_())