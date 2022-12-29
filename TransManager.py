
import tkinter as tk
import tkinter.messagebox as mb  
from tkinter import ttk

from datetime import datetime
from pathlib import Path

import sqlite3
import pandas as pd

import TransManager_BudgetWindow as TM_BW
import TransManager_DefaultWindow as TM_DW

# create a connection
db_connection = sqlite3.connect('TransManagerDB.db')

# creating database_cursor to perform SQL operation   
db_cursor = db_connection.cursor()

# turn off pandas warnings for dataframe updates, default='warn'
pd.options.mode.chained_assignment = None

#
# Class - Main
#

class TransManager(tk.Tk):

    def __init__(self):  
        super().__init__()  

        # Verify or create the CSV files
        self.verify_create_csv()
        
        # Global Data Frames
        self.transactions_df = pd.DataFrame()
        self.recordcount = 0

        self.title("Transaction Manager v1")  
        self.lblTitle = tk.Label(self, text="Transaction Manager v1", font=("Tahoma", 16)) 
        self.geometry("900x600")
        self.resizable(0, 0)

        # configure the standard grid
        self.columnconfigure(0, weight=1, uniform="TransUX")
        self.columnconfigure(1, weight=1, uniform="TransUX")
        self.columnconfigure(2, weight=1, uniform="TransUX")
        self.columnconfigure(3, weight=1, uniform="TransUX")
        self.columnconfigure(4, weight=1, uniform="TransUX")
        self.columnconfigure(5, weight=1, uniform="TransUX")
        self.columnconfigure(6, weight=1, uniform="TransUX")

        # configure the standard grid
        self.rowconfigure(20, weight=1, uniform="TransUX")
        self.rowconfigure(21, weight=1, uniform="TransUX")
        self.rowconfigure(22, weight=1, uniform="TransUX")
        self.rowconfigure(23, weight=1, uniform="TransUX")
        self.rowconfigure(24, weight=1, uniform="TransUX")
        self.rowconfigure(25, weight=1, uniform="TransUX")
        self.rowconfigure(26, weight=1, uniform="TransUX")
        self.rowconfigure(27, weight=1, uniform="TransUX")
        self.rowconfigure(28, weight=1, uniform="TransUX")

        self.lblSpace = tk.Label(self, text=" ", width=100)
        self.lblDate = tk.Label(self, text="Transaction Date:")   
        self.lblOriginalDesc = tk.Label(self, text="Original Desc:")  
        self.lblAmount = tk.Label(self, text="Transaction Amount:")  
        self.lblType = tk.Label(self, text="Transaction Type:") 
        self.lblAccount = tk.Label(self, text="Bank Account:")  
        self.lblDefaultCategory = tk.Label(self, text="Default Category:")  
        self.lblUserCategory = tk.Label(self, text="User Category:")
        self.lblUserNotes = tk.Label(self, text="User Notes:")  
        self.lblReportCategory = tk.Label(self, text="Reporting Category:")

        self.calDate = tk.Entry(self) 
        self.entOriginalDesc = tk.Entry(self)  
        self.entAmount = tk.Entry(self)  
        self.entType = tk.Entry(self)   
        self.entAccount = tk.Entry(self)
        self.entDefaultCategory = tk.Entry(self) 
        self.entUserCategory = ttk.Combobox(self)
        self.entUserCategory['values'] = (' ')
        self.entUserNotes = tk.Entry(self)   
        self.entReportCategory = tk.Entry(self) 

        self.entMessage = tk.Entry(self) 

        self.lblExtensions = tk.Label(self, text="Extensions", font=("Tahoma 12 underline"))  
        self.lblReports = tk.Label(self, text="Reporting", font=("Tahoma 12 underline"))  
        self.lblFunctions = tk.Label(self, text="Functions", font=("Tahoma 12 underline"))  

        self.btn_update = tk.Button(self,text="Update", command=self.update_transextension_data)
        self.btn_delete = tk.Button(self, text="Delete", command=self.delete_transextension_data) 
        self.btn_clear = tk.Button(self, text="Clear", command=self.clear_form)

        self.btn_pivot = tk.Button(self, text="Budget Rpt", bg="SlateGray4", fg="white", command=self.print_budget_report)  
        #self.entRptDate = tk.Entry(self)
        #self.entRptDate.insert(0,'2022-01')
        self.entRptDate = ttk.Combobox(self)
        self.entRptDate['values'] = (' ')

        self.btn_Budgeting = tk.Button(self, text="Budgeting", command=self.open_budgeting_window)  
        self.btn_Defaults = tk.Button(self, text="Defaults", command=self.open_defaults_window) 
        self.btn_exit = tk.Button(self, text="Exit", bg="red", fg="white", command=self.exit)  
        
        self.btn_oldcsv = tk.Button(self, text="Load CSV", bg="DarkSeaGreen4", fg="white", command=self.load_transaction_data)
        self.entcsvload = tk.Entry(self)    
        self.entcsvload.insert(0,'transactions')

        self.btn_show_all = tk.Button(self, text="Show All", command=self.load_showall_data) 

        self.btn_show_big = tk.Button(self, text="Show >=", command=self.load_showbig_data) 
        self.entshowbig = tk.Entry(self)
        self.entshowbig.insert(0,'65')

        self.btn_show_cat = tk.Button(self, text="Show Cat", command=self.load_showcat_data) 
        self.entshowcat = ttk.Combobox(self)
        self.entshowcat['values'] = (' ')
        
        # Transaction Window

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "8", "9", "10", "11")
        self.tvTransaction= ttk.Treeview(self,show="headings", columns=columns)  
        self.tvTransaction.heading('#1', text='Date', anchor='center')  
        self.tvTransaction.column('#1', width=60, anchor='w', stretch=False)  
        self.tvTransaction.heading('#2', text='Org Description', anchor='center')  
        self.tvTransaction.column('#2',width=100, anchor='w', stretch=False)  
        self.tvTransaction.heading('#3', text='Amount', anchor='center')  
        self.tvTransaction.column('#3',width=60, anchor='center', stretch=False)  
        self.tvTransaction.heading('#4', text='Type', anchor='center')  
        self.tvTransaction.column('#4',width=50, anchor='center', stretch=False)  
        self.tvTransaction.heading('#5', text='Category', anchor='center')  
        self.tvTransaction.column('#5', width=100, anchor='w', stretch=False)  
        self.tvTransaction.heading('#6', text='Account', anchor='center')  
        self.tvTransaction.column('#6', width=60, anchor='w', stretch=False) 
        self.tvTransaction.heading('#7', text='Dflt Cat', anchor='center')  
        self.tvTransaction.column('#7', width=100, anchor='w', stretch=False) 
        self.tvTransaction.heading('#8', text='User Cat', anchor='center')  
        self.tvTransaction.column('#8', width=100, anchor='w', stretch=False) 
        self.tvTransaction.heading('#9', text='User Notes', anchor='center')  
        self.tvTransaction.column('#9', width=100, anchor='w', stretch=False) 
        self.tvTransaction.heading('#10', text='Reporting Cat', anchor='center')  
        self.tvTransaction.column('#10', width=100, anchor='w', stretch=False)
        self.tvTransaction.heading('#11', text='Dup', anchor='center')  
        self.tvTransaction.column('#11', width=30, anchor='center', stretch=False) 

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvTransaction.yview)  
        self.tvTransaction.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvTransaction.xview)  
        self.tvTransaction.configure(xscroll=hsb.set)  
        self.tvTransaction.bind("<<TreeviewSelect>>", self.show_selected_record)  
 
        # Grid Positioning

        self.btn_oldcsv.grid            (row=1, column =0, sticky=tk.EW, padx=5, pady=5)
        self.entcsvload.grid            (row=1, column =1, padx=5, pady=5)
        self.btn_show_all.grid          (row=1, column =2, sticky=tk.EW, padx=5, pady=5)  
        self.btn_show_big.grid          (row=1, column =3, sticky=tk.EW, padx=5, pady=5)
        self.entshowbig.grid            (row=1, column =4, padx=5, pady=5)
        self.btn_show_cat.grid          (row=1, column =5, sticky=tk.EW, padx=5, pady=5)
        self.entshowcat.grid            (row=1, column =6, padx=5, pady=5)

        self.entMessage.grid            (row=2, column =0, columnspan = 7, sticky=tk.EW, padx=5, pady=5)

        self.tvTransaction.grid         (row=3, column =0, rowspan = 12, columnspan = 7, sticky=tk.EW, padx=5, pady=2)
        vsb.grid                        (row=3, column =7, rowspan = 12, columnspan = 1, sticky=tk.NS)
        hsb.grid                        (row=15, column =0, rowspan = 1, columnspan = 7, sticky=tk.EW)

        # Label Positioning

        self.lblDate.grid               (row=20, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblOriginalDesc.grid       (row=21, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblAmount.grid             (row=22, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblType.grid               (row=23, column =0, sticky=tk.E, padx=5, pady=2) 
        self.lblAccount.grid            (row=24, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblDefaultCategory.grid      (row=25, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblUserCategory.grid    (row=26, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblUserNotes.grid  (row=27, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblReportCategory.grid       (row=28, column =0, sticky=tk.E, padx=5, pady=2)

        self.calDate.grid               (row=20, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entOriginalDesc.grid       (row=21, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entAmount.grid             (row=22, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entType.grid               (row=23, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2) 
        self.entAccount.grid            (row=24, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entDefaultCategory.grid      (row=25, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entUserCategory.grid    (row=26, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entUserNotes.grid  (row=27, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entReportCategory.grid    (row=28, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=2)

        # Button Positioning

        self.lblExtensions.grid         (row=20, column =4, sticky=tk.EW, padx=5, pady=2)
        self.btn_update.grid            (row=21, column =4, sticky=tk.EW, padx=5, pady=2)  
        self.btn_delete.grid            (row=22, column =4, sticky=tk.EW, padx=5, pady=2)  
        self.btn_clear.grid             (row=23, column =4, sticky=tk.EW, padx=5, pady=2) 

        self.lblReports.grid            (row=20, column =5, sticky=tk.EW, padx=5, pady=2)
        self.btn_pivot.grid             (row=21, column =5, sticky=tk.EW, padx=5, pady=2)
        self.entRptDate.grid            (row=22, column =5, sticky=tk.EW, padx=5, pady=2)

        self.lblFunctions.grid          (row=20, column =6, sticky=tk.EW, padx=5, pady=2)
        self.btn_Budgeting.grid         (row=21, column =6, sticky=tk.EW, padx=5, pady=2)
        self.btn_Defaults.grid          (row=22, column =6, sticky=tk.EW, padx=5, pady=2)
        self.btn_exit.grid              (row=23, column =6, sticky=tk.EW, padx=5, pady=2)

        self.lblSpace.grid              (row=29, column =0)

#
# show_selected_record
#

    def show_selected_record(self, event):  
        
        self.calDate.configure(state='normal')
        self.entOriginalDesc.configure(state='normal')
        self.entAmount.configure(state='normal')
        self.entType.configure(state='normal')
        self.entAccount.configure(state='normal')
        self.entDefaultCategory.configure(state='normal')
        self.entReportCategory.configure(state='normal')

        self.clear_form()  
        for selection in self.tvTransaction.selection():  
            item = self.tvTransaction.item(selection)
            Date, OriginalDesc, Amount, Type, Category, Account, DefaultCategory, UserCategory, UserNotes, ReportCategory, Dups = item["values"][0:11]  
            self.calDate.insert(0, Date)    
            self.entOriginalDesc.insert(0, OriginalDesc)  
            self.entAmount .insert(0, Amount)  
            self.entType .insert(0, Type)
            self.entAccount .insert(0, Account)
            self.entDefaultCategory .insert(0, DefaultCategory)
            self.entUserCategory .insert(0, UserCategory)
            self.entUserNotes .insert(0, UserNotes)
            self.entReportCategory .insert(0, ReportCategory)

            self.calDate.configure(state='readonly')
            self.entOriginalDesc.configure(state='readonly')
            self.entAmount.configure(state='readonly')
            self.entType.configure(state='readonly')
            self.entAccount.configure(state='readonly')
            self.entDefaultCategory.configure(state='readonly')
            self.entReportCategory.configure(state='readonly')

#
# update_transactions_dataframe
#

    def update_transactions_dataframe(self):
        
        # Read the accounts file
        pd_reader = pd.read_csv('trans_defaultacct.csv')
        transaccount_df = pd.DataFrame(pd_reader)

        # Read the defaults file
        pd_reader = pd.read_csv('trans_defaultdesc.csv')
        transdefault_df = pd.DataFrame(pd_reader)
        transdefault_df.to_sql('transdefault', db_connection, if_exists='replace', index=False)

        # Read the budget catagorties file
        pd_reader = pd.read_csv('trans_budgetcats.csv')
        transbudgetcats_df = pd.DataFrame(pd_reader)
        transbudgetcats_df = transbudgetcats_df['UserCategory']
        transbudgetcats_df = transbudgetcats_df.values.tolist()
        self.entUserCategory['values'] = transbudgetcats_df
        self.entshowcat['values'] = transbudgetcats_df

        # Read the extension file
        db_cursor.execute('DROP INDEX IF EXISTS transextension_idx')
        pd_reader = pd.read_csv('trans_extensions.csv')
        transextension_df = pd.DataFrame(pd_reader)
        transextension_df.to_sql('transextension', db_connection, if_exists='replace', index=False)
        db_cursor.execute('CREATE UNIQUE INDEX transextension_idx on transextension (Date, OriginalDesc, Amount, Type, Account)')

        # Put it all together
        allrows_query = "SELECT t.Date, t.Description, t.OriginalDesc, t.Amount, t.Type, t.Category, t.Account, t.Label, t.Notes, t.Dups, e.UserCategory, e.UserNotes, d.UserCategory FROM transactions t LEFT JOIN transextension e on t.Date=e.Date and t.OriginalDesc=e.OriginalDesc and t.Amount=e.Amount and t.Type=e.Type and t.Account=e.Account LEFT JOIN transdefault d ON t.OriginalDesc LIKE '%'||d.UserDefaultDesc||'%' where t.Account in (?,?,?)"
        UserAccount = transaccount_df['UserAccount'].drop_duplicates()
        UserAccount = UserAccount.values.tolist()
        data_tuple = UserAccount
        db_cursor.execute(allrows_query, data_tuple)

        # Build the dataframe
        self.transactions_df = pd.DataFrame(db_cursor.fetchall())
        self.transactions_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups','UserCategory','UserNotes','DefaultCategory']
        self.transactions_df['ReportCategory'] = self.transactions_df['UserCategory']
        self.transactions_df['ReportDate']   = self.transactions_df['Date']
        self.transactions_df = self.transactions_df.astype({'Amount':'float'})

        for ind in self.transactions_df.index:

            # Convert Report Date
            date_string = self.transactions_df['ReportDate'][ind]
            date_time_obj = datetime.strptime(date_string, '%m/%d/%Y')
            self.transactions_df['ReportDate'][ind] = date_time_obj
            self.transactions_df['ReportDate'][ind] = self.transactions_df['ReportDate'][ind].strftime('%Y-%m')

            # Set the Report Budget from the Company Table
            if self.transactions_df['ReportCategory'][ind] is None:
                self.transactions_df['ReportCategory'][ind] = self.transactions_df['DefaultCategory'][ind]

            # Set the Report Budget from the Category
            if self.transactions_df['ReportCategory'][ind] is None:  
                self.transactions_df['ReportCategory'][ind] = self.transactions_df['Category'][ind]

            # If not category is configured, set to a default value
            if self.transactions_df['ReportCategory'][ind] not in transbudgetcats_df:
                self.transactions_df['ReportCategory'][ind] = "------"

            # Turn Debits into negaive numbers
            if self.transactions_df['Type'][ind] == 'debit':
                self.transactions_df['Amount'][ind] = -abs(self.transactions_df['Amount'][ind])

#
# load_screen_data
#

    def load_screen_data(self, transactionset_df):
            
            # clears the treeview tvTransaction 
            self.tvTransaction.delete(*self.tvTransaction.get_children()) 

            # Load the screen

            for ind in transactionset_df.index: 
                self.tvTransaction.insert("", 'end', values=(transactionset_df['Date'][ind], transactionset_df['OriginalDesc'][ind], transactionset_df['Amount'][ind], transactionset_df['Type'][ind], transactionset_df['Category'][ind], transactionset_df['Account'][ind], transactionset_df['DefaultCategory'][ind], transactionset_df['UserCategory'][ind], transactionset_df['UserNotes'][ind], transactionset_df['ReportCategory'][ind], transactionset_df['Dups'][ind]))  

            RptDate = transactionset_df['ReportDate'].drop_duplicates()
            RptDate = RptDate.values.tolist()
            self.entRptDate['values'] = RptDate
            self.entRptDate.insert(0, RptDate[0])

#
# Button - Load CSV Transactions
#

    def load_transaction_data(self):

        if self.recordcount == 0:

            db_cursor.execute('DROP INDEX IF EXISTS transactions_idx')

            # Read the transaction file, mark Dups
            csv_var = self.entcsvload.get()
            pd_reader = pd.read_csv(f'{csv_var}.csv')
            transactions_df = pd.DataFrame(pd_reader)

            bool_series1 = transactions_df.duplicated(keep='first')
            bool_series1.colums = ['Dups']
            transactions_df =pd.concat([transactions_df, bool_series1], axis="columns")
            
            bool_series2 = transactions_df.duplicated(keep='first')
            bool_series2.colums = ['Dups2']
            transactions_df =pd.concat([transactions_df, bool_series2], axis="columns")

            transactions_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups','Dups2']
            transactions_df['Amount'] = transactions_df['Amount'].fillna(0)

            transactions_df.to_sql('transactions', db_connection, if_exists='replace', index=False)
            db_cursor.execute('CREATE UNIQUE INDEX transactions_idx on transactions (Date,OriginalDesc,Amount,Type,Category,Account,Dups,Dups2)')

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df)

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Initial transactions uploaded successfully.")
            
            self.recordcount = 1 

        else:
        
            # Read the previous file, mark Dups
            csv_var = self.entcsvload.get()
            pd_reader = pd.read_csv(f'{csv_var}.csv')
            transprevious_df = pd.DataFrame(pd_reader)

            bool_series1 = transprevious_df.duplicated(keep='first')
            bool_series1.colums = ['Dups']
            transprevious_df =pd.concat([transprevious_df, bool_series1], axis="columns")   

            bool_series2 = transprevious_df.duplicated(keep='first')
            bool_series2.colums = ['Dups2']
            transprevious_df =pd.concat([transprevious_df, bool_series2], axis="columns")  

            transprevious_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups','Dups2']
            transprevious_df['Amount'] = transprevious_df['Amount'].fillna(0)

            insert_query = "INSERT OR REPLACE INTO transactions (Date, Description, OriginalDesc, Amount, Type, Category, Account, Label, Notes, Dups, Dups2) VALUES (?,?,?,?,?,?,?,?,?,?,?)"  

            for index, row in transprevious_df.iterrows():
                db_cursor.execute(insert_query, tuple(row))

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df) 

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Additional transactions uploaded successfully.")

#
# Button - Show Big
#

    def load_showbig_data(self):
        
        showbig = int(self.entshowbig.get())
        if showbig > 0:
            showbig = -abs(showbig)
        self.update_transactions_dataframe()
        showbig_df = self.transactions_df.query("Amount <= @showbig and Type == 'debit'")
        showbig_df = showbig_df.sort_values(by=['ReportDate', 'Amount'], ascending=False)
        self.load_screen_data(showbig_df) 

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Big transactions displayed.")

#
# Button - Show Cat
#

    def load_showcat_data(self):
        
        showcat = self.entshowcat.get()
        self.update_transactions_dataframe()
        showcat_df = self.transactions_df.query("ReportCategory == @showcat")
        showcat_df = showcat_df.sort_values(by=['ReportDate', 'Amount'], ascending=False)
        self.load_screen_data(showcat_df) 

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Catagory transactions displayed.")

#
# Button - Show All
#

    def load_showall_data(self):
        
        self.update_transactions_dataframe()
        self.load_screen_data(self.transactions_df)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "All transactions displayed.")

#
# Button - Update Extension Data
#

    def update_transextension_data(self):  
    
        Date =          self.calDate.get()
        OriginalDesc =  self.entOriginalDesc.get() 
        Amount =        abs(float(self.entAmount.get()))
        Type =          self.entType.get()
        Account =       self.entAccount.get()  
        UserCategory =  self.entUserCategory.get()
        UserNotes =     self.entUserNotes.get() 

        insert_query = "INSERT OR REPLACE INTO transextension (Date, OriginalDesc, Amount, Type, Account, UserCategory, UserNotes) VALUES (?,?,?,?,?,?,?)"  
        data_tuple = (Date, OriginalDesc, Amount, Type, Account, UserCategory, UserNotes)
        db_cursor.execute(insert_query, data_tuple)
        db_connection.commit

        transextension_df = pd.read_sql_query("SELECT * FROM transextension", db_connection)
        transextension_df.to_csv('trans_extensions.csv', index=False)

        self.update_transactions_dataframe()
        self.load_screen_data(self.transactions_df)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Selected extension updated successfully.")  

#
# Button - Delete Extension Data
#

    def delete_transextension_data(self):  
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected record', icon='warning')  
        if MsgBox == 'yes':  

            Date =          self.calDate.get()
            OriginalDesc =  self.entOriginalDesc.get() 
            Amount =        abs(float(self.entAmount.get()))
            Type =          self.entType.get()
            Account =       self.entAccount.get()  

            delete_query = "DELETE from transextension where Date=? and OriginalDesc=? and Amount=? and Type=? and Account=?"  
            data_tuple = (Date, OriginalDesc, Amount, Type, Account)
            db_cursor.execute(delete_query, data_tuple)
            db_connection.commit

            transextension_df = pd.read_sql_query("SELECT * FROM transextension", db_connection)
            transextension_df.to_csv('trans_extensions.csv', index=False)

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df)

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Selected extension deleted succssfully.")

#
#  Button - Clear Forms
#

    def clear_form(self):
        self.calDate.delete(0, tk.END)   
        self.entOriginalDesc.delete(0, tk.END) 
        self.entAmount.delete(0, tk.END) 
        self.entType.delete(0, tk.END) 
        self.entAccount.delete(0, tk.END) 
        self.entDefaultCategory.delete(0, tk.END)  
        self.entUserCategory.delete(0, tk.END) 
        self.entUserNotes.delete(0, tk.END)
        self.entReportCategory.delete(0, tk.END) 
        self.entMessage.delete(0, tk.END) 

#
# Button - Budget Report (using Pivot Table)
#
    
    def print_budget_report(self):
        
        RptDate = self.entRptDate.get()

        pivot_df = self.transactions_df.query("ReportCategory !='Credit Card Payment' & ReportDate >= @RptDate")

        #  Spending Report
        #  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
        pivot = pd.pivot_table(data= pivot_df, index= 'ReportCategory', columns = ['ReportDate'], values= 'Amount', aggfunc= 'sum', margins= True, margins_name= 'Total')

        #  Budgeting Report
        #  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
        pivot2 = pd.pivot_table(data= pivot_df, index= 'ReportCategory', columns = ['ReportDate'], values= 'Amount', aggfunc= 'sum', margins= True, margins_name= 'Total')

        pd_reader = pd.read_csv('trans_budgetcats.csv')
        transbudgetcats_df = pd.DataFrame(pd_reader)

        pivot2 = pd.merge(transbudgetcats_df, pivot2, left_on='UserCategory', right_on='ReportCategory', how='left')
        pivot2 = pivot2.drop(columns=['Month01', 'Month02','Month03','Month04','Month05','Month06','Month07','Month08','Month09','Month10','Month11','Month12'])

        MaxMonth_df = transbudgetcats_df.drop(columns=['UserCategory','UserType','YearTotal'])
        pivot2['MonthBudget']=MaxMonth_df.max(axis=1)

        pivot2 = pivot2.reindex(columns = [col for col in pivot2.columns if col != 'YearTotal'] + ['YearTotal'])
        
        #  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
        with pd.ExcelWriter('budget_report.xlsx') as writer:
            pivot.to_excel(writer, sheet_name= 'Spending', float_format= "%.0f")
            pivot2.to_excel(writer, sheet_name= 'Budgeting', float_format= "%.0f", index=False)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Reports generated succssfully.")

#
# Button - Budgeting Window
#

    def open_budgeting_window(self):
        window = TM_BW.BudgetWindow(self)
        window.grab_set()

#
# Button - Defaults Window
#

    def open_defaults_window(self):
        window = TM_DW.DefaultWindow(self)
        window.grab_set()

#
# Verify or Create CSV files
#

    def verify_create_csv(self):  

        #  Validate the extention file.

        path_to_file = 'trans_extensions.csv'
        path = Path(path_to_file)

        if path.is_file():
            print(f'The file {path_to_file} exists')
        else:
            data = {'Date':['12/12/1900'], 'OriginalDesc':['default'],'Amount':['0.0'],'Type':['default'],'UserCategory':['default'],'UserNotes':['default']}
            temp_df = pd.DataFrame(data)
            temp_df.to_csv('trans_extensions.csv', index=False)

        #  Validate the budget file.

        path_to_file = 'trans_budgetcats.csv'
        path = Path(path_to_file)

        if path.is_file():
            print(f'The file {path_to_file} exists')
        else:
            data = {'UserCategory':['------'],'UserType':['default'],'Month01':['0.0'],'Month02':['0.0'],'Month03':['0.0'],'Month04':['0.0'],'Month05':['0.0'],'Month06':['0.0'],'Month07':['0.0'],'Month08':['0.0'],'Month09':['0.0'],'Month10':['0.0'],'Month11':['0.0'],'Month12':['0.0'],'YearTotal':['0.0']}
            temp_df = pd.DataFrame(data)
            temp_df.to_csv('trans_budgetcats.csv', index=False)

        #  Validate the default description file.
        
        path_to_file = 'trans_defaultdesc.csv'
        path = Path(path_to_file)

        if path.is_file():
            print(f'The file {path_to_file} exists')
        else:
            data = {'UserDefaultDesc':['default'], 'UserCategory':['default']}
            temp_df = pd.DataFrame(data)
            temp_df.to_csv('trans_defaultdesc.csv', index=False)

        #  Validate the default accounts file.
        
        path_to_file = 'trans_defaultacct.csv'
        path = Path(path_to_file)

        if path.is_file():
            print(f'The file {path_to_file} exists')
        else:
            data = {'UserAccount':['default']}
            temp_df = pd.DataFrame(data)
            temp_df.to_csv('trans_defaultacct.csv', index=False)

#
# Button - Exit
#

    def exit(self):  
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit?', icon='warning')  
        if MsgBox == 'yes':  
            self.destroy()  


#
# Tinker Mainline
#

if __name__ == "__main__":
    app = TransManager()
    app.mainloop()
