
import tkinter as tk
import tkinter.messagebox as mb  
from tkinter import ttk

from datetime import datetime

import pandas as pd

# turn off pandas warnings for dataframe updates, default='warn'
pd.options.mode.chained_assignment = None

#
# Class - Budget Window
#

class BudgetWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title('Transaction Manager Budget Window')
        self.geometry("900x600")
        self.resizable(0, 0)

        self.budgetcatsGlobal_df = pd.DataFrame()

        # Transaction Window

        columns = ("Cat", "Typ", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",'Dec','Yr')
        self.tvBudget= ttk.Treeview(self,show="headings", columns=columns)  
        self.tvBudget.heading('Cat', text='Category', anchor='center')  
        self.tvBudget.column('Cat', width=150, anchor='w', stretch=True)  
        self.tvBudget.heading('Typ', text='Type', anchor='center')  
        self.tvBudget.column('Typ', width=50, anchor='w', stretch=True)  
        self.tvBudget.heading('Jan', text='Jan', anchor='center')  
        self.tvBudget.column('Jan',width=50, anchor='w', stretch=True)  
        self.tvBudget.heading('Feb', text='Feb', anchor='center')
        self.tvBudget.column('Feb',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Mar', text='Mar', anchor='center')
        self.tvBudget.column('Mar',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Apr', text='Apr', anchor='center')
        self.tvBudget.column('Apr',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('May', text='May', anchor='center')
        self.tvBudget.column('May',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Jun', text='Jun', anchor='center')
        self.tvBudget.column('Jun',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Jul', text='Jul', anchor='center')
        self.tvBudget.column('Jul',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Aug', text='Aug', anchor='center')
        self.tvBudget.column('Aug',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Sep', text='Sep', anchor='center')
        self.tvBudget.column('Sep',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Oct', text='Oct', anchor='center')
        self.tvBudget.column('Oct',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Nov', text='Nov', anchor='center')
        self.tvBudget.column('Nov',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Dec', text='Dec', anchor='center')
        self.tvBudget.column('Dec',width=50, anchor='w', stretch=True) 
        self.tvBudget.heading('Yr', text='Year', anchor='center')
        self.tvBudget.column('Yr',width=50, anchor='w', stretch=True) 

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvBudget.yview)  
        self.tvBudget.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvBudget.xview)  
        self.tvBudget.configure(xscroll=hsb.set)  
        self.tvBudget.bind("<<TreeviewSelect>>", self.show_budgetcat_record) 

        self.dspTotal = tk.Label(self, text="Totals:")
        self.dspMonth01 = tk.Entry(self)   
        self.dspMonth02 = tk.Entry(self) 
        self.dspMonth03 = tk.Entry(self) 
        self.dspMonth04 = tk.Entry(self) 
        self.dspMonth05 = tk.Entry(self) 
        self.dspMonth06 = tk.Entry(self) 
        self.dspMonth07 = tk.Entry(self) 
        self.dspMonth08 = tk.Entry(self) 
        self.dspMonth09 = tk.Entry(self) 
        self.dspMonth10 = tk.Entry(self) 
        self.dspMonth11 = tk.Entry(self) 
        self.dspMonth12 = tk.Entry(self) 

        self.lblUserCategory = tk.Label(self, text="Category") 
        self.lblUserType = tk.Label(self, text="Type")
        self.lblMonth01 = tk.Label(self, text="Jan")   
        self.lblMonth02 = tk.Label(self, text="Feb") 
        self.lblMonth03 = tk.Label(self, text="Mar") 
        self.lblMonth04 = tk.Label(self, text="Apr") 
        self.lblMonth05 = tk.Label(self, text="May") 
        self.lblMonth06 = tk.Label(self, text="Jun") 
        self.lblMonth07 = tk.Label(self, text="Jul") 
        self.lblMonth08 = tk.Label(self, text="Aug") 
        self.lblMonth09 = tk.Label(self, text="Sep") 
        self.lblMonth10 = tk.Label(self, text="Oct") 
        self.lblMonth11 = tk.Label(self, text="Nov")  
        self.lblMonth12 = tk.Label(self, text="Dec") 

        self.entUserCategory = tk.Entry(self)
        self.entUserType = ttk.Combobox(self)
        self.entUserType['values'] = ('credit','debit','none')
        self.entMonth01 = tk.Entry(self)   
        self.entMonth02 = tk.Entry(self) 
        self.entMonth03 = tk.Entry(self) 
        self.entMonth04 = tk.Entry(self) 
        self.entMonth05 = tk.Entry(self) 
        self.entMonth06 = tk.Entry(self) 
        self.entMonth07 = tk.Entry(self) 
        self.entMonth08 = tk.Entry(self) 
        self.entMonth09 = tk.Entry(self) 
        self.entMonth10 = tk.Entry(self) 
        self.entMonth11 = tk.Entry(self) 
        self.entMonth12 = tk.Entry(self) 

        self.btn_update = tk.Button(self,text="Update", command=self.update_budgetcats_data)
        self.btn_delete = tk.Button(self, text="Delete", command=self.delete_budgetcats_data) 
        self.btn_clear = tk.Button(self, text="Clear", command=self.clear_budgetcats_form) 

        # configure the standard grid
        self.columnconfigure(0, weight=1, uniform="BudgetUX")
        self.columnconfigure(1, weight=1, uniform="BudgetUX")
        self.columnconfigure(2, weight=1, uniform="BudgetUX")
        self.columnconfigure(3, weight=1, uniform="BudgetUX")
        self.columnconfigure(4, weight=1, uniform="BudgetUX")
        self.columnconfigure(5, weight=1, uniform="BudgetUX")
        self.columnconfigure(6, weight=1, uniform="BudgetUX")
        self.columnconfigure(7, weight=1, uniform="BudgetUX")
        self.columnconfigure(8, weight=1, uniform="BudgetUX")
        self.columnconfigure(9, weight=1, uniform="BudgetUX")
        self.columnconfigure(10, weight=1, uniform="BudgetUX")
        self.columnconfigure(11, weight=1, uniform="BudgetUX")
        self.columnconfigure(12, weight=1, uniform="BudgetUX")
        self.columnconfigure(13, weight=1, uniform="BudgetUX")
        self.columnconfigure(14, weight=1, uniform="BudgetUX")
        self.columnconfigure(15, weight=1, uniform="BudgetUX")
        self.columnconfigure(16, weight=1, uniform="BudgetUX")

        self.rowconfigure(0, weight=1, uniform="BudgetUX")
        self.rowconfigure(3, weight=15, uniform="BudgetUX")
        self.rowconfigure(18, weight=1, uniform="BudgetUX")
        self.rowconfigure(21, weight=1, uniform="BudgetUX")
        self.rowconfigure(22, weight=1, uniform="BudgetUX")
        self.rowconfigure(25, weight=1, uniform="BudgetUX")
        self.rowconfigure(26, weight=1, uniform="BudgetUX")
        self.rowconfigure(27, weight=1, uniform="BudgetUX")
        self.rowconfigure(28, weight=1, uniform="BudgetUX")

        self.tvBudget.grid              (row=3, column =0, rowspan = 15, columnspan = 17, sticky=tk.NSEW, padx=5, pady=2)
        vsb.grid                        (row=3, column =18, rowspan = 15, columnspan = 1, sticky=tk.NS)
        
        self.dspTotal.grid    (row=18, column =0, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.dspMonth01.grid  (row=18, column =4, padx=2, pady=2)
        self.dspMonth02.grid  (row=18, column =5, padx=2, pady=2)
        self.dspMonth03.grid  (row=18, column =6, padx=2, pady=2)
        self.dspMonth04.grid  (row=18, column =7, padx=2, pady=2)
        self.dspMonth05.grid  (row=18, column =8, padx=2, pady=2)
        self.dspMonth06.grid  (row=18, column =9, padx=2, pady=2)
        self.dspMonth07.grid  (row=18, column =10, padx=2, pady=2)
        self.dspMonth08.grid  (row=18, column =11, padx=2, pady=2)
        self.dspMonth09.grid  (row=18, column =12, padx=2, pady=2)
        self.dspMonth10.grid  (row=18, column =13, padx=2, pady=2)
        self.dspMonth11.grid  (row=18, column =14, padx=2, pady=2)
        self.dspMonth12.grid  (row=18, column =15, padx=2, pady=2)

        self.lblUserCategory.grid    (row=21, column =0, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.lblUserType.grid    (row=21, column =3, padx=2, pady=2)
        self.lblMonth01.grid  (row=21, column =4, padx=2, pady=2)
        self.lblMonth02.grid  (row=21, column =5, padx=2, pady=2)
        self.lblMonth03.grid  (row=21, column =6, padx=2, pady=2)
        self.lblMonth04.grid  (row=21, column =7, padx=2, pady=2)
        self.lblMonth05.grid  (row=21, column =8, padx=2, pady=2)
        self.lblMonth06.grid  (row=21, column =9, padx=2, pady=2)
        self.lblMonth07.grid  (row=21, column =10, padx=2, pady=2)
        self.lblMonth08.grid  (row=21, column =11, padx=2, pady=2)
        self.lblMonth09.grid  (row=21, column =12, padx=2, pady=2)
        self.lblMonth10.grid  (row=21, column =13, padx=2, pady=2)
        self.lblMonth11.grid  (row=21, column =14, padx=2, pady=2)
        self.lblMonth12.grid  (row=21, column =15, padx=2, pady=2)

        self.entUserCategory.grid    (row=22, column =0, columnspan = 3, sticky=tk.EW, padx=5, pady=2)
        self.entUserType.grid    (row=22, column =3, padx=2, pady=2)
        self.entMonth01.grid  (row=22, column =4, padx=2, pady=2)
        self.entMonth02.grid  (row=22, column =5, padx=2, pady=2)
        self.entMonth03.grid  (row=22, column =6, padx=2, pady=2)
        self.entMonth04.grid  (row=22, column =7, padx=2, pady=2)
        self.entMonth05.grid  (row=22, column =8, padx=2, pady=2)
        self.entMonth06.grid  (row=22, column =9, padx=2, pady=2)
        self.entMonth07.grid  (row=22, column =10, padx=2, pady=2)
        self.entMonth08.grid  (row=22, column =11, padx=2, pady=2)
        self.entMonth09.grid  (row=22, column =12, padx=2, pady=2)
        self.entMonth10.grid  (row=22, column =13, padx=2, pady=2)
        self.entMonth11.grid  (row=22, column =14, padx=2, pady=2)
        self.entMonth12.grid  (row=22, column =15, padx=2, pady=2)

        self.btn_update.grid            (row=25, column =3, columnspan = 3, sticky=tk.EW, padx=5, pady=2)  
        self.btn_delete.grid            (row=26, column =3, columnspan = 3, sticky=tk.EW, padx=5, pady=2)  
        self.btn_clear.grid             (row=27, column =3, columnspan = 3, sticky=tk.EW, padx=5, pady=2)  
        
        self.load_csv_data() 
        self.load_screen_data() 

#
# initial_csv_data
#

    def load_csv_data(self):

        # Read the budget catagorties file
        pd_reader = pd.read_csv('trans_budgetcats.csv')
        budgetcats_df = pd.DataFrame(pd_reader)
        budgetcats_df = budgetcats_df.astype(
            {'Month01':'float',
            'Month02':'float',
            'Month03':'float',
            'Month04':'float',
            'Month05':'float',
            'Month06':'float',
            'Month07':'float',
            'Month08':'float',
            'Month09':'float',
            'Month10':'float',
            'Month11':'float',
            'Month12':'float'})
    
        self.budgetcatsGlobal_df = budgetcats_df

#
# load_screen_data
#

    def load_screen_data(self):

        self.tvBudget.delete(*self.tvBudget.get_children()) 
        self.dspMonth01.delete(0, tk.END)
        self.dspMonth02.delete(0, tk.END)
        self.dspMonth03.delete(0, tk.END)
        self.dspMonth04.delete(0, tk.END)
        self.dspMonth05.delete(0, tk.END)
        self.dspMonth06.delete(0, tk.END)
        self.dspMonth07.delete(0, tk.END)
        self.dspMonth08.delete(0, tk.END)
        self.dspMonth09.delete(0, tk.END)
        self.dspMonth10.delete(0, tk.END)
        self.dspMonth11.delete(0, tk.END)
        self.dspMonth12.delete(0, tk.END)

        for each_rec in range(len(self.budgetcatsGlobal_df)):
            self.tvBudget.insert("", tk.END, values=list(self.budgetcatsGlobal_df.loc[each_rec]))

        debits_df = self.budgetcatsGlobal_df.query("UserType == 'debit'")
        credits_df = self.budgetcatsGlobal_df.query("UserType == 'credit'")

        #  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html

        self.dspMonth01.insert(0, -abs(debits_df['Month01'].sum())+credits_df['Month01'].sum())  
        self.dspMonth02.insert(0, -abs(debits_df['Month02'].sum())+credits_df['Month02'].sum())  
        self.dspMonth03.insert(0, -abs(debits_df['Month03'].sum())+credits_df['Month03'].sum())  
        self.dspMonth04.insert(0, -abs(debits_df['Month04'].sum())+credits_df['Month04'].sum())  
        self.dspMonth05.insert(0, -abs(debits_df['Month05'].sum())+credits_df['Month05'].sum())  
        self.dspMonth06.insert(0, -abs(debits_df['Month06'].sum())+credits_df['Month06'].sum())  
        self.dspMonth07.insert(0, -abs(debits_df['Month07'].sum())+credits_df['Month07'].sum())  
        self.dspMonth08.insert(0, -abs(debits_df['Month08'].sum())+credits_df['Month08'].sum())  
        self.dspMonth09.insert(0, -abs(debits_df['Month09'].sum())+credits_df['Month09'].sum())  
        self.dspMonth10.insert(0, -abs(debits_df['Month10'].sum())+credits_df['Month10'].sum())  
        self.dspMonth11.insert(0, -abs(debits_df['Month11'].sum())+credits_df['Month11'].sum())  
        self.dspMonth12.insert(0, -abs(debits_df['Month12'].sum())+credits_df['Month12'].sum())  

#
# Show Budget Cat
#

    def show_budgetcat_record(self, event):
        
        self.clear_budgetcats_form()  
        for selection in self.tvBudget.selection():

            item = self.tvBudget.item(selection)
            UserCategory, UserType, Month01, Month02, Month03, Month04, Month05, Month06, Month07, Month08, Month09, Month10, Month11, Month12, YearTotal = item["values"][0:15]  
            
            self.entUserCategory.insert(0, UserCategory)
            self.entUserType.insert(0, UserType)    
            self.entMonth01.insert(0, Month01)  
            self.entMonth02.insert(0, Month02)
            self.entMonth03.insert(0, Month03)
            self.entMonth04.insert(0, Month04)
            self.entMonth05.insert(0, Month05)
            self.entMonth06.insert(0, Month06)
            self.entMonth07.insert(0, Month07)
            self.entMonth08.insert(0, Month08)
            self.entMonth09.insert(0, Month09)
            self.entMonth10.insert(0, Month10)
            self.entMonth11.insert(0, Month11)
            self.entMonth12.insert(0, Month12)

#
# Update Budget Cat
#

    def update_budgetcats_data(self):

        UserCategory =    self.entUserCategory.get()
        UserType =    self.entUserType.get()
        Month01 =  abs(float(self.entMonth01.get())) 
        Month02 =  abs(float(self.entMonth02.get())) 
        Month03 =  abs(float(self.entMonth03.get())) 
        Month04 =  abs(float(self.entMonth04.get()))  
        Month05 =  abs(float(self.entMonth05.get()))  
        Month06 =  abs(float(self.entMonth06.get()))  
        Month07 =  abs(float(self.entMonth07.get()))  
        Month08 =  abs(float(self.entMonth08.get())) 
        Month09 =  abs(float(self.entMonth09.get())) 
        Month10 =  abs(float(self.entMonth10.get())) 
        Month11 =  abs(float(self.entMonth11.get())) 
        Month12 =  abs(float(self.entMonth12.get())) 
        YearTotal = Month01+Month02+Month03+Month04+Month05+Month06+Month07+Month08+Month09+Month10+Month11+Month12
        
        if (UserCategory in self.budgetcatsGlobal_df['UserCategory'].values):
            idx = self.budgetcatsGlobal_df.index[self.budgetcatsGlobal_df['UserCategory'] == UserCategory].tolist()
            self.budgetcatsGlobal_df.loc[idx,'UserType'] = UserType
            self.budgetcatsGlobal_df.loc[idx,'Month01'] = Month01
            self.budgetcatsGlobal_df.loc[idx,'Month02'] = Month02
            self.budgetcatsGlobal_df.loc[idx,'Month03'] = Month03
            self.budgetcatsGlobal_df.loc[idx,'Month04'] = Month04
            self.budgetcatsGlobal_df.loc[idx,'Month05'] = Month05
            self.budgetcatsGlobal_df.loc[idx,'Month06'] = Month06
            self.budgetcatsGlobal_df.loc[idx,'Month07'] = Month07
            self.budgetcatsGlobal_df.loc[idx,'Month08'] = Month08
            self.budgetcatsGlobal_df.loc[idx,'Month09'] = Month09
            self.budgetcatsGlobal_df.loc[idx,'Month10'] = Month10
            self.budgetcatsGlobal_df.loc[idx,'Month11'] = Month11
            self.budgetcatsGlobal_df.loc[idx,'Month12'] = Month12
            self.budgetcatsGlobal_df.loc[idx,'YearTotal'] = YearTotal

        else:
            data_tuple = (UserCategory,UserType,Month01,Month02,Month03,Month04,Month05,Month06,Month07,Month08,Month09,Month10,Month11,Month12,YearTotal)
            self.budgetcatsGlobal_df.loc[len(self.budgetcatsGlobal_df)] = data_tuple

        self.budgetcatsGlobal_df = self.budgetcatsGlobal_df.sort_values(by=['UserCategory'])
        self.budgetcatsGlobal_df = self.budgetcatsGlobal_df.reset_index(drop=True)
        self.budgetcatsGlobal_df.to_csv('trans_budgetcats.csv', index=False)
        print(self.budgetcatsGlobal_df)

        self.load_screen_data()

#
# Delete Budget Cat
#

    def delete_budgetcats_data(self):
  
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected record', icon='warning')  
        if MsgBox == 'yes':  

            UserCategory =    self.entUserCategory.get()

            self.budgetcatsGlobal_df = self.budgetcatsGlobal_df.drop(self.budgetcatsGlobal_df[self.budgetcatsGlobal_df.UserCategory == UserCategory].index)

            self.budgetcatsGlobal_df = self.budgetcatsGlobal_df.sort_values(by=['UserCategory'])
            self.budgetcatsGlobal_df = self.budgetcatsGlobal_df.reset_index(drop=True)
            self.budgetcatsGlobal_df.to_csv('trans_budgetcats.csv', index=False)
            print(self.budgetcatsGlobal_df)

            self.load_screen_data()

#
#  Button - Clear Forms
#

    def clear_budgetcats_form(self):

        self.entUserCategory.delete(0, tk.END)   
        self.entUserType.delete(0, tk.END)   
        self.entMonth01.delete(0, tk.END) 
        self.entMonth02.delete(0, tk.END)
        self.entMonth03.delete(0, tk.END) 
        self.entMonth04.delete(0, tk.END) 
        self.entMonth05.delete(0, tk.END) 
        self.entMonth06.delete(0, tk.END) 
        self.entMonth07.delete(0, tk.END) 
        self.entMonth08.delete(0, tk.END) 
        self.entMonth09.delete(0, tk.END) 
        self.entMonth10.delete(0, tk.END) 
        self.entMonth11.delete(0, tk.END) 
        self.entMonth12.delete(0, tk.END) 
