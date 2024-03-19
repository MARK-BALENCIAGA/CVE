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
from PyQt5.QtWidgets import QFileDialog
import sys
import os
from main_window import *
import pandas as pd
from main_window import name_table


class Export_Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedSize(350, 380)
        self.setStyleSheet("background-color: #EBF5FB;")
        self.setWindowTitle("Экспорт")
        LB_main = QtWidgets.QLabel(self)
        LB_main.setGeometry(30, 15, 300, 35)
        LB_main.setText("Выберете поля для экспорта в Excel")
        font = LB_main.font()
        font.setPointSize(13)
        LB_main.setFont(font)

        self.cb_id = QCheckBox('id', self)
        self.cb_id.move(30, 50)
        self.cb_id.toggle()
        self.cb_id.setChecked(False)
        self.cb_id.show()

        self.cb_name = QCheckBox('Имя', self)
        self.cb_name.move(30, 80)
        self.cb_name.toggle()
        self.cb_name.setChecked(False)
        self.cb_name.show()

        self.cb_number = QCheckBox('Номер', self)
        self.cb_number.move(30, 110)
        self.cb_number.toggle()
        self.cb_number.setChecked(False)
        self.cb_number.show()

        self.cb_address = QCheckBox('Адрес', self)
        self.cb_address.move(30, 140)
        self.cb_address.toggle()
        self.cb_address.setChecked(False)
        self.cb_address.show()

        self.cb_org = QCheckBox('Организация', self)
        self.cb_org.move(30, 170)
        self.cb_org.toggle()
        self.cb_org.setChecked(False)
        self.cb_org.show()

        self.cb_birthday = QCheckBox('День рождения', self)
        self.cb_birthday.move(30, 200)
        self.cb_birthday.toggle()
        self.cb_birthday.setChecked(False)
        self.cb_birthday.show()

        self.cb_all = QCheckBox('Весь список', self)
        self.cb_all.move(30, 230)
        self.cb_all.toggle()
        self.cb_all.setChecked(False)
        self.cb_all.stateChanged.connect(self.all_cb_True)
        self.cb_all.show()

        self.LE_name_file = QLineEdit(self)
        self.LE_name_file.setPlaceholderText("Введите название файла")
        self.LE_name_file.setFocus()
        self.LE_name_file.setGeometry(30, 260, 250, 30)
        font = self.LE_name_file.font()
        font.setPointSize(13)
        self.LE_name_file.setFont(font)
        self.LE_name_file.setStyleSheet(
            "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;")

        btn_export = QPushButton('Экспорт', self)
        btn_export.setGeometry(30, 300, 150, 30)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px; 
}
"""
        btn_export.setStyleSheet(style)
        btn_export.clicked.connect(self.btn_export)

    def all_cb_True(self):
        self.cb_birthday.setChecked(True)
        self.cb_id.setChecked(True)
        self.cb_org.setChecked(True)
        self.cb_address.setChecked(True)
        self.cb_number.setChecked(True)
        self.cb_name.setChecked(True)

    def btn_export(self):
        self.my_dir = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            "/",
            QFileDialog.ShowDirsOnly
        )
        name_file = self.LE_name_file.text()
        command = []
        if self.cb_id.checkState():
            command.append('id')
        if self.cb_name.checkState():
            command.append('name')
        if self.cb_number.checkState():
            command.append('number')
        if self.cb_address.checkState():
            command.append('address')
        if self.cb_org.checkState():
            command.append('organization')
        if self.cb_birthday.checkState():
            command.append('birthday')
        if self.my_dir != '' and name_file != '':
            if len(command) != 0:
                str_headers = ", ".join(command)
                self.import_excel(str_headers, name_file)

    def import_excel(self, headers, fn):
        self.file_n = fn + '.xlsx'
        self.file_name = self.my_dir + "/" + fn + '.xlsx'
        if self.the_same_name():
            db_name = self.db_name_file()
            headers_name = headers.replace(',', '')
            list_headers = headers_name.split(' ')
            print(db_name)
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            list_all = []
            for i in range(len(list_headers)):
                c.execute(
                    "select " + list_headers[i] + " from " + name_table)
                ls = c.fetchall()
                temp = []
                temp = [i[0] for i in ls]
                list_all.append(temp)
            dictionary = dict(zip(list_headers, list_all))
            df = pd.DataFrame(dictionary)
            df.to_excel(self.file_name, sheet_name='Contacts', index=False)
            self.hide_window()

    def db_name_file(self):
        with open("path.txt") as file:
            str_path = file.readline()
        return str_path

    def the_same_name(self):
        entries = os.listdir(self.my_dir+"/")
        if self.file_n in entries:
            QMessageBox.critical(
                self, "Ошибка ", "Файл с данным именем уже существует", QMessageBox.Ok)
            return False
        return True

    def hide_window(self):
        self.hide()
