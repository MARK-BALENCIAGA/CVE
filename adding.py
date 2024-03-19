import ast

user_input = input("Input numbers: ")
result = eval(user_input)
print("REsult:", result)



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