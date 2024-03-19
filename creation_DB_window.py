from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import pyqtSignal
import sqlite3
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
import sys
import os
from main_window import *
from main_window import create_table


class New_DB_Window(QWidget):

    window_closed2 = pyqtSignal()
    hide_signal2 = pyqtSignal()
    error_signal2 = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 200)
        self.setWindowTitle("Создать список")
        self.setStyleSheet("background-color: #EBF5FB;")
        LB = QtWidgets.QLabel(self)
        LB.setGeometry(80, 15, 200, 35)
        LB.setText("Введите название")
        font = LB.font()
        font.setPointSize(13)
        LB.setFont(font)
        self.LE_name = QLineEdit(self)
        self.LE_name.setGeometry(50, 50, 200, 30)
        font = self.LE_name.font()
        font.setPointSize(13)
        self.LE_name.setFont(font)
        style = "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;"
        self.LE_name.setStyleSheet(style)
        self.create_window()

    def create_window(self):
        btn_create_w3 = QPushButton('Создать список', self)
        btn_create_w3.setGeometry(100, 100, 100, 30)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px; 
}
"""
        btn_create_w3.setStyleSheet(style)
        btn_create_w3.clicked.connect(self.btn_create_DB)
        btn_create_w3.clicked.connect(self.hide_window2)

    def hide_window2(self):
        self.hide_signal2.emit()
        self.hide()

    def closeEvent(self, event):
        self.window_closed2.emit()
        event.accept()

    def btn_create_DB(self):
        text_LE = self.LE_name.text()
        self.my_dir = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            "/",
            QFileDialog.ShowDirsOnly
        )

        if text_LE != '' and self.my_dir != '':
            name = text_LE + '.db'
            entries = os.listdir(self.my_dir + '/')
            if name in entries:
                QMessageBox.critical(
                    self, "Ошибка ", "Файл с данным именем уже существует", QMessageBox.Ok)
                self.error_signal2.emit()
            else:
                file = open('path.txt', 'w')
                file.write(self.my_dir + '/' + name)
                file.close()
                create_table(self.my_dir + '/' + name)
