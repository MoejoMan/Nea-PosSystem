import sys
import os
import sqlite3
import time
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets

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

Login = "CREATE TABLE IF NOT EXISTS Login (Username TEXT NOT NULL PRIMARY KEY, Password TEXT NOT NULL)"
c.execute(Login)

conn.commit()

###################################################################

class Login(QDialog): 
    def __init__(self):
        super(Login,self).__init__()
        loadUi("loginscreen.ui",self)
        self.login_button.clicked.connect(self.loginfunction)
        self.logpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_button.clicked.connect(self.gotocreate)
            

    def loginfunction(self):
        user = self.username
        adminlog = self.logpassword
        
        if user == "Joe" and adminlog == "1234":
            admindash = AdminDash()
            widget.addWidget(admindash)
            widget.setCurrentIndex(widget.currentIndex()+1)
            email = self.username.text()
            password = self.logpassword.text()
            print("Sucessfully logged in with: ", email, "and password: ", password)
        else:
            dash = DashScreen()
            widget.addWidget(dash)
            widget.setCurrentIndex(widget.currentIndex()+1)
            email = self.username.text()
            password = self.logpassword.text()
            print("Sucessfully logged in with: ", email, "and password: ", password)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AdminDash(QMainWindow):
    def __init__(self):
        super(AdminDash,self).__init()
        loadUi("AdminDash.ui",self)
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class DashScreen(QMainWindow): 
    def __init__(self):
        super(DashScreen,self).__init__()
        loadUi("dashboard2.ui",self)
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        self.push1.clicked.connect(self.change)

    def change(self):
        self.menu=["6oz Ribeye Steak","Texas Burger","Gammon Steak","Tuna Steak","Beef Wellington","Sunday Roast","Full English","Sausage Egg","Chilli","Mixed Veg","Loaded Fries","S and P Fries","Water","Pinot Grigio","Pinot Noir","Sauvingon Blanc","Malbec","Riesling",]

        self.prices=["15.50","14.10","12.00","12.00","21.50","11.45","10.50","10.00","9.00","3.50","5.75","5.50","0.00","12.00","12.00","12.00","12.00","12.00",]

        label = self.I1

        #if (self.push1).isChecked():
            #for n in range(1, 9): self.I1 = getattr(self, f'I{n}'); self.push1 = getattr(self, f'push{n}')
            # label[y].setText(str(self.menu[0]))
            

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("signupscreen.ui",self)
        self.signup_button.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def createaccfunction(self):
        if self.password.text()==self.confirmpassword.text():

            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

# main
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec()