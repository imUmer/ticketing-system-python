from PyQt5.QtWidgets import *
import sys
import csv
from docxtpl import DocxTemplate
from docxtpl import DocxTemplate
import datetime
from PyQt5.uic import loadUiType
import pandas as pd
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import os

cwd = os.getcwd()
# append the relative path of your file to the current working directory
loign_path = os.path.join(cwd, 'login.ui')
main_path = os.path.join(cwd, 'login.ui')

# open the file

ui_login,_  = loadUiType('./frontend/login.ui')                    
ui_main,_  = loadUiType('./frontend/main.ui')
role = ["",""]

class Login(QMainWindow, ui_login):
   
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_login.clicked.connect(self.check_login)
        self.pushButton_exit.clicked.connect(self.exit_app)
        self.messagelabel.setText('')

    def signup_user(self):
        self.username = self.textBox_username.text()
        self.password = self.textBox_password.text()

        if self.username != '' and self.password != '':
            lst = []
            with open("users.csv") as usersCsv:
                reader = csv.reader(usersCsv)
                for row in reader:
                    lst.append(row)

            lst.append([self.username, self.password,"1"])
            
            with open("users.csv", "w", newline='') as usersCsv:
                writer = csv.writer(usersCsv)
                writer.writerows(lst)

            self.messagelabel.setText('New User is Signed Up')
        else:
            self.messagelabel.setText('Please Enter username and password')
    def exit_app(self):
        sys.exit()

    def check_login(self):
        self.username = self.textBox_username.text()
        self.password = self.textBox_password.text()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name,role FROM users WHERE username=? AND password=? ", (self.username, self.password))
        result = c.fetchone()
        role.clear()
        conn.close()
        if result:
            self.messagelabel.setText('Logged in')
            role.append(result[0])
            role.append(result[1])
            windowMain.user_role()
            windowMain.show()
            window.hide()
            return True
        else:
            self.messagelabel.setText('Wrong username or password')
            return False
        

class MainApp (QMainWindow ,ui_main):
    def __init__(self, role):
        QMainWindow.__init__(self)
        self.setupUi(self) 
        self.lst = {"Select":"select the vendor"}
        self.invoice_list = []
        self.load_data_add_tickets(self.tableWidget)
        self.load_data(self.tableWidget_all_tickets)
        self.load_data(self.tableWidget_refund)
        self.load_data(self.tableWidget_invoice)
        self.load_data_vendors(self.tableWidget_ven)
        self.load_vendors()
        self.addItemsToCombo()
        self.lineEdit_sn.setText(str(self.get_sn()))
        print(self.stackedWidget)

        # Stacked 
        self.stacked_widget = self.stackedWidget 
        self.pushButton_add_tickets_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.pushButton_refund_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.pushButton_search_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.pushButton_invoices_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.pushButton_vendors_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.pushButton_settings_nav.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.pushButton_logout_nav.clicked.connect(self.logout)

        #Invoice 
        self.lineEdit_inv_searchbar.textChanged.connect(self.search_table_inv)
        self.pushButton_inv_print.clicked.connect( self.print_invoice)
        self.pushButton_inv_save.clicked.connect( self.save_invoice)
        self.tableWidget_invoice.cellClicked.connect(self.selectrow_invoice)
        
        # Vendors
        self.tableWidget_ven.cellClicked.connect(self.selectRow_vendors)
        self.lineEdit_ven_searchbar.textChanged.connect(self.search_table_ven)
        self.pushButton_ven_add.clicked.connect( self.adddata_ven)
        self.pushButton_ven_del.clicked.connect( self.remove_data_ven)
        self.pushButton_ven_update.clicked.connect( self.update_data_ven)

        # REFund PAnel 
        self.lineEdit_searchbar.textChanged.connect(self.search_table)
        self.tableWidget_refund.cellClicked.connect(self.selectRow_refund)
        self.pushButton_refund.clicked.connect(self.refund)

        # Add Tickets PAnel
        self.comboBox_vname.currentIndexChanged.connect(self.get_vendor_data)
        self.tableWidget.cellClicked.connect(self.selectRow)
        self.pushButton_add.clicked.connect( self.adddata)
        self.pushButton_rem.clicked.connect( self.remove_data)
        self.pushButton_update.clicked.connect( self.update_data)
        self.pushButton_submit.clicked.connect( self.submit_data)

        # All Tickets PAnel
        self.comboBox_vname_at.currentIndexChanged.connect(self.get_vendor_data_at)
        self.tableWidget_all_tickets.cellClicked.connect(self.selectRow_at)
        self.pushButton_add_at.clicked.connect( self.adddata_at)
        self.pushButton_rem_at.clicked.connect( self.remove_data_at)
        self.pushButton_update_at.clicked.connect( self.update_data_at)
        # self.pushButton_submit_at.clicked.connect( self.submit_data_at)

         # All Tickets PAnel
        self.comboBox_role.currentIndexChanged.connect(self.get_role_data)
        self.pushButton_user_add.clicked.connect(self.adddata_user)
        self.pushButton_user_rem.clicked.connect(self.remove_data_user)
        self.pushButton_user_update.clicked.connect( self.update_data_user)
        self.tableWidget_users.cellClicked.connect(self.selectRow_user)
        self.load_role()
        self.load_user_data()

    def user_role(self):
        if role[1] == 'employee':
            self.pushButton_settings_nav.hide()
            self.pushButton_settings_nav.setEnabled(True)
        else:
            self.pushButton_settings_nav.show()
            self.pushButton_settings_nav.setEnabled(True)

    # -----------------------  Start is Settings Area  ---------------------------

    def get_role_data(self):
        try:
            selected_item = self.comboBox_role.currentText()
            self.lst[selected_item]
            self.lineEdit_vcn_at.setText(self.lst[selected_item])
        except:
            pass
    
    def load_role(self):
        self.comboBox_role.addItem('Select the Role')
        self.comboBox_role.addItem('admin')
        self.comboBox_role.addItem('employee')

    def clearFileds_user(self): 
        self.label_user_id.setText("")
        self.lineEdit_user_name.setText("")
        self.lineEdit_user_un.setText("")
        self.lineEdit_user_pass.setText("")
        self.comboBox_role.setCurrentText("Select the Vendor")

    def update_data_user(self):
        id = self.label_user_id.text()
        name = self.lineEdit_user_name.text()
        un = self.lineEdit_user_un.text()
        pwd = self.lineEdit_user_pass.text()
        role = self.comboBox_role.currentText()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE users SET name=? ,username=?, password=?, role=?Where userid=? ", (name, un,pwd,  role, id))
        conn.commit()
        conn.close()
        self.load_user_data()

    def load_user_data(self):
        try:
            self.table = self.tableWidget_users
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            
            c.execute("SELECT * FROM users")
            rows = c.fetchall()
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table.setItem(i, j, item)
            conn.close()
        except:
            pass
        finally:
            print("no Data")

    def remove_data_user(self):
        selected_row = self.tableWidget_users.currentRow()

        if selected_row != -1:
            userid = self.tableWidget_users.item(selected_row, 0).text()
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM users WHERE userid=?", (userid))
            conn.commit()
            conn.close()
            self.load_user_data()
        
    def adddata_user(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            
            cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (userid INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, username TEXT, password TEXT, role TEXT
                            )''')
            id = self.label_user_id.text()
            name = self.lineEdit_user_name.text()
            un = self.lineEdit_user_un.text()
            pwd = self.lineEdit_user_pass.text()
            role = self.comboBox_role.currentText()

            sql = f"INSERT INTO users (name ,username, password, role) VALUES ('{name}', '{un}','{pwd}', '{role}')"
            r = cursor.execute(sql)
            conn.commit()

        except sqlite3.Error as e:
            # handle the exception
            print(f"An error occurred: {e}")

        finally:
            # close the connection        
            conn.close()
            self.clearFileds_user()
            self.load_user_data()
    
    def selectRow_user(self):
        selected_row = self.tableWidget_users.currentRow()
        if selected_row >= 0:
            id = self.tableWidget_users.item(selected_row, 0).text()
            name = self.tableWidget_users.item(selected_row, 1).text()
            un = self.tableWidget_users.item(selected_row, 2).text()
            pwd = self.tableWidget_users.item(selected_row, 3).text()
            role = self.tableWidget_users.item(selected_row, 4).text()

            # set the values to line edits
            self.label_user_id.setText(id)
            self.lineEdit_user_name.setText(name)
            self.lineEdit_user_un.setText(un)
            self.lineEdit_user_pass.setText(pwd)
            self.comboBox_role.setCurrentText(role)

    


    # -----------------------  End is Settings Area  ---------------------------
    # -----------------------  Start is All Tickets Area  ---------------------------
    def get_vendor_data_at(self):
        try:
            selected_item = self.comboBox_vname_at.currentText()
            self.lst[selected_item]
            self.lineEdit_vcn_at.setText(self.lst[selected_item])
        except:
            pass

    def clearFileds_at(self): 
        self.lineEdit_date_at.setText("")
        self.lineEdit_pname_at.setText("")
        self.lineEdit_pcn_at.setText("")
        self.lineEdit_tpnr_at.setText("")
        self.lineEdit_s_at.setText("")
        self.lineEdit_fare_at.setText("")
        self.lineEdit_tax_at.setText("")
        self.lineEdit_sales_at.setText("")
        self.comboBox_vname_at.setCurrentText("Select the Vendor")
        self.lineEdit_vcn_at.setText("")
        self.label_entry_at.setText("")

    def update_data_at(self):
        sn = self.lineEdit_sn_at.text()
        date = self.lineEdit_date_at.text()
        pname = self.lineEdit_pname_at.text()
        pc = self.lineEdit_pcn_at.text()
        ticketpnr = self.lineEdit_tpnr_at.text()
        sector = self.lineEdit_s_at.text()
        fare = self.lineEdit_fare_at.text()
        taxes = self.lineEdit_tax_at.text()
        net = str(int(fare) + int(taxes))
        refund = str(0)
        sales = self.lineEdit_sales_at.text()
        gop = str(int(sales) - int(net))
        total = gop
        vendor = self.comboBox_vname_at.currentText()
        contact = self.lineEdit_vcn_at.text()
        ticketid = self.label_entry_at.text()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE tickets SET sn=? ,date=?, pname=?, pc=?, ticketpnr=?, sector=?, fare=?, taxes=?, net=?, refund=?, sales=?, gop=?, total=?, vendor=?, contact=? Where ticketid=? ", (sn, date,pname,  pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact,ticketid))
        # c.execute("UPDATE tickets SET sn=? ,date=?, pname=?, pc=?, ticketpnr=?, sector=?, fare=?, taxes=?, net=?, refund=?, sales=?, gop=?, total=?, vendor=?, contact=? Where ticketid=? ", (sn, date,pname,  pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact,ticketid))
        conn.commit()
        conn.close()
        self.load_data(self.tableWidget_all_tickets)

    def remove_data_at(self):
        selected_row = self.tableWidget_all_tickets.currentRow()

        if selected_row != -1:
            ticketid = self.tableWidget_all_tickets.item(selected_row, 0).text()
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM tickets WHERE ticketid=?", (ticketid))
            conn.commit()
            conn.close()
            self.load_data(self.tableWidget_all_tickets)
        
    def adddata_at(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS tickets 
                            (ticketid INTEGER PRIMARY KEY AUTOINCREMENT, sn INTEGER, date TEXT, pname TEXT, pc TEXT, ticketpnr TEXT
                                , sector TEXT, fare TEXT, taxes TEXT, net TEXT
                                , refund TEXT, sales TEXT, gop TEXT, total TEXT, vendor TEXT, contact TEXT
                            )''')
            
            sn = self.lineEdit_sn_at.text()
            date = self.lineEdit_date_at.text()
            pname = self.lineEdit_pname_at.text()
            pc = self.lineEdit_pcn_at.text()
            ticketpnr = self.lineEdit_tpnr_at.text()
            sector = self.lineEdit_s_at.text()
            fare = self.lineEdit_fare_at.text()
            taxes = self.lineEdit_tax_at.text()
            net = str(int(fare) + int(taxes))
            refund = str(0)
            sales = self.lineEdit_sales_at.text()
            gop = str(int(sales) - int(net))
            total = gop
            vendor = self.comboBox_vname_at.currentText()
            contact = self.lineEdit_vcn_at.text()

            # new_user = ('John Doe', 'johndoe@example.com')
            # cursor.execute("INSERT INTO tickets (pname, pc, ticketpnr, sector, date, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", new_user)
            # sql = f"INSERT INTO addtickets (sn ,date, pname, pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES ('{sn}', '{date}','{pname}', '{pc}', '{ticketpnr}', '{sector}', '{fare}', '{taxes}', '{net}', '{refund}', '{sales}', '{gop}', '{total}', '{vendor}', '{contact}')"
            sql2 = f"INSERT INTO tickets (sn ,date, pname, pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES ('{sn}', '{date}','{pname}', '{pc}', '{ticketpnr}', '{sector}', '{fare}', '{taxes}', '{net}', '{refund}', '{sales}', '{gop}', '{total}', '{vendor}', '{contact}')"
            # r = cursor.execute(sql)
            r = cursor.execute(sql2)
            conn.commit()

        except sqlite3.Error as e:
            # handle the exception
            print(f"An error occurred: {e}")

        finally:
            # close the connection        
            conn.close()
            self.clearFileds_at()
            self.load_data(self.tableWidget_all_tickets)
    
    def selectRow_at(self):
        selected_row = self.tableWidget_all_tickets.currentRow()
        if selected_row >= 0:
            id = self.tableWidget_all_tickets.item(selected_row, 0).text()
            sn = self.tableWidget_all_tickets.item(selected_row, 1).text()
            date = self.tableWidget_all_tickets.item(selected_row, 2).text()
            pname = self.tableWidget_all_tickets.item(selected_row, 3).text()
            pc = self.tableWidget_all_tickets.item(selected_row, 4).text()
            ticketpnr = self.tableWidget_all_tickets.item(selected_row, 5).text()
            sector = self.tableWidget_all_tickets.item(selected_row, 6).text()
            fare = self.tableWidget_all_tickets.item(selected_row, 7).text()
            taxes = self.tableWidget_all_tickets.item(selected_row, 8).text()
            # net = self.tableWidget_all_tickets.item(selected_row, 7).text()
            # refund = self.tableWidget_all_tickets.item(selected_row, 8).text()
            sales = self.tableWidget_all_tickets.item(selected_row, 11).text()
            # gop = self.tableWidget_all_tickets.item(selected_row, 10).text()
            # total = self.tableWidget_all_tickets.item(selected_row, 11).text()
            vendor = self.tableWidget_all_tickets.item(selected_row, 14).text()
            contact = self.tableWidget_all_tickets.item(selected_row, 15).text()

            # set the values to line edits
            self.label_entry_at.setText(id)
            self.lineEdit_sn_at.setText(sn)
            self.lineEdit_pname_at.setText(pname)
            self.lineEdit_pcn_at.setText(pc)
            self.lineEdit_tpnr_at.setText(ticketpnr)
            self.lineEdit_s_at.setText(sector)
            self.lineEdit_date_at.setText(date)
            self.lineEdit_fare_at.setText(fare)
            self.lineEdit_tax_at.setText(taxes)
            # self.lineEdit_n.setText(net)
            # self.lineEdit_refun.setText(refund)
            self.lineEdit_sales_at.setText(sales)
            # self.lineEdit_gop.setText(gop)
            # self.lineEdit_total.setText(total)
            self.comboBox_vname_at.setCurrentText(vendor)
            self.lineEdit_vcn_at.setText(contact)


    # -----------------------  End is All Tickets Area  ---------------------------
    
    # -----------------------  Start is Invoice Area  ---------------------------
    def add_item(self):
        for row in range(self.tableWidget_invoice.rowCount()):
            row_data = []
            for column in range(self.tableWidget_invoice.columnCount()):
                cell_value = self.tableWidget_invoice.item(row, column).text()
                row_data.append(cell_value)
            pname = row_data[3]
            service = self.lineEdit_inv_s.text()
            sec = row_data[6]
            tdate = self.lineEdit_inv_tdate.text()
            ftax = int(row_data[7]) + int(row_data[8])
            t = ftax
            invoice_item = [pname, service, sec, tdate,ftax,t] 
            self.invoice_list.append(invoice_item)

    def selectrow_invoice(self):
        selected_row = self.tableWidget_invoice.currentRow()
        if selected_row >= 0:
            invoice = self.tableWidget_invoice.item(selected_row, 1).text()

            # set the values to line edits
            self.label_inv_si.setText(invoice)
            self.onselect_invoice()
   

    def save_invoice(self):
        if self.label_inv_si.text() != '0':
            self.add_item()
            doc = DocxTemplate("invoice_template.docx")
            cname = self.lineEdit_inv_cn.text()
            invoiceno = self.label_inv_si.text()
            sperson = self.lineEdit_inv_sp.text()
            mop = self.comboBox_payment_method.currentText()
            date =  datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
            subtotal = sum(item[5] for item in self.invoice_list) 
            total = subtotal
            
            doc.render({
                    "cname":cname, 
                    "sperson":sperson,
                    "invoiceno":invoiceno,
                    "mop" : mop,
                    "date" : date,
                    "invoice_list": self.invoice_list,
                    "subtotal":subtotal,
                    "total":total})
            
            doc_name = "" + cname +" "+ datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".docx"
            doc.save(doc_name)
            print("Invoice Complete", "Invoice Complete") 
            self.clear_invoice()

    def clear_invoice(self):
        self.invoice_list.clear()
        self.lineEdit_inv_cn.setText("")
        self.lineEdit_inv_s.setText("")
        self.lineEdit_inv_sp.setText("")
        self.lineEdit_inv_tdate.setText("")
        self.label_inv_si.setText("0")
        self.comboBox_payment_method.setCurrentText("Select Payment Method")
        self.load_data(self.tableWidget_invoice)

    # -----------------------  End of Invoice Area  ---------------------------




    def addItemsToCombo(self):
        self.comboBox_payment_method.addItem("Select Payment Method")
        self.comboBox_payment_method.addItem("Cash")
        self.comboBox_payment_method.addItem("Dabit Card")

    def print_invoice(self):
        pass
    def onselect_invoice(self):
        try:
            self.table = self.tableWidget_invoice
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            if self.label_inv_si.text() != '0':
                c.execute(f"SELECT * FROM tickets WHERE sn LIKE '%{self.label_inv_si.text()}%' ")
                # """
                # SELECT invoice.invoiceid, tickets.sn, tickets.pname, tickets.pc, tickets.ticket, tickets.sector
                # FROM invoice
                # INNER JOIN tickets ON invoice.sn = tickets.sn;
                # """
                rows = c.fetchall()
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, col in enumerate(row):
                        item = QTableWidgetItem(str(col))
                        self.table.setItem(i, j, item)
            else:
                self.load_data(self.tableWidget_invoice)
                print(f"No data!!")
        except:
            # handle the exception
            print(f"An error occurred: ")

        finally:
            # close the connection        
            conn.close()

    def search_table_inv(self):
        try:
            self.table = self.tableWidget_invoice
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            if self.lineEdit_inv_searchbar.text() != '':
                c.execute(f"SELECT * FROM tickets WHERE sn LIKE '%{self.lineEdit_inv_searchbar.text()}%' ")
                # """
                # SELECT invoice.invoiceid, tickets.sn, tickets.pname, tickets.pc, tickets.ticket, tickets.sector
                # FROM invoice
                # INNER JOIN tickets ON invoice.sn = tickets.sn;
                # """
                rows = c.fetchall()
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, col in enumerate(row):
                        item = QTableWidgetItem(str(col))
                        self.table.setItem(i, j, item)
            else:
                self.load_data(self.tableWidget_invoice)
                print(f"No data!!")
        except:
            # handle the exception
            print(f"An error occurred: ")

        finally:
            # close the connection        
            conn.close()

    def search_table_ven(self):
        try:
            self.table = self.tableWidget_ven
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            if self.lineEdit_ven_searchbar.text() != '':
                c.execute(f"SELECT * FROM VENDORS WHERE vcontact LIKE '%{self.lineEdit_ven_searchbar.text()}%'")
                
                rows = c.fetchall()
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, col in enumerate(row):
                        item = QTableWidgetItem(str(col))
                        self.table.setItem(i, j, item)
            else:
                self.load_data_vendors(self.tableWidget_ven)
                print(f"No data!!")
        except:
            # handle the exception
            print(f"An error occurred: ")

        finally:
            # close the connection        
            conn.close()
    
    def update_data_ven(self):
        venid = self.label_ven_id.text()
        name = self.lineEdit_ven_name.text()
        contact = self.lineEdit_ven_contact.text()
        address = self.lineEdit_ven_address.text()
        email = self.lineEdit_ven_email.text()
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE vendors SET vname=? ,vcontact=?, vaddress=?, vemail=? Where venid=? ", (name,  contact, address, email, venid))
        conn.commit()
        conn.close()
        self.load_data_vendors(self.tableWidget_ven)
        self.load_vendors()

    def remove_data_ven(self):
        selected_row = self.tableWidget_ven.currentRow()

        if selected_row != -1:
            id = self.tableWidget_ven.item(selected_row, 0).text()
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM vendors WHERE venid={id}")
            conn.commit()
            conn.close()
            self.load_data_vendors(self.tableWidget_ven)
            self.load_vendors()
        
    def adddata_ven(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS vendors 
                            (venid INTEGER PRIMARY KEY AUTOINCREMENT, vname TEXT, vcontact TEXT, vaddress TEXT, vemail TEXT
                            )''')

            name = self.lineEdit_ven_name.text()
            contact = self.lineEdit_ven_contact.text()
            address = self.lineEdit_ven_address.text()
            email = self.lineEdit_ven_email.text()

            sql = f"INSERT INTO vendors (vname, vcontact, vaddress, vemail) VALUES ('{name}', '{contact}','{address}','{email}')"
            r = cursor.execute(sql)
            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()
            self.load_data_vendors(self.tableWidget_ven)
            self.load_vendors()

    def search_table(self):
        # self.cursor.execute(f"SELECT * FROM TICKETS WHERE ticketpnr LIKE '%{self.lineEdit_searchbar.text()}%' OR pc LIKE '%{self.lineEdit_searchbar.text()}%'")
        # data = self.cursor.fetchall()
        # self.table.setRowCount(0)
        # for row_num, row_data in enumerate(data):
        #     self.table.insertRow(row_num)
        #     for col_num, col_data in enumerate(row_data):
        #         item = self.tableWidget(str(col_data))
        #         item.setTextAlignment(Qt.AlignCenter)
        #         self.table.setItem(row_num, col_num, item)
        try:
            self.table = self.tableWidget_refund
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            if self.lineEdit_searchbar.text() != '':
                c.execute(f"SELECT * FROM TICKETS WHERE ticketpnr LIKE '%{self.lineEdit_searchbar.text()}%'")
                
                rows = c.fetchall()
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, col in enumerate(row):
                        item = QTableWidgetItem(str(col))
                        self.table.setItem(i, j, item)
            else:
                self.load_data(self.tableWidget_refund)
                print(f"No data!!")
        except:
            # handle the exception
            print(f"An error occurred: ")

        finally:
            # close the connection        
            conn.close()

    def selectRow_refund(self):
        selected_row = self.tableWidget_refund.currentRow()
        if selected_row >= 0:
            id = self.tableWidget_refund.item(selected_row, 0).text()
            sn = self.tableWidget_refund.item(selected_row, 1).text()
            date = self.tableWidget_refund.item(selected_row, 2).text()
            pname = self.tableWidget_refund.item(selected_row, 3).text()
            pc = self.tableWidget_refund.item(selected_row, 4).text()
            ticketpnr = self.tableWidget_refund.item(selected_row, 5).text()
            sector = self.tableWidget_refund.item(selected_row, 6).text()
            fare = self.tableWidget_refund.item(selected_row, 7).text()
            taxes = self.tableWidget_refund.item(selected_row, 8).text()
            net = self.tableWidget_refund.item(selected_row, 9).text()
            # refund = self.tableWidget.item(selected_row, 8).text()
            sales = self.tableWidget_refund.item(selected_row, 11).text()
            # gop = self.tableWidget.item(selected_row, 10).text()
            total = self.tableWidget_refund.item(selected_row, 13).text() 

            # set the values to line edits
            self.label_entry_id.setText(id)
            self.label_date.setText(date)
            # self.lineEdit_sn.setText(sn)
            self.label_pn.setText(pname)
            self.label_pcn.setText(pc)
            self.label_tpnr.setText(ticketpnr)
            self.label_s.setText(sector)
            self.label_f.setText(fare)
            self.label_tax.setText(taxes)
            self.label_net.setText(net)
            self.label_sale.setText(sales)
            self.label_total.setText(total)

    def refund(self):
        conn = sqlite3.connect('database.db')
        try:
            if self.lineEdit_refund_cash.text() !='': 
                # fare = self.lineEdit_fare.text()
                # taxes = self.lineEdit_tax.text()
                # net = str(int(fare) + int(taxes))
                refund = self.lineEdit_refund_cash.text()
                sales = self.label_sale.text()
                total = str(int(sales) - int(refund))
                ticketid = int(self.label_entry_id.text())
                c = conn.cursor()
                # c.execute("UPDATE tickets SET taxes=?, net=?, refund=?, sales=?, gop=?, total=?, vendor=?, contact=? Where ticketid=? ", (sn, date,pname,  pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact,ticketid))
                c.execute(f"UPDATE tickets SET refund='{refund}', total='{total}' Where ticketid={ticketid} ")
                conn.commit()
                
        except sqlite3.Error as e:
            # handle the exception
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            self.load_data(self.tableWidget_refund)
        

    def selectRow(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            id = self.tableWidget.item(selected_row, 0).text()
            sn = self.tableWidget.item(selected_row, 1).text()
            date = self.tableWidget.item(selected_row, 2).text()
            pname = self.tableWidget.item(selected_row, 3).text()
            pc = self.tableWidget.item(selected_row, 4).text()
            ticketpnr = self.tableWidget.item(selected_row, 5).text()
            sector = self.tableWidget.item(selected_row, 6).text()
            fare = self.tableWidget.item(selected_row, 7).text()
            taxes = self.tableWidget.item(selected_row, 8).text()
            # net = self.tableWidget.item(selected_row, 7).text()
            # refund = self.tableWidget.item(selected_row, 8).text()
            sales = self.tableWidget.item(selected_row, 11).text()
            # gop = self.tableWidget.item(selected_row, 10).text()
            # total = self.tableWidget.item(selected_row, 11).text()
            vendor = self.tableWidget.item(selected_row, 14).text()
            contact = self.tableWidget.item(selected_row, 15).text()

            # set the values to line edits
            self.label_entry.setText(id)
            self.lineEdit_sn.setText(sn)
            self.lineEdit_pname.setText(pname)
            self.lineEdit_pcn.setText(pc)
            self.lineEdit_tpnr.setText(ticketpnr)
            self.lineEdit_s.setText(sector)
            self.lineEdit_date.setText(date)
            self.lineEdit_fare.setText(fare)
            self.lineEdit_tax.setText(taxes)
            # self.lineEdit_n.setText(net)
            # self.lineEdit_refun.setText(refund)
            self.lineEdit_sales.setText(sales)
            # self.lineEdit_gop.setText(gop)
            # self.lineEdit_total.setText(total)
            self.comboBox_vname.setCurrentText(vendor)
            self.lineEdit_vcn.setText(contact)

    def selectRow_vendors(self):
        selected_row = self.tableWidget_ven.currentRow()
        if selected_row >= 0:
            id = self.tableWidget_ven.item(selected_row, 0).text()
            name = self.tableWidget_ven.item(selected_row, 1).text()
            contact = self.tableWidget_ven.item(selected_row, 2).text()
            address = self.tableWidget_ven.item(selected_row, 3).text()
            email = self.tableWidget_ven.item(selected_row, 4).text()

            # set the values to line edits
            self.label_ven_id.setText(id)
            self.lineEdit_ven_name.setText(name)
            self.lineEdit_ven_contact.setText(contact)
            self.lineEdit_ven_address.setText(address)
            self.lineEdit_ven_email.setText(email)

    def get_vendor_data(self):
        try:
            selected_item = self.comboBox_vname.currentText()
            self.lst[selected_item]
            self.lineEdit_vcn.setText(self.lst[selected_item])
        except:
            pass
    def load_vendors(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT vname,vcontact FROM vendors')
        data = c.fetchall()
        self.lst["select"] = "select the vendor"
        self.comboBox_vname.clear()
        self.comboBox_vname_at.clear()

        # Add data to combobox
        for item in data:
            self.lst[item[0]] = item[1]
            self.comboBox_vname.addItem(item[0])
            self.comboBox_vname_at.addItem(item[0])

        # Close database connection
        conn.close()

    def load_data_vendors(self, table):
        self.table = table
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendors'")
        r = c.fetchone()
        if r:
            c.execute("SELECT * FROM vendors")
            rows = c.fetchall()
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table.setItem(i, j, item)
            conn.close()
            
    def load_data(self, table):
        self.table = table
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
        r = c.fetchone()
        if r:
            c.execute("SELECT * FROM tickets")
            rows = c.fetchall()
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table.setItem(i, j, item)
            conn.close()

    def load_data_add_tickets(self, table):
        self.table = table
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='addtickets'")
        r = c.fetchone()
        if r:
            c.execute("SELECT * FROM addtickets")
            rows = c.fetchall()
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table.setItem(i, j, item)
            conn.close()

    def submit_data(self):
        sn = self.lineEdit_sn.text()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO invoice (sn) Values ({sn}) ")
        conn.commit()
        conn.close()
        self.tableWidget.setRowCount(0)
        self.removeall() 
        self.lineEdit_sn.setText(str(self.get_sn()))
        self.clearFileds()  
        self.load_data(self.tableWidget_refund)
        
    def clearFileds(self): 
        self.lineEdit_date.setText("")
        self.lineEdit_pname.setText("")
        self.lineEdit_pcn.setText("")
        self.lineEdit_tpnr.setText("")
        self.lineEdit_s.setText("")
        self.lineEdit_fare.setText("")
        self.lineEdit_tax.setText("")
        self.lineEdit_sales.setText("")
        self.comboBox_vname.setCurrentText("Select the Vendor")
        self.lineEdit_vcn.setText("")
        self.label_entry.setText("")

    def removeall(self):
        sn = self.lineEdit_sn.text()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"DROP TABLE addtickets")
        conn.commit()
        conn.close()

    def get_sn(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Get the maximum invoice number from the database
        cursor.execute("SELECT MAX(sn) FROM invoice")
        result = cursor.fetchone()[0]

        if result is None:
            # If there are no invoices in the database, start from 1000
            invoice_number = 1000
        else:
            # Increment the maximum invoice number by 1 to generate a new invoice number
            invoice_number = result + 1

        conn.close()

        return invoice_number
        
    def update_data(self):
        sn = self.lineEdit_sn.text()
        date = self.lineEdit_date.text()
        pname = self.lineEdit_pname.text()
        pc = self.lineEdit_pcn.text()
        ticketpnr = self.lineEdit_tpnr.text()
        sector = self.lineEdit_s.text()
        fare = self.lineEdit_fare.text()
        taxes = self.lineEdit_tax.text()
        net = str(int(fare) + int(taxes))
        refund = str(0)
        sales = self.lineEdit_sales.text()
        gop = str(int(sales) - int(net))
        total = gop
        vendor = self.comboBox_vname.currentText()
        contact = self.lineEdit_vcn.text()
        ticketid = self.label_entry.text()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE addtickets SET sn=? ,date=?, pname=?, pc=?, ticketpnr=?, sector=?, fare=?, taxes=?, net=?, refund=?, sales=?, gop=?, total=?, vendor=?, contact=? Where ticketid=? ", (sn, date,pname,  pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact,ticketid))
        # c.execute("UPDATE tickets SET sn=? ,date=?, pname=?, pc=?, ticketpnr=?, sector=?, fare=?, taxes=?, net=?, refund=?, sales=?, gop=?, total=?, vendor=?, contact=? Where ticketid=? ", (sn, date,pname,  pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact,ticketid))
        conn.commit()
        conn.close()
        self.load_data_add_tickets(self.tableWidget)

    def remove_data(self):
        selected_row = self.tableWidget.currentRow()

        if selected_row != -1:
            ticketid = self.tableWidget.item(selected_row, 0).text()
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM addtickets WHERE ticketid=?", (ticketid))
            conn.commit()
            conn.close()
            self.load_data_add_tickets(self.tableWidget)
        
    def adddata(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS addtickets 
                            (ticketid INTEGER PRIMARY KEY AUTOINCREMENT, sn INTEGER, date TEXT, pname TEXT, pc TEXT, ticketpnr TEXT
                                , sector TEXT, fare TEXT, taxes TEXT, net TEXT
                                , refund TEXT, sales TEXT, gop TEXT, total TEXT, vendor TEXT, contact TEXT
                            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS tickets 
                            (ticketid INTEGER PRIMARY KEY AUTOINCREMENT, sn INTEGER, date TEXT, pname TEXT, pc TEXT, ticketpnr TEXT
                                , sector TEXT, fare TEXT, taxes TEXT, net TEXT
                                , refund TEXT, sales TEXT, gop TEXT, total TEXT, vendor TEXT, contact TEXT
                            )''')
            
            sn = self.lineEdit_sn.text()
            date = self.lineEdit_date.text()
            pname = self.lineEdit_pname.text()
            pc = self.lineEdit_pcn.text()
            ticketpnr = self.lineEdit_tpnr.text()
            sector = self.lineEdit_s.text()
            fare = self.lineEdit_fare.text()
            taxes = self.lineEdit_tax.text()
            net = str(int(fare) + int(taxes))
            refund = str(0)
            sales = self.lineEdit_sales.text()
            gop = str(int(sales) - int(net))
            total = gop
            vendor = self.comboBox_vname.currentText()
            contact = self.lineEdit_vcn.text()

            # new_user = ('John Doe', 'johndoe@example.com')
            # cursor.execute("INSERT INTO tickets (pname, pc, ticketpnr, sector, date, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", new_user)
            sql = f"INSERT INTO addtickets (sn ,date, pname, pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES ('{sn}', '{date}','{pname}', '{pc}', '{ticketpnr}', '{sector}', '{fare}', '{taxes}', '{net}', '{refund}', '{sales}', '{gop}', '{total}', '{vendor}', '{contact}')"
            sql2 = f"INSERT INTO tickets (sn ,date, pname, pc, ticketpnr, sector, fare, taxes, net, refund, sales, gop, total, vendor, contact) VALUES ('{sn}', '{date}','{pname}', '{pc}', '{ticketpnr}', '{sector}', '{fare}', '{taxes}', '{net}', '{refund}', '{sales}', '{gop}', '{total}', '{vendor}', '{contact}')"
            r = cursor.execute(sql)
            r = cursor.execute(sql2)
            conn.commit()

        except sqlite3.Error as e:
            # handle the exception
            print(f"An error occurred: {e}")

        finally:
            # close the connection        
            conn.close()
            self.clearFileds()
            self.load_data_add_tickets(self.tableWidget)

   
    def logout(self):
        window.show()
        role.clear()
        windowMain.hide()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    windowMain = MainApp(role)  
    # windowMain.show()
    app.exec_()
