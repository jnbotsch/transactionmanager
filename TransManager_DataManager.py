##
##  Transaction Manager for Mint
##  Created By:  Jeff Botsch
##  
##   DataManager - Version 2.0
##
##   - Leverages sqlite3 and pandas to return dataframes.
##   - Ensures constant CSV file integrity as CSV files are the system of record. 
##   - SQL is only required for a complex LIKE join not available in Mint.
##   - Expanded usage of SQL as a personal learning opportunity.
##

import sqlite3
import pandas as pd

from datetime import datetime
from pathlib import Path

##
##  Class - Main
##

class TransManager_DataManager():

    def __init__(self):  
        super().__init__()  

        ##  create a connection
        self.db_connection = sqlite3.connect('TransManagerDB.db')

        ##  creating database_cursor to perform SQL operation   
        self.db_cursor = self.db_connection.cursor()

##
##  Load Transactions
##

    def load_transactions(self, csv_var):

            self.db_cursor.execute('DROP INDEX IF EXISTS transactions_idx')

            ##  Read the transaction file,
            pd_reader = pd.read_csv(f'{csv_var}.csv')
            transactions_df = pd.DataFrame(pd_reader)

            ##  Mark duplicate records.
            bool_series1 = transactions_df.duplicated(keep='first')
            bool_series1.colums = ['Dups']
            transactions_df =pd.concat([transactions_df, bool_series1], axis="columns")

            ##  Allow for another level of duplicate records.
            bool_series2 = transactions_df.duplicated(keep='first')
            bool_series2.colums = ['Dups2']
            transactions_df =pd.concat([transactions_df, bool_series2], axis="columns")

            ##  Rename columns, replace all NaN elements with 0s
            transactions_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups','Dups2']
            transactions_df['Amount'] = transactions_df['Amount'].fillna(0)

            ##  Write dataframe to SQL
            transactions_df.to_sql('transactions', self.db_connection, if_exists='replace', index=False)
            
            ##  Create index to establish unqiue key
            self.db_cursor.execute('CREATE UNIQUE INDEX transactions_idx on transactions (Date,OriginalDesc,Amount,Type,Category,Account,Dups,Dups2)')

#
# Add Transactions
#

    def add_transactions(self, csv_var):

            ###  Read the transaction file.
            pd_reader = pd.read_csv(f'{csv_var}.csv')
            transprevious_df = pd.DataFrame(pd_reader)

            ##  Mark duplicate records.
            bool_series1 = transactions_df.duplicated(keep='first')
            bool_series1.colums = ['Dups']
            transactions_df =pd.concat([transactions_df, bool_series1], axis="columns")

            ##  Allow for another level of duplicate records.
            bool_series2 = transactions_df.duplicated(keep='first')
            bool_series2.colums = ['Dups2']
            transactions_df =pd.concat([transactions_df, bool_series2], axis="columns")

            ##  Rename columns, replace all NaN elements with 0s
            transactions_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups','Dups2']
            transactions_df['Amount'] = transactions_df['Amount'].fillna(0)

            ##  Write dataframe to SQL
            insert_query = "INSERT OR REPLACE INTO transactions (Date, Description, OriginalDesc, Amount, Type, Category, Account, Label, Notes, Dups, Dups2) VALUES (?,?,?,?,?,?,?,?,?,?,?)"  

            ##  No mass upsert, need to spin through all rows
            for index, row in transprevious_df.iterrows():
                self.db_cursor.execute(insert_query, tuple(row))

#
# Read Transactions
#

    def read_transactions(self):
        
        ##  Load the required CSV files.
        trans_budgetcats_df     = self.load_csv_to_sql('trans_budgetcats')
        trans_defaultacct_df    = self.load_csv_to_sql('trans_defaultacct')
        trans_defaultdesc_df    = self.load_csv_to_sql('trans_defaultdesc')
        trans_extensions_df     = self.load_transextensions()

        ##  Create the overall allrows_qeruy join statement.
        join_transdefaultacct_query = "JOIN trans_defaultacct a on t.Account=a.UserAccount "
        leftjoin_transdefault_query = "LEFT JOIN trans_defaultdesc d ON t.OriginalDesc LIKE '%'||d.UserDefaultDesc||'%' "
        leftjoin_transextension_query = "LEFT JOIN trans_extensions e on t.Date=e.Date and t.OriginalDesc=e.OriginalDesc and t.Amount=e.Amount and t.Type=e.Type and t.Account=e.Account "

        allrows_query = "SELECT t.Date, t.Description, t.OriginalDesc, t.Amount, t.Type, t.Category, t.Account, t.Label, t.Notes, t.Dups, e.UserDate, e.UserCategory, e.UserNotes, d.UserCategory FROM transactions t "
        allrows_query = allrows_query + join_transdefaultacct_query + leftjoin_transextension_query + leftjoin_transdefault_query

        ##  Execute the query
        self.db_cursor.execute(allrows_query)

        ##  Build and return the dataframe
        transactions_df = pd.DataFrame(self.db_cursor.fetchall())
        transactions_df.columns = ['Date','Description','OriginalDesc','Amount','Type','Category','Account','Label','Notes','Dups', 'UserDate', 'UserCategory','UserNotes','DefaultCategory']
        transactions_df['ReportCategory'] = transactions_df['UserCategory']
        transactions_df['ReportDate']   = transactions_df['UserDate']
        transactions_df = transactions_df.astype({'Amount':'float'})

        for ind in transactions_df.index:

            # Set the Report Date from the Extension Table
            if transactions_df['ReportDate'][ind] is None:
                transactions_df['ReportDate'][ind] = transactions_df['Date'][ind]

            # Convert Report Date
            date_string = transactions_df['ReportDate'][ind]
            date_time_obj = datetime.strptime(date_string, '%m/%d/%Y')
            transactions_df['ReportDate'][ind] = date_time_obj
            transactions_df['ReportDate'][ind] = transactions_df['ReportDate'][ind].strftime('%Y-%m')

            # Set the Report Budget from the Company Table
            if transactions_df['ReportCategory'][ind] is None:
                transactions_df['ReportCategory'][ind] = transactions_df['DefaultCategory'][ind]

            # Set the Report Budget from the Category
            if transactions_df['ReportCategory'][ind] is None:  
                transactions_df['ReportCategory'][ind] = transactions_df['Category'][ind]

            # If not category is configured, set to a default value
            if transactions_df['ReportCategory'][ind] not in trans_budgetcats_df:
                transactions_df['ReportCategory'][ind] = "------"

            # Turn Debits into negaive numbers
            if transactions_df['Type'][ind] == 'debit':
                transactions_df['Amount'][ind] = -abs(transactions_df['Amount'][ind])

        return transactions_df

#
# Load Trans_Extensions dataframe
#

    def load_transextensions(self):

        self.db_cursor.execute('DROP INDEX IF EXISTS trans_extensions_idx')
        transextension_df = self.load_csv_to_sql('trans_extensions')
        self.db_cursor.execute('CREATE UNIQUE INDEX trans_extensions_idx on trans_extensions (Date, OriginalDesc, Amount, Type, Account)')
        
        return transextension_df

#
# Update Trans_Extensions table and file
#

    def update_transextensions(self, transextensions_tuple):

        insert_query = "INSERT OR REPLACE INTO trans_extensions (Date, OriginalDesc, Amount, Type, Account, UserDate, UserCategory, UserNotes) VALUES (?,?,?,?,?,?,?,?)"
        self.db_cursor.execute(insert_query, transextensions_tuple)
        self.db_connection.commit

        self.load_sql_to_csv('trans_extensions')

#
# Delete Trans_Extensions table and file
#

    def delete_transextensions(self, transextensions_tuple):  

        delete_query = "DELETE from trans_extensions where Date=? and OriginalDesc=? and Amount=? and Type=? and Account=?"
        self.db_cursor.execute(delete_query, transextensions_tuple)
        self.db_connection.commit

        self.load_sql_to_csv('trans_extensions')
        
#
# Load Trans_Defaults dataframe
#

    def load_transdefaults(self):

        self.db_cursor.execute('DROP INDEX IF EXISTS trans_defaultdesc_idx')
        trans_defaultdesc_df = self.load_csv_to_sql('trans_defaultdesc')
        self.db_cursor.execute('CREATE UNIQUE INDEX trans_defaultdesc_idx on trans_defaultdesc (UserDefaultDesc)')

        return trans_defaultdesc_df

#
# Update Trans_Defaults table and file
#

    def update_transdefaults(self, transdefaults_tuple):

        insert_query = "INSERT OR REPLACE INTO trans_defaultdesc (UserDefaultDesc, UserCategory) VALUES (?,?)"
        self.db_cursor.execute(insert_query, transdefaults_tuple)
        self.db_connection.commit

        self.load_sql_to_csv('trans_defaultdesc')

#
# Delete Trans_Defaults table and file
#

    def delete_transdefaults(self, transdefaults_tuple):  

        delete_query = "DELETE from trans_defaultdesc where UserCategory=?"
        self.db_cursor.execute(delete_query, transdefaults_tuple)
        self.db_connection.commit

        self.load_sql_to_csv('trans_defaultdesc')

#
# Check if CSV files exist and created is required
#

    def verify_create_csv(self,csv_var):  

        path_to_file = f'{csv_var}.csv'
        path = Path(path_to_file)

        if path.is_file():
            print(f'The file {path_to_file} exists')
        else:
            if csv_var == "trans_extensions":
                data = {'Date':['12/12/1900'], 'OriginalDesc':['default'],'Amount':['0.0'],'Type':['default'],'UserCategory':['default'],'UserNotes':['default']}
            
            elif csv_var == "trans_budgetcats":
                data = {'UserCategory':['------'],'UserType':['default'],'Month01':['0.0'],'Month02':['0.0'],'Month03':['0.0'],'Month04':['0.0'],'Month05':['0.0'],'Month06':['0.0'],'Month07':['0.0'],'Month08':['0.0'],'Month09':['0.0'],'Month10':['0.0'],'Month11':['0.0'],'Month12':['0.0'],'YearTotal':['0.0']}
            
            elif csv_var == "trans_defaultdesc":
                data = {'UserDefaultDesc':['default'], 'UserCategory':['default']}
            
            elif csv_var == "trans_defaultacct":
                data = {'UserAccount':['default']}

            temp_df = pd.DataFrame(data)
            temp_df.to_csv(f'{csv_var}.csv', index=False)

#
# Load CSV to SQL
#

    def load_csv_to_sql(self, csv_var):
 
        pd_reader = pd.read_csv(f'{csv_var}.csv')
        csv_df = pd.DataFrame(pd_reader)
        csv_df.to_sql(csv_var, self.db_connection, if_exists='replace', index=False)
        return csv_df

#
# Load SQL to CSV
#

    def load_sql_to_csv(self, sql_var):
        
        query = "SELECT * FROM "+ sql_var
        sql_df = pd.read_sql_query(query, self.db_connection)
        sql_df.to_csv(f'{sql_var}.csv', index=False)

#
# Backup CSV Files
#

    def backup_csv_files(self, csv_var):  

        pd_reader = pd.read_csv(f'{csv_var}.csv')
        backup_extensions_df = pd.DataFrame(pd_reader)
        csv_backup = "backup_" + f'{csv_var}.csv'
        backup_extensions_df.to_csv(csv_backup, index=False)
