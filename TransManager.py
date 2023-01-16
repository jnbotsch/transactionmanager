##
##  Transaction Manager for Mint
##  Created By:  Jeff Botsch
##  
##   TransManager - Version 2.0
##
##   - Version 2.0 moves all SQL and CSV transactions to the DataManager.
##   - Local pandas queries and sorts are used for faster screen processing.
##   - System ensures constant CSV file integrity as CSV files are the system of record.
##

import pandas as pd
import tkinter as tk
import tkinter.messagebox as mb

from datetime import datetime
from tkinter import ttk

import TransManager_BudgetWindow as TM_BW
import TransManager_DefaultWindow as TM_DW

import TransManager_DataManager as TM_DM
dm = TM_DM.TransManager_DataManager()

##  turn off pandas warnings for dataframe updates, default='warn'
pd.options.mode.chained_assignment = None

##
##  Class - Main
##

class TransManager(tk.Tk):

    def __init__(self):  
        super().__init__()  

        ##  Verify or create the CSV files
        self.verify_create_csv()

        ##  Global variable
        self.recordcount = 0

        ##  Created dataframes for all tables
        self.trans_budgetcats_df = pd.DataFrame()
        self.trans_defaultacct_df = pd.DataFrame()
        self.trans_defaultdesc_df = pd.DataFrame()
        self.trans_extensions_df = pd.DataFrame()
        self.transactions_df = pd.DataFrame()

        ##  Window sizing
        self.title("Transaction Manager v1")  
        self.lblTitle = tk.Label(self, text="Transaction Manager v1", font=("Tahoma", 16)) 
        self.geometry("1050x650")
        self.resizable(0, 0)

        ##  configure the standard grid
        self.columnconfigure(0, weight=1, uniform="TransUX")
        self.columnconfigure(1, weight=1, uniform="TransUX")
        self.columnconfigure(2, weight=1, uniform="TransUX")
        self.columnconfigure(3, weight=1, uniform="TransUX")
        self.columnconfigure(4, weight=1, uniform="TransUX")
        self.columnconfigure(5, weight=1, uniform="TransUX")
        self.columnconfigure(6, weight=1, uniform="TransUX")

        ##  configure the standard grid
        self.rowconfigure(20, weight=1, uniform="TransUX")
        self.rowconfigure(21, weight=1, uniform="TransUX")
        self.rowconfigure(22, weight=1, uniform="TransUX")
        self.rowconfigure(23, weight=1, uniform="TransUX")
        self.rowconfigure(24, weight=1, uniform="TransUX")
        self.rowconfigure(25, weight=1, uniform="TransUX")
        self.rowconfigure(26, weight=1, uniform="TransUX")
        self.rowconfigure(27, weight=1, uniform="TransUX")
        self.rowconfigure(28, weight=1, uniform="TransUX")
        self.rowconfigure(29, weight=1, uniform="TransUX")
        self.rowconfigure(30, weight=1, uniform="TransUX")

        ##  configure the labels
        self.lblSpace = tk.Label(self, text=" ", width=100)
        self.lblDate = tk.Label(self, text="Transaction Date:")   
        self.lblUserDate = tk.Label(self, text="User Date:")
        self.lblOriginalDesc = tk.Label(self, text="Original Desc:")  
        self.lblAmount = tk.Label(self, text="Transaction Amount:")  
        self.lblType = tk.Label(self, text="Transaction Type:") 
        self.lblAccount = tk.Label(self, text="Bank Account:")  
        self.lblCategory = tk.Label(self, text="Category:") 
        self.lblDefaultCategory = tk.Label(self, text="Default Category:")  
        self.lblUserCategory = tk.Label(self, text="User Category:")
        self.lblUserNotes = tk.Label(self, text="User Notes:")  

        ##  configure the entry fields
        self.calDate = tk.Entry(self) 
        self.entUserDate = tk.Entry(self)  
        self.entOriginalDesc = tk.Entry(self)  
        self.entAmount = tk.Entry(self)  
        self.entType = tk.Entry(self)   
        self.entAccount = tk.Entry(self)
        self.entDefaultCategory = tk.Entry(self) 
        self.entCategory = tk.Entry(self)  
        self.entUserCategory = ttk.Combobox(self)
        self.entUserCategory['values'] = (' ')
        self.entUserNotes = tk.Entry(self)    

        self.entMessage = tk.Entry(self) 
        
        ##  configure the buttons section
        self.lblExtensions = tk.Label(self, text="Extensions", font=("Tahoma 12 underline"))  
        self.lblReports = tk.Label(self, text="Reporting", font=("Tahoma 12 underline"))  
        self.lblFunctions = tk.Label(self, text="Functions", font=("Tahoma 12 underline"))  

        self.btn_update = tk.Button(self,text="Update", command=self.update_transextension_data)
        self.btn_delete = tk.Button(self, text="Delete", command=self.delete_transextension_data) 
        self.btn_clear = tk.Button(self, text="Clear", command=self.clear_form)

        self.btn_pivot = tk.Button(self, text="Budget Rpt", bg="SlateGray4", fg="white", command=self.print_budget_report)  
        self.entRptDate = ttk.Combobox(self)
        self.entRptDate['values'] = (' ')

        self.btn_Budgeting = tk.Button(self, text="Budgeting", command=self.open_budgeting_window)  
        self.btn_Defaults = tk.Button(self, text="Defaults", command=self.open_defaults_window) 
        self.btn_exit = tk.Button(self, text="Exit", bg="red", fg="white", command=self.exit)
        self.btn_backup = tk.Button(self, text="Backup", command=self.backup_csv_files) 
        
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
        
        ##  Transaction Window
        columns = ("#Date", "#ODesc", "#Amt", "#Acct", "#Cat", "#DCat", "#UCat", "#UNotes", "#UDate", "#Type", "#Dup")
        self.tvTransaction= ttk.Treeview(self,show="headings", columns=columns)
        self.tvTransaction.heading('#Date', text='Date', anchor='center')  
        self.tvTransaction.column('#Date', width=80, anchor='w', stretch=False)   
        self.tvTransaction.heading('#ODesc', text='Org Description', anchor='center')  
        self.tvTransaction.column('#ODesc',width=200, anchor='w', stretch=False)  
        self.tvTransaction.heading('#Amt', text='Amount', anchor='center')  
        self.tvTransaction.column('#Amt',width=80, anchor='center', stretch=False)  
        self.tvTransaction.heading('#Acct', text='Account', anchor='center')  
        self.tvTransaction.column('#Acct', width=125, anchor='w', stretch=False)   
        self.tvTransaction.heading('#Cat', text='Category', anchor='center')  
        self.tvTransaction.column('#Cat', width=125, anchor='w', stretch=False)  
        self.tvTransaction.heading('#DCat', text='Dflt Cat', anchor='center')  
        self.tvTransaction.column('#DCat', width=125, anchor='w', stretch=False)
        self.tvTransaction.heading('#UCat', text='User Cat', anchor='center')  
        self.tvTransaction.column('#UCat', width=125, anchor='w', stretch=False) 
        self.tvTransaction.heading('#UNotes', text='User Notes', anchor='center')  
        self.tvTransaction.column('#UNotes', width=100, anchor='w', stretch=False) 
        self.tvTransaction.heading('#UDate', text='U.Date', anchor='center')  
        self.tvTransaction.column('#UDate', width=80, anchor='w', stretch=False)
        self.tvTransaction.heading('#Type', text='Type', anchor='center')  
        self.tvTransaction.column('#Type',width=50, anchor='center', stretch=False)
        self.tvTransaction.heading('#Dup', text='Dup', anchor='center')  
        self.tvTransaction.column('#Dup', width=35, anchor='center', stretch=False) 

        ##  Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvTransaction.yview)  
        self.tvTransaction.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvTransaction.xview)  
        self.tvTransaction.configure(xscroll=hsb.set)  
        self.tvTransaction.bind("<<TreeviewSelect>>", self.show_selected_record)  
 
        ##  Grid Positioning

        self.btn_oldcsv.grid            (row=1, column =0, sticky=tk.EW, padx=5, pady=1)
        self.entcsvload.grid            (row=1, column =1, padx=5, pady=1)
        self.btn_show_all.grid          (row=1, column =2, sticky=tk.EW, padx=5, pady=1)  
        self.btn_show_big.grid          (row=1, column =3, sticky=tk.EW, padx=5, pady=1)
        self.entshowbig.grid            (row=1, column =4, padx=5, pady=1)
        self.btn_show_cat.grid          (row=1, column =5, sticky=tk.EW, padx=5, pady=1)
        self.entshowcat.grid            (row=1, column =6, padx=5, pady=1)

        self.entMessage.grid            (row=2, column =0, columnspan = 7, sticky=tk.EW, padx=5, pady=5)

        self.tvTransaction.grid         (row=3, column =0, rowspan = 12, columnspan = 7, sticky=tk.EW, padx=5, pady=1)
        vsb.grid                        (row=3, column =7, rowspan = 12, columnspan = 1, sticky=tk.NS)
        hsb.grid                        (row=15, column =0, rowspan = 1, columnspan = 7, sticky=tk.EW)

        ##  Label Positioning

        self.lblDate.grid               (row=20, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblUserDate.grid           (row=21, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblOriginalDesc.grid       (row=22, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblAmount.grid             (row=23, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblType.grid               (row=24, column =0, sticky=tk.E, padx=5, pady=1) 
        self.lblAccount.grid            (row=25, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblCategory.grid           (row=26, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblDefaultCategory.grid    (row=27, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblUserCategory.grid       (row=28, column =0, sticky=tk.E, padx=5, pady=1)
        self.lblUserNotes.grid          (row=29, column =0, sticky=tk.E, padx=5, pady=1)

        self.calDate.grid               (row=20, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entUserDate.grid           (row=21, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entOriginalDesc.grid       (row=22, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entAmount.grid             (row=23, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entType.grid               (row=24, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1) 
        self.entAccount.grid            (row=25, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entCategory.grid           (row=26, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entDefaultCategory.grid    (row=27, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entUserCategory.grid       (row=28, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)
        self.entUserNotes.grid          (row=29, column =1, columnspan = 3, sticky=tk.EW, padx=5, pady=1)

        ##  Button Positioning

        self.lblExtensions.grid         (row=20, column =4, sticky=tk.EW, padx=5, pady=1)
        self.btn_update.grid            (row=21, column =4, sticky=tk.EW, padx=5, pady=1)  
        self.btn_delete.grid            (row=22, column =4, sticky=tk.EW, padx=5, pady=1)  
        self.btn_clear.grid             (row=23, column =4, sticky=tk.EW, padx=5, pady=1) 

        self.lblReports.grid            (row=20, column =5, sticky=tk.EW, padx=5, pady=1)
        self.btn_pivot.grid             (row=21, column =5, sticky=tk.EW, padx=5, pady=1)
        self.entRptDate.grid            (row=22, column =5, sticky=tk.EW, padx=5, pady=1)

        self.lblFunctions.grid          (row=20, column =6, sticky=tk.EW, padx=5, pady=1)
        self.btn_Budgeting.grid         (row=21, column =6, sticky=tk.EW, padx=5, pady=1)
        self.btn_Defaults.grid          (row=22, column =6, sticky=tk.EW, padx=5, pady=1)
        self.btn_exit.grid              (row=23, column =6, sticky=tk.EW, padx=5, pady=1)
        self.btn_backup.grid            (row=24, column =6, sticky=tk.EW, padx=5, pady=1)

        self.lblSpace.grid              (row=30, column =0)

##
##  Verify or Create CSV files
##

    def verify_create_csv(self):  

        dm.verify_create_csv('trans_extensions')
        dm.verify_create_csv('trans_budgetcats')
        dm.verify_create_csv('trans_defaultacct')
        dm.verify_create_csv('trans_defaultdesc')

##
##  show_selected_record
##

    def show_selected_record(self, event):  
        
        self.calDate.configure(state='normal')
        self.entOriginalDesc.configure(state='normal')
        self.entAmount.configure(state='normal')
        self.entType.configure(state='normal')
        self.entAccount.configure(state='normal')
        self.entCategory.configure(state='normal')
        self.entDefaultCategory.configure(state='normal')

        self.clear_form()  
        for selection in self.tvTransaction.selection():  
            item = self.tvTransaction.item(selection)
            Date, OriginalDesc, Amount, Account, Category, DefaultCategory, UserCategory, UserNotes, UserDate, Type, Dups = item["values"][0:12]  
            self.calDate            .insert(0, Date)  
            self.entUserDate        .insert(0, UserDate)  
            self.entOriginalDesc    .insert(0, OriginalDesc)  
            self.entAmount          .insert(0, Amount)  
            self.entType            .insert(0, Type)
            self.entAccount         .insert(0, Account)
            self.entCategory        .insert(0, Category)
            self.entDefaultCategory .insert(0, DefaultCategory)
            self.entUserCategory    .insert(0, UserCategory)
            self.entUserNotes       .insert(0, UserNotes)

            self.calDate.configure(state='readonly')
            self.entOriginalDesc.configure(state='readonly')
            self.entAmount.configure(state='readonly')
            self.entType.configure(state='readonly')
            self.entAccount.configure(state='readonly')
            self.entCategory.configure(state='readonly')
            self.entDefaultCategory.configure(state='readonly')

##
##  update_transactions_dataframe
##

    def update_transactions_dataframe(self):
        
        # Load the extention files
        self.transactions_df = dm.read_transactions()
        
        # Obtain the drop down list values
        self.trans_budgetcats_df = dm.load_csv_to_sql('trans_budgetcats')
        self.entUserCategory['values'] = self.trans_budgetcats_df['UserCategory'].values.tolist()
        self.entshowcat['values'] = self.trans_budgetcats_df['UserCategory'].values.tolist()

##
##  load_screen_data
##

    def load_screen_data(self, transactionset_df):

            # clears the treeview tvTransaction 
            self.tvTransaction.delete(*self.tvTransaction.get_children())

            # Load the screen

            for ind in transactionset_df.index: 
                self.tvTransaction.insert("", 'end', 
                values=(transactionset_df['Date'][ind], 
                transactionset_df['OriginalDesc'][ind], 
                transactionset_df['Amount'][ind],
                transactionset_df['Account'][ind], 
                transactionset_df['Category'][ind], 
                transactionset_df['DefaultCategory'][ind], 
                transactionset_df['UserCategory'][ind], 
                transactionset_df['UserNotes'][ind],
                transactionset_df['UserDate'][ind],
                transactionset_df['Type'][ind], 
                transactionset_df['Dups'][ind]))

            RptDate = transactionset_df['ReportDate'].drop_duplicates()
            RptDate = RptDate.values.tolist()
            self.entRptDate['values'] = RptDate
            self.entRptDate.insert(0, RptDate[0])

##
##  Button - Load CSV Transactions
##

    def load_transaction_data(self):

        ##  If first set of transactions, load transactions
        if self.recordcount == 0:

            csv_var = self.entcsvload.get()
            dm.load_transactions(csv_var)
            self.recordcount = 1 

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df) 

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Transactions uploaded successfully.")

        ##  If second set of transactions, add transactions
        else:

            csv_var = self.entcsvload.get()
            dm.add_transactions(csv_var)

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df) 

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Additional transactions uploaded successfully.")

##
##  Button - Show Big
##

    def load_showbig_data(self):
        
        showbig = int(self.entshowbig.get())
        if showbig > 0:
            showbig = -abs(showbig)
        showbig_df = self.transactions_df
        showbig_df = showbig_df.query("Amount <= @showbig and Type == 'debit'")
        showbig_df = showbig_df.sort_values(by=['ReportDate', 'Amount'], ascending=False)
        self.load_screen_data(showbig_df)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Big transactions displayed.")

##
##  Button - Show Cat
##

    def load_showcat_data(self):
        
        showcat = self.entshowcat.get()
        showcat_df = self.transactions_df
        showcat_df = showcat_df.query("ReportCategory == @showcat")
        showcat_df = showcat_df.sort_values(by=['ReportDate', 'Amount'], ascending=False)
        self.load_screen_data(showcat_df) 

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Catagory transactions displayed.")

##
##  Button - Show All
##

    def load_showall_data(self):
        
        self.load_screen_data(self.transactions_df)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "All transactions displayed.")

##
##  Button - Update Extension Data
##

    def update_transextension_data(self):  
    
        Date =          self.calDate.get()
        OriginalDesc =  self.entOriginalDesc.get() 
        Amount =        abs(float(self.entAmount.get()))
        Type =          self.entType.get()
        Account =       self.entAccount.get()  
        UserDate =      self.entUserDate.get()
        UserCategory =  self.entUserCategory.get()
        UserNotes =     self.entUserNotes.get() 

        if UserDate == 'None':
            UserDate = ''

        if UserCategory == 'None':
            UserCategory = ''

        if UserNotes == 'None':
            UserNotes = ''

        transextensions_tuple = (Date, OriginalDesc, Amount, Type, Account, UserDate, UserCategory, UserNotes)
        dm.update_transextensions(transextensions_tuple)

        self.update_transactions_dataframe()
        self.load_screen_data(self.transactions_df) 

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Selected extension updated successfully.")  

##
##  Button - Delete Extension Data
##

    def delete_transextension_data(self):  
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected record', icon='warning')  
        if MsgBox == 'yes':  

            Date =          self.calDate.get()
            OriginalDesc =  self.entOriginalDesc.get() 
            Amount =        abs(float(self.entAmount.get()))
            Type =          self.entType.get()
            Account =       self.entAccount.get()  

            transextensions_tuple = (Date, OriginalDesc, Amount, Type, Account)
            dm.update_transextensions(transextensions_tuple)

            self.update_transactions_dataframe()
            self.load_screen_data(self.transactions_df) 

            self.entMessage.delete(0, tk.END)
            self.entMessage.insert(0, "Selected extension deleted succssfully.")

##
##  Button - Clear Forms
##

    def clear_form(self):
        self.calDate.delete(0, tk.END)   
        self.entUserDate.delete(0, tk.END) 
        self.entOriginalDesc.delete(0, tk.END) 
        self.entAmount.delete(0, tk.END) 
        self.entType.delete(0, tk.END) 
        self.entAccount.delete(0, tk.END) 
        self.entCategory.delete(0, tk.END) 
        self.entDefaultCategory.delete(0, tk.END)  
        self.entUserCategory.delete(0, tk.END) 
        self.entUserNotes.delete(0, tk.END)
        self.entMessage.delete(0, tk.END) 

##
##  Button - Budget Report (using Pivot Table)
##

    def print_budget_report(self):
        
        RptDate = self.entRptDate.get()      

        pivot_df = self.transactions_df.query("ReportCategory != ['Credit Card Payment','Transfer'] & ReportDate >= @RptDate")

        #  Spending Report
        #  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
        pivot = pd.pivot_table(data= pivot_df, index= 'ReportCategory', columns = ['ReportDate'], values= 'Amount', aggfunc= 'sum', margins= True, margins_name= 'Total')

        #  Budgeting Report
        #  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html
        pivot2 = pd.pivot_table(data= pivot_df, index= 'ReportCategory', columns = ['ReportDate'], values= 'Amount', aggfunc= 'sum', margins= True, margins_name= 'Total')

        trans_budgetcats_df = dm.load_csv_to_sql('trans_budgetcats')

        pivot2 = pd.merge(trans_budgetcats_df, pivot2, left_on='UserCategory', right_on='ReportCategory', how='left')
        pivot2 = pivot2.drop(columns=['Month01', 'Month02','Month03','Month04','Month05','Month06','Month07','Month08','Month09','Month10','Month11','Month12'])

        MaxMonth_df = trans_budgetcats_df.drop(columns=['UserCategory','UserType','YearTotal'])
        pivot2['MonthBudget']=MaxMonth_df.max(axis=1)

        pivot2 = pivot2.reindex(columns = [col for col in pivot2.columns if col != 'YearTotal'] + ['YearTotal'])
        
        #  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
        with pd.ExcelWriter('budget_report.xlsx') as writer:
            pivot.to_excel(writer, sheet_name= 'Spending', float_format= "%.0f")
            pivot2.to_excel(writer, sheet_name= 'Budgeting', float_format= "%.0f", index=False)

        self.entMessage.delete(0, tk.END)
        self.entMessage.insert(0, "Reports generated succssfully.")

##
##  Button - Budgeting Window
##

    def open_budgeting_window(self):
        window = TM_BW.BudgetWindow(self)
        window.grab_set()

##
##  Button - Defaults Window
##

    def open_defaults_window(self):
        window = TM_DW.DefaultWindow(self)
        window.grab_set()

##
##  Button - Exit
##

    def exit(self):  
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit?', icon='warning')  
        if MsgBox == 'yes':  
            self.destroy()  

##
##  Button - Backup CSV Files
##

    def backup_csv_files(self):  

        dm.backup_csv_files('trans_extensions')
        dm.backup_csv_files('trans_budgetcats')
        dm.backup_csv_files('trans_defaultacct')
        dm.backup_csv_files('trans_defaultdesc')

##
##  Tinker Mainline
##

if __name__ == "__main__":
    app = TransManager()
    app.mainloop()
