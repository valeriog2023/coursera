# Importing the required libraries
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Get the exchange rate file from here:
# wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv

# Table Attributes (upon Extraction only)	Name, MC_USD_Billion
table_attribs = [ "Name", "MC_USD_Billion"]

def log_progress(message:str):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. 
    Function returns nothing
    The log message is prepended with a timestamp in the format # Year-Monthname-Day-Hour-Minute-Second 
    '''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open('code_log.txt',"a") as f: 
        f.write(timestamp + ' : ' + message + '\n')


def extract(url:str, table_attribs:list[str])->pd.DataFrame:
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    # Create an empty df
    df = pd.DataFrame(columns=table_attribs)
    # Get the web page text
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error while trying to get web page from: {url}")
        print(f'Status code: {r.status_code}') 
        print(f'{r.text}')
        raise Exception("Error during extract function")  
    #
    # get the data into a BS object, find all the tables
    # from visual inspection, our data is in the first table
    data = BeautifulSoup(r.text, 'html.parser')
    #
    # I used a different approach here.. checking the caption of the table
    # instead of hardcoding the index of the table..
    # The table has the caption: 'GDP (USD million) by country'
    # so we find all the captions and when we get this one we get the parent item
    tables = data.find_all('table')
    #
    # from visual analysis of source page, the correct table is the first in the list of tables
    # add all rows in the table and create the df   
    rows = tables[0].find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        #
        # the table has Rank, Name and MC_USD_Bilion
        # so skipping rows that don't have 3 elements
        if len(cols) != 3: continue
        # Create the data dict "Name", "MC_USD_Billion"
        data_dict = { "Name": cols[1].text.strip(),
                      "MC_USD_Billion": float(cols[2].text.strip())
                    }
        # Now we concat the existing df with a new DF created with the dict  
        # note that the index=[0] is required when you create a df from a simple dict          
        df = pd.concat([ df,
                         pd.DataFrame(data_dict, index=[0]) ],
                        ignore_index = True
                       )
    #
    # print the returning df and return
    print(df)
    return df

def transform(df:pd.DataFrame, csv_path:str)->pd.DataFrame:
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    exchange_df = pd.read_csv(csv_path)
    exchange_dict = exchange_df.set_index('Currency').to_dict()['Rate']
    #
    # Adding 3 columns for MC_GBP_Billion, MC_EUR_Billion and MC_INR_Billion
    df['MC_GBP_Billion'] = df['MC_USD_Billion'].apply(lambda x: round( exchange_dict['GBP'] * x, 2) )
    df['MC_EUR_Billion'] = df['MC_USD_Billion'].apply(lambda x: round( exchange_dict['EUR'] * x, 2) )
    df['MC_INR_Billion'] = df['MC_USD_Billion'].apply(lambda x: round( exchange_dict['INR'] * x, 2) )
    #
    # print and exit     
    print("-----")
    print(df['MC_EUR_Billion'][4])
    return df



def load_to_csv(df:pd.DataFrame, csv_path:str):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)



def load_to_db(df:pd.DataFrame, sql_connection:sqlite3.Connection, table_name:str):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)



def run_query(query_statement:str, sql_connection:sqlite3.Connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(f"Running: {query_statement}")
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)   
    print("---------") 


''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
#
log_progress('Preliminaries complete. Initiating ETL process')
# Data URL	https://web.archive.org/web/20230908091635 /
# https://en.wikipedia.org/wiki/List_of_largest_banks
bank_list_url = "https://en.wikipedia.org/wiki/List_of_largest_banks"
df = extract(bank_list_url, table_attribs)
#
log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df, 'exchange_rate.csv')
#
log_progress('Data transformation complete. Initiating Loading process')
load_to_csv(df, './Largest_banks_data.csv')
log_progress(f'Data saved to CSV file')
#
sql_connection = sqlite3.connect("Banks.db")
log_progress('SQL Connection initiated')
load_to_db(df, sql_connection, "Largest_banks")
log_progress(f'Data loaded to Database as a table, Executing queries')
#
#
query1 = "SELECT * FROM Largest_banks"
query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
query3 = "SELECT Name from Largest_banks LIMIT 5"
run_query(query1, sql_connection)
run_query(query2, sql_connection)
run_query(query3, sql_connection)
#
log_progress('Process Complete.')
#
#sql_connection.close()
log_progress('Server Connection closed.')
#
