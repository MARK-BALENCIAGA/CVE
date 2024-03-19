import sys
import os
import sqlite3
from creation_DB_window import *
from creation_contact_window import *
from creation_excel_file import *
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QCheckBox
name_table = 'phone_numbers'
import re
import subprocess
import sqlite3
import pickle

command = input("Enter a command to execute: ")
os.system(command)

user_input = input("Enter a Python expression to evaluate: ")
try:
    result = eval(user_input)
    print(f"Result:\n{result}")
except Exception as e:
    print(f"Error:\n{e}")

def sanitize_input(user_input):
    # A simple example: Allow only alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9]', '', user_input)

command = "ls"
directory = input("Which directory to list? ")
subprocess.run([command, directory])


command = input("Enter the directory to list: ")
subprocess.run(f"ls {command}", shell=True)

domain = input("Enter the Domain: ")
output = subprocess.check_output(f"nslookup {domain}", shell=True, encoding='UTF-8')

def get_user(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    connection.close()
    return user

username = input("Введите имя пользователя: ")
user = get_user(username)
if user:
    print("Пользователь найден:", user)
else:
    print("Пользователь не найден.")




class Main_Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ongoing = False
        self.setWindowTitle("Электронный телефонный справочник")
        self.setFixedSize(1000, 600)
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setGeometry(QtCore.QRect(200, 130, 800, 441))
        self.setStyleSheet("background-color: #EBF5FB;")
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        try:
            file = open('path.txt', 'r')
        except IOError:
            file = open('path.txt', 'w')
            file.close()
        with open("path.txt") as file:
            self.path_str_defult = file.readline()
        self.createConnection()

    def design_table(self):
        self.model = QSqlTableModel(self)
        self.model.setTable(name_table)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(1, Qt.Horizontal, "Имя ↓")
        self.model.setHeaderData(2, Qt.Horizontal, "Номер")
        self.model.setHeaderData(3, Qt.Horizontal, "Адрес")
        self.model.setHeaderData(4, Qt.Horizontal, "Организация")
        self.model.setHeaderData(5, Qt.Horizontal, "День рождения")
        self.model.select()
        self.view = QtWidgets.QTableView(self.groupBox)
        self.view.horizontalHeader().sectionClicked.connect(self.chose_column)
        self.view.setModel(self.model)
        self.view.setColumnHidden(0, True)
        self.view.setColumnHidden(4, True)
        self.view.setColumnHidden(5, True)
        self.view.setColumnWidth(1, 150)
        self.view.setColumnWidth(2, 150)
        self.view.setColumnWidth(3, 150)
        self.view.setColumnWidth(4, 150)
        self.view.setColumnWidth(5, 150)
        self.view.isCornerButtonEnabled()
        self.view.setStyleSheet(
            "QTableCornerButton::section{border-width: 0px;  border-style:solid; background:#EBF5FB; }QHeaderView::section { background-color:#EBF5FB; font-size:11pt; border-width: 1px;border-style: solid; border-color: #D6EAF8;}")
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.view.setFont(font2)
        self.setCentralWidget(self.view)
        self.choose_sort_type(1)
        self.run_btns()


def create_table(path_file):
    global name_table
    conn = sqlite3.connect(path_file)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS """ + name_table + """ (
        id INTEGER PRIMARY KEY,
        name TEXT CHECK (length("name") <= 40),
        number TEXT CHECK (length("number") <= 11),
        address TEXT CHECK (length("address") <= 40),
        organization TEXT CHECK (length("organization") <= 40),
        birthday TEXT CHECK (length("birthday") <= 40));
        """)
    get_column_names = conn.execute(
        """select * from """ + name_table + """ limit 1""")
    col_name = [i[0] for i in get_column_names.description]
    if (col_name[0] != 'id' or col_name[1] != 'name' or col_name[2] != 'number' or col_name[3] != 'address' or col_name[4] != 'organization' or col_name[5] != 'birthday'):
        name_table = name_table + '1'
        create_table(path_file)
    conn.commit()


class Class_Buttons(Main_Window, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.index = 0

    def createConnection(self):
        global name_table
        self.ongoing = False

        with open("path.txt") as file:
            self.path_str = file.readline()
        self.con.setDatabaseName(self.path_str)
        if not self.con.open():
            QMessageBox.critical(
                None,
                "QTableView Example - Error!",
                "Database Error: %s" % self.con.lastError().databaseText(),
            )

        self.design_table()

    def run_btns(self):
        self.btn_delete()
        self.btn_add()
        self.search_widgets()
        self.btn_open_DB()
        self.btn_new_DB()
        self.btn_del_search()
        self.under_line()
        self.initUI()
        self.name_DB()
        self.checkBoxes()
        self.btn_export()

    def initUI(self):
        self.label = QLabel(self)
        self.pixmap = QPixmap('telephone.png')
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(650, 300, 256, 256)
        self.label.show()

    def checkBoxes(self):
        self.cb_org = QCheckBox('Организация', self)
        self.cb_org.move(630, 20)
        self.cb_org.toggle()
        self.cb_org.setChecked(False)
        self.cb_org.stateChanged.connect(self.hide_columns)
        self.cb_org.show()

        self.cb_birthday = QCheckBox('День рождения', self)
        self.cb_birthday.move(730, 20)
        self.cb_birthday.toggle()
        self.cb_birthday.setChecked(False)
        self.cb_birthday.stateChanged.connect(self.hide_columns)
        self.cb_birthday.show()

    def under_line(self):
        labelA = QtWidgets.QLabel(self)
        labelA.setGeometry(0, 595, 900, 30)
        labelA.setStyleSheet("background-color : #EBF5FB;")
        labelA.show()

    def btn_export(self):
        self.button_export = QPushButton('Экспорт', self)
        self.button_export.setToolTip('Экспорт списка в Excel')
        self.button_export.setGeometry(837, 24, 70, 25)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.button_export.setStyleSheet(style)
        self.button_export.clicked.connect(self.show_new_window3)
        self.button_export.show()

    def btn_delete(self):
        self.button_delete = QPushButton('Удалить', self)
        self.button_delete.setToolTip('Удалить выделенный контакт')
        self.button_delete.setGeometry(825, 180, 80, 35)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.button_delete.setStyleSheet(style)
        self.button_delete.clicked.connect(self.delete_row)
        self.button_delete.show()

    def btn_add(self):
        self.button_add = QPushButton('Новый контакт', self)
        self.button_add.setToolTip('Создать новый контакт')
        self.button_add.setGeometry(630, 120, 100, 35)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.button_add.setStyleSheet(style)
        self.button_add.clicked.connect(self.show_new_window)
        self.button_add.show()

    def btn_del_search(self):
        self.button_del_search = QPushButton("x", self)
        self.button_del_search.setToolTip('Очистить поле поиска')
        self.button_del_search.setGeometry(930, 63, 20, 23)
        style = """QPushButton:pressed {
    background-color: #D5D8DC;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 5px;
}
"""
        self.button_del_search.setStyleSheet(style)
        self.button_del_search.clicked.connect(self.del_search)
        self.button_del_search.clicked.connect(self.LE_search.clear)
        self.button_del_search.show()

    def choose_sort_type(self, column):
        self.AscendingOrder_sort(
            column) if not self.ongoing else self.DescendingOrder_sort(column)
        self.ongoing = not self.ongoing

    def search_widgets(self):
        self.LE_search = QLineEdit(self)
        self.LE_search.setPlaceholderText("Введите текст для поиска")
        self.LE_search.setFocus()
        self.LE_search.setGeometry(630, 60, 280, 30)
        font = self.LE_search.font()
        font.setPointSize(13)
        self.LE_search.setFont(font)
        self.LE_search.setStyleSheet(
            "border : 2px solid #808B96; border-radius : 3px; background-color : #F8F9F9;")
        self.btn_search = QPushButton('Поиск', self)
        self.btn_search.setGeometry(825, 120, 80, 35)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.btn_search.setStyleSheet(style)
        self.btn_search.clicked.connect(self.view_search)
        self.LE_search.show()
        self.btn_search.show()

    def btn_open_DB(self):
        self.btn_open_new_DB = QPushButton('Открыть список', self)
        self.btn_open_new_DB.setToolTip('Открыть другой список контактов')
        self.btn_open_new_DB.setGeometry(630, 240, 100, 35)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.btn_open_new_DB.setStyleSheet(style)
        self.btn_open_new_DB.clicked.connect(self.getFilePath)
        self.btn_open_new_DB.show()

    def getFilePath(self):  # move to MW!!!!
        self.filename, format = QFileDialog.getOpenFileName(
            self, "Выбрать файл", ".", "DB(*.db)")
        if self.filename != '':

            file = open('path.txt', 'w')
            file.write(self.filename)
            file.close()
            create_table(self.filename)

        self.createConnection()

    def name_DB(self):
        self.LB_name_DB = QtWidgets.QLabel(self)
        self.LB_name_DB.setGeometry(825, 240, 80, 35)
        name_db = ''

        with open("path.txt") as file:
            path_str = file.readline()

        if path_str != '':
            i = len(path_str) - 1
            count = 0
            name_db = ""
            while path_str[i] != '/':
                i -= 1
                if i == 0:
                    count = 1
                    break
            if count == 1:
                name_db = path_str[:-3]
            else:
                name_db = path_str[i+1:-3]
        self.LB_name_DB.setText(name_db)
        font = self.LB_name_DB.font()
        font.setPointSize(13)
        self.LB_name_DB.setFont(font)
        self.LB_name_DB.setStyleSheet(
            "border : 0px solid #808B96; border-radius : 3px; ")
        self.LB_name_DB.show()

    def btn_new_DB(self):
        self.button_create = QPushButton('Новый список', self)
        self.button_create.setToolTip('Создать новый список контактов')
        self.button_create.setGeometry(630, 180, 100, 35)
        style = """QPushButton:pressed {
    background-color: #D5D8DC ;
}
QPushButton {
     background-color: #E9F7EF ; border: 2px solid #808B96;
     border-radius: 4px;
}
"""
        self.button_create.setStyleSheet(style)
        self.button_create.clicked.connect(self.show_window_create_DB)
        self.button_create.show()


class Class_Functions(Class_Buttons):
    def __init__(self, parent=None):
        super().__init__(parent)

    def hide_columns(self):
        if self.cb_birthday.checkState() and not self.cb_org.checkState():
            self.view.setColumnHidden(4, True)
            self.view.setColumnHidden(5, False)
            self.move_widgets_back()
        elif not self.cb_birthday.checkState() and not self.cb_org.checkState():
            self.view.setColumnHidden(4, True)
            self.view.setColumnHidden(5, True)
            self.move_widgets_back()
        elif not self.cb_birthday.checkState() and self.cb_org.checkState():
            self.view.setColumnHidden(4, False)
            self.view.setColumnHidden(5, True)
            self.move_widgets_back()
        elif self.cb_birthday.checkState() and self.cb_org.checkState():
            self.view.setColumnHidden(4, False)
            self.view.setColumnHidden(5, False)
            self.move_widgets()
            self.button_del_search.setGeometry(1090, 63, 20, 23)

    def move_widgets(self):
        self.setFixedSize(1120, 600)
        self.button_del_search.setGeometry(1090, 63, 20, 23)
        self.label.setGeometry(800, 300, 256, 256)
        self.button_delete.setGeometry(1000, 180, 80, 35)
        self.button_add.setGeometry(800, 120, 100, 35)
        self.LE_search.setGeometry(800, 60, 280, 30)
        self.btn_search.setGeometry(1000, 120, 80, 35)
        self.btn_open_new_DB.setGeometry(800, 240, 100, 35)
        self.LB_name_DB.setGeometry(1000, 240, 80, 35)
        self.button_create.setGeometry(800, 180, 100, 35)
        self.button_del_search.setGeometry(1180, 63, 20, 23)
        self.cb_org.move(800, 20)
        self.cb_birthday.move(900, 20)
        self.button_export.setGeometry(1007, 24, 70, 25)

    def move_widgets_back(self):
        self.setFixedSize(1000, 600)
        self.cb_org.move(630, 20)
        self.cb_birthday.move(730, 20)
        self.label.setGeometry(650, 300, 256, 256)
        self.button_delete.setGeometry(825, 180, 80, 35)
        self.button_add.setGeometry(630, 120, 100, 35)
        self.button_del_search.setGeometry(930, 63, 20, 23)
        self.LE_search.setGeometry(630, 60, 280, 30)
        self.btn_search.setGeometry(825, 120, 80, 35)
        self.btn_open_new_DB.setGeometry(630, 240, 100, 35)
        self.LB_name_DB.setGeometry(825, 240, 80, 35)
        self.button_create.setGeometry(630, 180, 100, 35)
        self.button_export.setGeometry(837, 24, 70, 25)

    def delete_row(self):
        self.index = self.view.currentIndex()
        self.model.deleteRowFromTable(self.index.row())
        self.model.submitAll()
        self.model.select()

    def show_new_window(self):  # def show_new_window(self, checked):
        self.window = None
        if self.window is None:
            self.window = New_Contact_Window()
        self.window.window_closed.connect(self.update_table)
        self.window.hide_signal.connect(self.update_table)
        self.window.error_signal.connect(self.show_new_window)
        self.window.show()

    def show_new_window3(self):
        self.window = None
        if self.window is None:
            self.window = Export_Window()
        self.window.show()

    def update_table(self):
        self.model.select()

    def del_search(self):
        strwhere = "name like '%' "
        self.model.setFilter(strwhere)
        self.model.select()

    def AscendingOrder_sort(self, column):
        self.model.setSort(column, Qt.AscendingOrder)
        if (column == 1):
            self.model.setHeaderData(1, Qt.Horizontal, "Имя ↑")
            self.model.setHeaderData(2, Qt.Horizontal, "Номер")
        if (column == 2):
            self.model.setHeaderData(2, Qt.Horizontal, "Номер ↑")
            self.model.setHeaderData(1, Qt.Horizontal, "Имя")
        self.model.select()

    def DescendingOrder_sort(self, column):
        self.model.setSort(column, Qt.DescendingOrder)
        if (column == 1):
            self.model.setHeaderData(1, Qt.Horizontal, "Имя ↓")
            self.model.setHeaderData(2, Qt.Horizontal, "Номер")
        if (column == 2):
            self.model.setHeaderData(2, Qt.Horizontal, "Номер ↓")
            self.model.setHeaderData(1, Qt.Horizontal, "Имя")
        self.model.select()

    def view_search(self):
        global name_table
        str_text = self.LE_search.text()
        strwhere = "name LIKE '%" + str_text + "%' OR address LIKE '%" + str_text + """%' OR number LIKE '%""" + str_text + \
            """%' OR organization LIKE '%""" + str_text + \
            """%' OR birthday LIKE '%""" + str_text + "%'"
        if str_text == '':
            self.model.select()
        else:
            self.model.setFilter(strwhere)
            self.model.select()

        with open("path.txt") as file:
            path_file = file.readline()
        conn = sqlite3.connect(path_file)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM """ + name_table +
                    """ WHERE name LIKE '%""" + str_text + """%' OR number LIKE '%""" + str_text + """%' OR address LIKE '%""" + str_text + """%' OR organization LIKE '%""" + str_text + """%' OR birthday LIKE '%""" + str_text + """%'""")
        record = cur.fetchall()
        if len(record) == 0:
            self.no_results()
        cur.close()

    def no_results(self):
        QMessageBox.critical(
            self, "Поиск", "Результатов поиска не найдено", QMessageBox.Ok)

    def show_window_create_DB(self):
        self.window = None
        if self.window is None:
            self.window = New_DB_Window()
        self.window.window_closed2.connect(self.createConnection)
        self.window.hide_signal2.connect(self.createConnection)
        self.window.error_signal2.connect(self.show_window_create_DB)
        self.window.show()

    def chose_column(self, col_num):
        if col_num == 1:
            self.choose_sort_type(col_num)
        elif col_num == 2:
            self.choose_sort_type(col_num)


def name_table_return():
    return name_table


def create_main_window():
    app = QApplication(sys.argv)
    win = Class_Functions()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    create_main_window()
