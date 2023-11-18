import sqlite3 
import sys
import time

conn = sqlite3.connect("POS SYSTEM.db")
c = conn.cursor()

###################################################################

Suppliers = "CREATE TABLE IF NOT EXISTS Suppliers ( Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT, Supplier_Name TEXT NOT NULL)"
c.execute(Suppliers)

Stock_Items = "CREATE TABLE IF NOT EXISTS Stock_Items ( Stock_ID INTEGER PRIMARY KEY AUTOINCREMENT, Name_Of_Stock_Item TEXT NOT NULL, Cost_Of_Bulk_Item INTEGER NOT NULL, Supplier_ID INTEGER NOT NULL, FOREIGN KEY (Supplier_ID) REFERENCES Suppliers(Supplier_ID))"
c.execute(Stock_Items)

Current_Stock_List = "CREATE TABLE IF NOT EXISTS Current_Stock_List ( Current_Stock_List_ID INTEGER PRIMARY KEY AUTOINCREMENT,Name_Of_CStock_Item TEXT NOT NULL, Spoil_Date DATE NOT NULL, Portions_Per_Bulk_Item INTEGER NOT NULL, Stock_Order_ID INTEGER,Stock_ID INTEGER, FOREIGN KEY (Stock_ID) REFERENCES Stock_Items(Stock_ID))"
c.execute(Current_Stock_List)

Menu_Items = "CREATE TABLE IF NOT EXISTS Menu_Items ( Menu_Item_ID INTEGER PRIMARY KEY AUTOINCREMENT, Menu_Name TEXT NOT NULL)"
c.execute(Menu_Items)

Ingredients = "CREATE TABLE IF NOT EXISTS Ingredients ( Ingredient_Name TEXT NOT NULL, Menu_Name TEXT NOT NULL, Stock_ID INTEGER, FOREIGN KEY (Menu_Name) REFERENCES Menu_Items(Menu_Name), FOREIGN KEY (Stock_ID) REFERENCES Stock_Items(Stock_ID))"
c.execute(Ingredients)


suppliername = input("\nEnter a supplier name\n").capitalize()
vars = (suppliername)
print("\nData Added To The Table.\n")
c.execute("INSERT INTO Suppliers (Supplier_Name) VALUES (?)", (vars,))


nameofsi = input("\nEnter the name of the stock item you wish to add\n").capitalize()
costofbi = input("\nEnter the price of the bulk item\n").capitalize()

sqlSupplierV = "SELECT * FROM Suppliers"
c.execute(sqlSupplierV)
supplieritems = c.fetchall()
print("\n\n\n\n\n\n\n\nSupplier Database View\n\n")
for item in supplieritems:
    print(item)
supplieridinput = (input("\nEnter the SupplierID from the list above\n"))

vars2 = (nameofsi, costofbi, supplieridinput)
print("\nData Added To The Table.\n")
sql = "INSERT INTO Stock_Items (Name_Of_Stock_Item, Cost_Of_Bulk_Item, Supplier_ID) VALUES (?,?,?)"
c.execute(sql, vars2)


numberofcurrentsi = input("\nEnter the name of the current stock item you wish to add\n")
spoildate = input("\n Enter the spoil date of the item")
portionperbi = input("\n Enter the portions of the item in bulk")

sqlStockItemV = "SELECT * FROM Stock_Items"
c.execute(sqlStockItemV)
stockitems = c.fetchall()
print("\n\n\n\n\n\n Stock Database View\n\n")
for item in stockitems:
    print(item)
stockidinput = (input("\nEnter the StockID from the list above\n"))

vars3 = (numberofcurrentsi, spoildate, portionperbi, stockidinput)
print("\nData Added To The Table.\n")
sql = "INSERT INTO Current_Stock_List (Name_Of_CStock_Item, Spoil_Date, Portions_Per_Bulk_Item, Stock_ID) VALUES (?,?,?,?)"
c.execute(sql, vars3)


menuname = input("\nEnter a menu item name\n").capitalize()
vars4 = (menuname)
print("\nData Added To The Table.\n")
c.execute("INSERT INTO Menu_Items (Menu_Name) VALUES (?)", (vars4,))


sqlMenuNameV = "SELECT * FROM Menu_Items"
c.execute(sqlMenuNameV)
menunamefetch = c.fetchall()
print("\n\n\n\n\n\n\nMenu Database View\n\n")
for item in menunamefetch:
    print(item)
menuinput = (input("\nEnter the Menu Item from the list above\n"))


ingn = input("\nEnter the name of the ingredient within the menu item\n")
vars5 = (menuinput, ingn)
print("\nData Added To The Table.\n")
sql = "INSERT INTO Ingredients ( INGMenu_Item_Name, Ingredient_Name) VALUES (?,?)"
c.execute(sql, vars5)

conn.commit()
