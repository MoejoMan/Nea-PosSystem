import sys
import os
import sqlite3
import time
import PyQt5
import hashlib
import NewIcons
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QProgressDialog, QMessageBox, QPushButton, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):   
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

conn = sqlite3.connect("POS SYSTEM.db")
c = conn.cursor()

###################################################################

Suppliers = "CREATE TABLE IF NOT EXISTS Suppliers ( Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT, Supplier_Name TEXT NOT NULL)"
c.execute(Suppliers)

Stock_Items = "CREATE TABLE IF NOT EXISTS Stock_Items ( Stock_ID INTEGER PRIMARY KEY AUTOINCREMENT, Name_Of_Stock_Item TEXT NOT NULL, Cost_Of_Bulk_Item INTEGER NOT NULL, Supplier_ID INTEGER NOT NULL, FOREIGN KEY (Supplier_ID) REFERENCES Suppliers(Supplier_ID))"
c.execute(Stock_Items)

Current_Stock_List = "CREATE TABLE IF NOT EXISTS Current_Stock_List ( Current_Stock_List_ID INTEGER PRIMARY KEY AUTOINCREMENT,Name_Of_CStock_Item TEXT NOT NULL, Spoil_Date DATE NOT NULL, Portions_Per_Bulk_Item INTEGER NOT NULL,FOREIGN KEY (Stock_ID) REFERENCES Stock_Items(Stock_ID))"
c.execute(Current_Stock_List)

Menu_Items = "CREATE TABLE IF NOT EXISTS Menu_Items ( Menu_Item_ID INTEGER PRIMARY KEY AUTOINCREMENT, Menu_Name TEXT NOT NULL)"
c.execute(Menu_Items)

Ingredients = "CREATE TABLE IF NOT EXISTS Ingredients ( Ingredient_Name TEXT NOT NULL, Menu_Item_ID INTEGER NOT NULL, Stock_ID INTEGER, FOREIGN KEY (Menu_Item_ID) REFERENCES Menu_Items(Menu_Item_ID), FOREIGN KEY (Stock_ID) REFERENCES Stock_Items(Stock_ID))"
c.execute(Ingredients)

Login = "CREATE TABLE IF NOT EXISTS Login (Username TEXT NOT NULL, Password TEXT NOT NULL)"
c.execute(Login)

FoodTable = "CREATE TABLE IF NOT EXISTS FoodTables (Food TEXT, Price INTEGER)"
c.execute(FoodTable)

Admins = "CREATE TABLE IF NOT EXISTS Admins (Username TEXT NOT NULL, Password TEXT NOT NULL)"
c.execute(Admins)

# drop = "DROP TABLE IF EXISTS Login ";
# c.execute(drop)


conn.commit()

###################################################################
class SplashScreen(QMainWindow):
    def __init__(self, widget):
        super(SplashScreen, self).__init__()
        loadUi("splashscreen.ui", self)
        widget.setFixedSize(325, 200)

        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)  
        self.show()

    def update_progress(self):
        value = self.progressBar.value() + 1
        self.progressBar.setValue(value)
        if value == 100:
            self.timer.stop()
            self.hide()
            login_screen = Login()
            login_widget = QtWidgets.QWidget()
            login_widget.setLayout(QVBoxLayout())
            login_widget.layout().addWidget(login_screen)
            login_widget.setFixedSize(400, 400)
            widget.addWidget(login_widget)
            widget.setCurrentIndex(widget.currentIndex() + 1)

class AdminDashScreen(QMainWindow): 
    def __init__(self):
        super(AdminDashScreen, self).__init__()
        loadUi("admindashboard.ui", self)
        widget.setFixedSize(800, 460)
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

        self.backButton.clicked.connect(self.goBackToLogin)
        # self.clearButton.clicked.connect(self.clearTable)
        # self.deleteButton.clicked.connect(self.deleteItem)
        # self.printButton.clicked.connect(self.printReceipt)
        # self.notesButton.clicked.connect(self.takeNotes)

        # self.OrderTable.setColumnWidth(0, 100)
        # self.OrderTable.setColumnWidth(1, 270)
        # self.OrderTable.setHorizontalHeaderLabels(["Orders"])
        # self.loaddata()

    def goBackToLogin(self):
        login_screen = Login()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedSize(400, 400)
        self.hide() 
        self.close()


class Login(QDialog): 
    def __init__(self):
        super(Login,self).__init__()
        loadUi("loginscreen.ui",self)
        self.login_button.clicked.connect(self.loginfunction)
        self.logpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_button.clicked.connect(self.gotocreate)
        self.setFixedSize(400, 400)

    
    def loginfunction(self):
        username = self.username.text()
        password = self.logpassword.text()

        is_admin = self.check_admin_credentials(username, password)

        if self.username.text() == "" and self.logpassword.text() == "":
            self.lbl_noaccount.setText("Username and Password fields are empty")

        elif self.username.text() == "":
            self.lbl_noaccount.setText("Username field is empty")

        elif self.logpassword.text() == "":
            self.lbl_noaccount.setText("Password field is empty")

        elif is_admin:
            admin_dash = AdminDashScreen()
            widget.addWidget(admin_dash)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            passcode = "SELECT Password FROM Login WHERE Username = (?)"
            c.execute(passcode, [username])
            fetch = c.fetchone()

            hashed_password = hashlib.sha256(password.encode('ascii')).hexdigest()

            try:
                if fetch is not None and hashed_password == str(fetch[0]):
                    dash = DashScreen()
                    widget.addWidget(dash)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    self.lbl_noaccount.setText("Username or Password is incorrect")
            except:
                self.lbl_noaccount.setText("An error occurred during login")

    def check_admin_credentials(self, username, password):
        admin_query = "SELECT * FROM Admins WHERE Username = ? AND Password = ?"
        c.execute(admin_query, [username, hashlib.sha256(password.encode('ascii')).hexdigest()])
        admin_fetch = c.fetchone()
        return admin_fetch is not None


    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class DashScreen(QMainWindow): 
    def __init__(self):
        super(DashScreen,self).__init__()
        loadUi("dashboard3.ui",self)
        widget.setFixedSize(800, 460)
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

        c.execute("DELETE FROM FoodTables")
        conn.commit()

        self.OrderTable.setSelectionBehavior(QTableWidget.SelectRows)

        self.varprice = 0

        self.timer = QTimer(self)

        self.push1.clicked.connect(partial(self.order,"6oz Ribeye Steak", 20))
        self.push2.clicked.connect(partial(self.order,"Texas Burger", 15))
        self.push3.clicked.connect(partial(self.order,"Gammon Steak", 18))
        self.push4.clicked.connect(partial(self.order,"Tuna Steak", 19))
        self.push5.clicked.connect(partial(self.order,"Beef Wellington", 25))
        self.push6.clicked.connect(partial(self.order,"Sunday Roast", 18))
        self.push7.clicked.connect(partial(self.order,"Full English", 15))
        self.push8.clicked.connect(partial(self.order,"Sausage, Egg", 13))
        self.push9.clicked.connect(partial(self.order,"Chilli", 15))
        self.push10.clicked.connect(partial(self.order,"Mixed Veg", 3))
        self.push11.clicked.connect(partial(self.order,"Loaded Fries", 5))
        self.push12.clicked.connect(partial(self.order,"S and P Fries", 4))
        self.push13.clicked.connect(partial(self.order,"Water", 0))
        self.push14.clicked.connect(partial(self.order,"Pinot Grigio", 20))
        self.push15.clicked.connect(partial(self.order,"Pinot Noir", 20))
        self.push16.clicked.connect(partial(self.order,"Sauvingon Blanc", 20))
        self.push17.clicked.connect(partial(self.order,"Malbec", 20))
        self.push18.clicked.connect(partial(self.order,"Riesling", 20))

        self.backButton.clicked.connect(self.goBackToLogin)
        self.clearButton.clicked.connect(self.clearTable)
        self.deleteButton.clicked.connect(self.deleteItem)
        self.printButton.clicked.connect(self.printReceipt)
        self.notesButton.clicked.connect(self.takeNotes)

        
        self.OrderTable.setColumnWidth(0, 100)
        self.OrderTable.setColumnWidth(1, 270)
        self.OrderTable.setHorizontalHeaderLabels(["Orders"])
        self.loaddata()

    def goBackToLogin(self):
        login_screen = Login()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedSize(400, 400)
        self.hide() 
        self.close()

    def loaddata(self):
        c.execute("SELECT * FROM FoodTables")
        results = c.fetchall()
        self.OrderTable.setRowCount(len(results))
        for row_index, row in enumerate(results):
            item = QTableWidgetItem(row[0])
            self.OrderTable.setItem(row_index, 0, item)


    def order(self, food, price):
        sql = "INSERT INTO FoodTables (Food, Price) VALUES (?, ?)"
        params = [food, price]
        c.execute(sql, params)
        conn.commit()
        self.varprice += price
        self.PriceLabel.setText("Total = £" + str(self.varprice))
        self.loaddata()
    

    def clearTable(self):
        num_rows = self.OrderTable.rowCount()
        if num_rows == 0:
            warning_box = QMessageBox(QMessageBox.Warning, "Warning", "No items in the table to clear.")
            warning_box.setStyleSheet("QMessageBox { background-color: white; }")
            warning_box.exec_()
            return

        c.execute("DELETE FROM FoodTables")
        conn.commit()

        self.OrderTable.clearContents()
        self.OrderTable.setRowCount(0)
        self.varprice = 0
        self.PriceLabel.setText("Total = £0")

    def deleteItem(self):
        num_rows = self.OrderTable.rowCount()
        if num_rows == 0:
            warning_box = QMessageBox(QMessageBox.Warning, "Warning", "No items to delete.")
            warning_box.setStyleSheet("QMessageBox { background-color: white; }")
            warning_box.exec_()
            return

        item = self.OrderTable.takeItem(num_rows - 1, 0)
        if item is not None:
            food_to_delete = item.text()
            c.execute("SELECT Price FROM FoodTables WHERE Food=? ORDER BY ROWID DESC LIMIT 1", [food_to_delete])
            deleted_item_price_result = c.fetchone()

            if deleted_item_price_result is not None:
                deleted_item_price = deleted_item_price_result[0]
            else:
                deleted_item_price = 0

            self.OrderTable.removeRow(num_rows - 1)
            self.varprice -= deleted_item_price
            self.PriceLabel.setText("Total = £" + str(self.varprice))
            c.execute("DELETE FROM FoodTables WHERE ROWID IN (SELECT ROWID FROM FoodTables WHERE Food=? ORDER BY ROWID DESC LIMIT 1)", [food_to_delete])
            conn.commit()

        else:
            QMessageBox.warning(self, "Warning", "No item in the last row.")



    def printReceipt(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Printing Receipt")
        message_box.setText("Receipt is being printed.")
        cancel_button = QPushButton("Cancel")
        message_box.addButton(cancel_button, QMessageBox.RejectRole)
        cancel_button.clicked.connect(message_box.reject)
        result = message_box.exec_()
        if result == QMessageBox.RejectRole:
            print("Printing canceled")
            timer = QTimer(self)
            timer.timeout.connect(self.showSecondMessageBox)
            timer.start(3000)

    def showSecondMessageBox(self):
        self.sender().disconnect()
        second_message_box = QMessageBox()
        second_message_box.setIcon(QMessageBox.Information)
        second_message_box.setWindowTitle("Receipt Printed")
        second_message_box.setText("Receipt has been printed.")
        second_message_box.exec_()
        
    
    def takeNotes(self):
        white_background_widget = QWidget(self)
        white_background_widget.setStyleSheet("background-color: white;")
        note, okPressed = QInputDialog.getText(white_background_widget, "Add Note", "Enter your note:", QLineEdit.Normal, "")

        if okPressed and note.strip():
            selected_rows = self.OrderTable.selectionModel().selectedRows()

            if selected_rows:
                selected_row = selected_rows[0].row()
                self.OrderTable.setItem(selected_row, 1, QTableWidgetItem(note))
            else:
                white_background_widget_warning = QWidget(self)
                white_background_widget_warning.setStyleSheet("background-color: white;")
                QMessageBox.warning(white_background_widget_warning, "Warning", "Select a row in the OrderTable to add a note.")



class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("signupscreen.ui",self)
        self.signup_button.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
 
    
    def createaccfunction(self):
        email = self.username.text()
        password = self.password.text()

        CheckCustomerAlreadyExists = "SELECT COUNT(*) FROM Login WHERE username = (?)"
        c.execute(CheckCustomerAlreadyExists, [self.username.text()])
        result = c.fetchone()
        if result[0] > 0:
            self.ErrorLabel.setText("Username Already Exists") 

        elif self.username.text() == "" and self.password.text() == "" and self.confirmpassword.text() == "":
            self.ErrorLabel.setText("Username and Password must be entered")

        elif self.password.text()!=self.confirmpassword.text():
            self.ErrorLabel.setText("Password and Confirm Password fields must be the same") 

        elif self.password.text() == "" or self.confirmpassword.text() == "":
            self.ErrorLabel.setText("Password must be entered") 

        elif self.username.text() == "":
            self.ErrorLabel.setText("Username must be entered")

        elif self.password.text()==self.confirmpassword.text():
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)


            password = self.password.text()
            password = hashlib.sha256(password.encode('ascii')).hexdigest()
            password = str(password)
            vars = (email,password)
            sql = "INSERT INTO Login (Username, Password) VALUES (?,?)"
            c.execute(sql, vars)
            conn.commit()
        
# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.show()

splash = SplashScreen(widget)
widget.addWidget(splash)
app.exec()





