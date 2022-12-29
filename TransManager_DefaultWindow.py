
import tkinter as tk
import tkinter.messagebox as mb  
from tkinter import ttk

from datetime import datetime

import sqlite3
import pandas as pd

# create a connection
db_connection = sqlite3.connect('TransManagerDB.db')

# creating database_cursor to perform SQL operation   
db_cursor = db_connection.cursor()

# turn off pandas warnings for dataframe updates
pd.options.mode.chained_assignment = None  # default='warn'

#
# Class - Default Window
#

class DefaultWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title('Transaction Manager Default Window')
        self.geometry("500x500")
        self.resizable(0, 0)
 
        self.lblUserDefaultDesc = tk.Label(self, text="User Default Desc:")
        self.lblUserCategory = tk.Label(self, text="User Category:")

        self.entUserDefaultDesc = tk.Entry(self)
        self.entUserCategory = ttk.Combobox(self)
        self.entUserCategory['values'] = (' ')
        
        self.btn_update = tk.Button(self,text="Update", command=self.update_budgetdft_data)
        self.btn_delete = tk.Button(self, text="Delete", command=self.delete_budgetdft_data) 
        self.btn_clear = tk.Button(self, text="Clear", command=self.clear_budgetdft_form)

        # Transaction Window

        columns = ("#1", "#2")
        self.tvDefault= ttk.Treeview(self,show="headings", columns=columns)  
        self.tvDefault.heading('#1', text='User Description', anchor='center')  
        self.tvDefault.column('#1', width=150, anchor='w', stretch=True)  
        self.tvDefault.heading('#2', text='User Category', anchor='center')  
        self.tvDefault.column('#2',width=150, anchor='w', stretch=True)
        
        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvDefault.yview)  
        self.tvDefault.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvDefault.xview)  
        self.tvDefault.configure(xscroll=hsb.set)  
        self.tvDefault.bind("<<TreeviewSelect>>", self.show_budgetdft_record)  

        # configure the standard grid
        self.columnconfigure(0, weight=1, uniform="DefaultUX")
        self.columnconfigure(1, weight=1, uniform="DefaultUX")

        self.rowconfigure(0, weight=1, uniform="DefaultUX")
        self.rowconfigure(3, weight=12, uniform="DefaultUX")
        self.rowconfigure(18, weight=1, uniform="DefaultUX")
        self.rowconfigure(21, weight=1, uniform="DefaultUX")
        self.rowconfigure(22, weight=1, uniform="DefaultUX")
        self.rowconfigure(25, weight=1, uniform="DefaultUX")
        self.rowconfigure(26, weight=1, uniform="DefaultUX")
        self.rowconfigure(27, weight=1, uniform="DefaultUX")
        self.rowconfigure(28, weight=1, uniform="DefaultUX")

        self.tvDefault.grid             (row=3, column =0, rowspan = 12, columnspan = 2, sticky=tk.NSEW, padx=5, pady=2)
        vsb.grid                        (row=3, column =2, rowspan = 12, columnspan = 1, sticky=tk.NS)

        self.lblUserDefaultDesc.grid       (row=20, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblUserCategory.grid         (row=21, column =0, sticky=tk.E, padx=5, pady=2)

        self.entUserDefaultDesc.grid       (row=20, column =1, sticky=tk.EW, padx=5, pady=2)
        self.entUserCategory.grid         (row=21, column =1, sticky=tk.EW, padx=5, pady=2)
 
        self.btn_update.grid            (row=25, column =1, sticky=tk.EW, padx=5, pady=2)  
        self.btn_delete.grid            (row=26, column =1, sticky=tk.EW, padx=5, pady=2)  
        self.btn_clear.grid             (row=27, column =1, sticky=tk.EW, padx=5, pady=2) 

        self.load_csv_data() 
        self.load_screen_data() 

#
# initial_csv_data
#

    def load_csv_data(self):
    
        # Read the budget catagorties file
        db_cursor.execute('DROP INDEX IF EXISTS transdefault_idx')
        pd_reader = pd.read_csv('trans_defaultdesc.csv')
        default_df = pd.DataFrame(pd_reader)
        default_df.to_sql('transdefault', db_connection, if_exists='replace', index=False)
        db_cursor.execute('CREATE UNIQUE INDEX transdefault_idx on transdefault (UserDefaultDesc)')

        # Read the budget catagorties file
        pd_reader = pd.read_csv('trans_budgetcats.csv')
        transbudgetcats_df = pd.DataFrame(pd_reader)
        transbudgetcats_df = transbudgetcats_df['UserCategory']
        transbudgetcats_df = transbudgetcats_df.values.tolist()
        self.entUserCategory['values'] = transbudgetcats_df

#
# load_screen_data
#

    def load_screen_data(self):

        default_df = pd.read_sql_query("SELECT * FROM transdefault ORDER BY UserDefaultDesc", db_connection)

        self.tvDefault.delete(*self.tvDefault.get_children()) 

        for ind in default_df.index: 
                self.tvDefault.insert("", 'end', values=(default_df['UserDefaultDesc'][ind], default_df['UserCategory'][ind]))  

#
# Show Budget Cat
#

    def show_budgetdft_record(self, event):
        
        self.clear_budgetdft_form()  
        for selection in self.tvDefault.selection():

            item = self.tvDefault.item(selection)
            UserDefaultDesc, UserCategory = item["values"][0:2]  
            
            self.entUserDefaultDesc.insert(0, UserDefaultDesc)    
            self.entUserCategory.insert(0, UserCategory)  

#
# Update Budget Cat
#

    def update_budgetdft_data(self):

        UserDefaultDesc =    self.entUserDefaultDesc.get()
        UserCategory =  self.entUserCategory.get() 

        insert_query = "INSERT OR REPLACE INTO transdefault (UserDefaultDesc, UserCategory) VALUES (?,?)"  
        data_tuple = (UserDefaultDesc, UserCategory)
        db_cursor.execute(insert_query, data_tuple)
        db_connection.commit

        default_df = pd.read_sql_query("SELECT * FROM transdefault ORDER BY UserDefaultDesc", db_connection)
        default_df.to_csv('trans_defaultdesc.csv', index=False)

        self.load_screen_data()

#
# Delete Budget Cat
#

    def delete_budgetdft_data(self):
  
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected record', icon='warning')  
        if MsgBox == 'yes':  

            UserDefaultDesc =    self.entUserDefaultDesc.get()

            insert_query = "DELETE from transdefault where UserCategory=?"  
            data_tuple = (UserDefaultDesc,)
            db_cursor.execute(insert_query, data_tuple)
            db_connection.commit

            default_df = pd.read_sql_query("SELECT * FROM transdefault ORDER BY UserDefaultDesc", db_connection)
            default_df.to_csv('trans_defaultdesc.csv', index=False)

            self.load_screen_data()

#
#  Button - Clear Forms
#

    def clear_budgetdft_form(self):

        self.entUserDefaultDesc.delete(0, tk.END)   
        self.entUserCategory.delete(0, tk.END) 
