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
from main_window import *
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
import sys
import os
name_table = 'phone_numbers'


class New_Contact_Window(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    window_closed = pyqtSignal()
    hide_signal = pyqtSignal()
    error_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFixedSize(550, 350)
        self.setStyleSheet("background-color: #EBF5FB;")
        self.setWindowTitle("Создать список")
        LB_name = QtWidgets.QLabel(self)
        LB_name.setGeometry(130, 15, 80, 35)
        LB_name.setText("Имя")
        font = LB_name.font()
        font.setPointSize(13)
        LB_name.setFont(font)

        self.LE_name = QLineEdit(self)
        self.LE_name.setGeometry(50, 50, 200, 30)
        font = self.LE_name.font()
        font.setPointSize(13)
        self.LE_name.setFont(font)
        style = "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;"
        self.LE_name.setStyleSheet(style)

        LB_number = QtWidgets.QLabel(self)
        LB_number.setGeometry(120, 95, 80, 35)
        LB_number.setText("Номер")
        LB_number.setFont(font)

        self.LE_number = QLineEdit(self)
        self.LE_number.setGeometry(50, 130, 200, 30)
        self.LE_number.setFont(font)
        self.LE_number.setStyleSheet(style)

        LB_address = QtWidgets.QLabel(self)
        LB_address.setGeometry(120, 175, 80, 35)
        LB_address.setText("Адрес")
        LB_address.setFont(font)

        self.LE_address = QLineEdit(self)
        self.LE_address.setGeometry(50, 210, 200, 30)
        self.LE_address.setFont(font)
        self.LE_address.setStyleSheet(style)

        LB_org = QtWidgets.QLabel(self)
        LB_org.setGeometry(350, 15, 150, 35)
        LB_org.setText("Организация")
        font = LB_org.font()
        font.setPointSize(13)
        LB_org.setFont(font)

        self.LE_org = QLineEdit(self)
        self.LE_org.setGeometry(300, 50, 200, 30)
        font = self.LE_org.font()
        font.setPointSize(13)
        self.LE_org.setFont(font)
        style = "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;"
        self.LE_org.setStyleSheet(style)

        LB_birthday = QtWidgets.QLabel(self)
        LB_birthday.setGeometry(340, 95, 150, 35)
        LB_birthday.setText("День рождения")
        font = LB_birthday.font()
        font.setPointSize(13)
        LB_birthday.setFont(font)

        self.LE_birthday = QLineEdit(self)
        self.LE_birthday.setGeometry(300, 130, 200, 30)
        font = self.LE_birthday.font()
        font.setPointSize(13)
        self.LE_birthday.setFont(font)
        style = "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;"
        self.LE_birthday.setStyleSheet(style)

        btn_add_w2 = QPushButton('Создать контакт', self)
        btn_add_w2.setGeometry(75, 270, 150, 30)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px; 
}
"""
        btn_add_w2.setStyleSheet(style)
        btn_add_w2.clicked.connect(self.btn_addition_add)
        btn_add_w2.clicked.connect(self.hide_window)

    def hide_window(self):
        self.hide_signal.emit()
        self.hide()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

    def btn_addition_add(self):
        name = self.LE_name.text()
        number = self.LE_number.text()
        address = self.LE_address.text()
        organization = self.LE_org.text()
        birthday = self.LE_birthday.text()
        if (name != '' or number != '' or address != ''):
            self.add_records(name, number, address, organization, birthday)

    def add_records(self, name, number, address, organization, birthday):
        model2 = QSqlTableModel(self)
        model2.setTable(name_table)
        rec = model2.record()
        rec.setValue("name", name)
        rec.setValue("number", number)
        rec.setValue("address", address)
        rec.setValue("organization", organization)
        rec.setValue("birthday", birthday)
        model2.insertRecord(-1, rec)
