##
##  Transaction Manager for Mint
##  Created By:  Jeff Botsch
##  
##   DefaultWindow - Version 2.0
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

import TransManager_DataManager as TM_DM
dm = TM_DM.TransManager_DataManager()

##
##  Class - Default Window
##

class DefaultWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        ##  Window sizing

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

        ##  Transaction Window
        columns = ("#1", "#2")
        self.tvDefault= ttk.Treeview(self,show="headings", columns=columns)  
        self.tvDefault.heading('#1', text='User Description', anchor='center')  
        self.tvDefault.column('#1', width=150, anchor='w', stretch=True)  
        self.tvDefault.heading('#2', text='User Category', anchor='center')  
        self.tvDefault.column('#2',width=150, anchor='w', stretch=True)
        
        ##  Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvDefault.yview)  
        self.tvDefault.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvDefault.xview)  
        self.tvDefault.configure(xscroll=hsb.set)  
        self.tvDefault.bind("<<TreeviewSelect>>", self.show_budgetdft_record)  

        ##  configure the standard grid
        self.columnconfigure(0, weight=1, uniform="DefaultUX")
        self.columnconfigure(1, weight=1, uniform="DefaultUX")
        
        ##  configure the standard grid
        self.rowconfigure(0, weight=1, uniform="DefaultUX")
        self.rowconfigure(3, weight=12, uniform="DefaultUX")
        self.rowconfigure(18, weight=1, uniform="DefaultUX")
        self.rowconfigure(21, weight=1, uniform="DefaultUX")
        self.rowconfigure(22, weight=1, uniform="DefaultUX")
        self.rowconfigure(25, weight=1, uniform="DefaultUX")
        self.rowconfigure(26, weight=1, uniform="DefaultUX")
        self.rowconfigure(27, weight=1, uniform="DefaultUX")
        self.rowconfigure(28, weight=1, uniform="DefaultUX")

        ##  Grid Positioning
        self.tvDefault.grid             (row=3, column =0, rowspan = 12, columnspan = 2, sticky=tk.NSEW, padx=5, pady=2)
        vsb.grid                        (row=3, column =2, rowspan = 12, columnspan = 1, sticky=tk.NS)

        ##  Label Positioning
        self.lblUserDefaultDesc.grid       (row=20, column =0, sticky=tk.E, padx=5, pady=2)
        self.lblUserCategory.grid         (row=21, column =0, sticky=tk.E, padx=5, pady=2)

        self.entUserDefaultDesc.grid       (row=20, column =1, sticky=tk.EW, padx=5, pady=2)
        self.entUserCategory.grid         (row=21, column =1, sticky=tk.EW, padx=5, pady=2)
        
        ##  Button Positioning
        self.btn_update.grid            (row=25, column =1, sticky=tk.EW, padx=5, pady=2)  
        self.btn_delete.grid            (row=26, column =1, sticky=tk.EW, padx=5, pady=2)  
        self.btn_clear.grid             (row=27, column =1, sticky=tk.EW, padx=5, pady=2) 

        self.load_csv_data() 
        self.load_screen_data() 

##
##  initial_csv_data
##

    def load_csv_data(self):

        # Obtain the drop down list values
        self.trans_budgetcats_df = dm.load_csv_to_sql('trans_budgetcats')
        self.entUserCategory['values'] = self.trans_budgetcats_df['UserCategory'].values.tolist()

##
##  load_screen_data
##

    def load_screen_data(self):

        trans_defaultdesc_df = dm.load_transdefaults()
        trans_defaultdesc_df = trans_defaultdesc_df.sort_values(by=['UserDefaultDesc'], ascending=True)

        self.tvDefault.delete(*self.tvDefault.get_children()) 

        for ind in trans_defaultdesc_df.index: 
                self.tvDefault.insert("", 'end', values=(trans_defaultdesc_df['UserDefaultDesc'][ind], trans_defaultdesc_df['UserCategory'][ind]))  

##
##  Show Budget Cat
##

    def show_budgetdft_record(self, event):
        
        self.clear_budgetdft_form()  
        for selection in self.tvDefault.selection():

            item = self.tvDefault.item(selection)
            UserDefaultDesc, UserCategory = item["values"][0:2]  
            
            self.entUserDefaultDesc.insert(0, UserDefaultDesc)    
            self.entUserCategory.insert(0, UserCategory)  

##
##  Update Budget Cat
##

    def update_budgetdft_data(self):

        UserDefaultDesc =    self.entUserDefaultDesc.get()
        UserCategory =  self.entUserCategory.get() 

        transdefaults_tuple = (UserDefaultDesc, UserCategory)
        dm.update_transdefaults(transdefaults_tuple)

        self.load_screen_data()

##
##  Delete Budget Cat
##

    def delete_budgetdft_data(self):
  
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected record', icon='warning')  
        if MsgBox == 'yes':  

            UserDefaultDesc =    self.entUserDefaultDesc.get() 

            transdefaults_tuple = (UserDefaultDesc,)
            dm.delete_transdefaults(transdefaults_tuple)

            self.load_screen_data()

##
##  Button - Clear Forms
##

    def clear_budgetdft_form(self):

        self.entUserDefaultDesc.delete(0, tk.END)   
        self.entUserCategory.delete(0, tk.END) 
