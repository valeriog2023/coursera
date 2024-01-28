import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy
from datetime import datetime
# This script extract the list of all countries in order of their GDPs in billion USDs 
# (rounded to 2 decimal places), as logged by the International Monetary Fund (IMF). 
# The required data seems to be available on the URL mentioned below:

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

# The script will also save the data as CSV as well as a table in a sqlite3 DB
csv_file = 'Countries_by_GDP.csv'
table_name = 'Countries_by_GDP'
table_attribs = [ 'Country', 'GDP_USD_millions' ]
db_name = 'World_Economies.db' 


# Logs are save to a file
log_file = 'etl_project_log.txt'


# Code for ETL operations on Country-GDP data
# Importing the required libraries
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
        return 
    #
    # get the data into a BS object, find all the tables
    # from visual inspection, our data is in the first table
    data = BeautifulSoup(r.text, 'html.parser')
    #
    # I used a different approach here.. checking the caption of the table
    # instead of hardcoding the index of the table..
    # The table has the caption: 'GDP (USD million) by country'
    # so we find all the captions and when we get this one we get the parent item
    table = None
    for caption in data.find_all('caption'):
        if caption.text.strip().lower() == 'GDP (USD million) by country'.lower():
            print("Found table: GDP (USD million) by country")
            table = caption.parent
            break
    if table == None:
        print("Could not find table: GDP (USD million) by country")
        return
    #
    # add all rows in the table and create the df   
    rows = table.find_all('tr')
    skipped_count = 0
    for row in rows:
        cols = row.find_all('td')
        # skipping a row if either of these 3 conditions is met
        if len(cols) == 0 or \
           cols[0].find('a') is None or \
           '-' in str(cols[2]):
            #print(f"skipping row: {cols}")
            skipped_count += 1
            continue
        # Create the data dict
        # I tries to use cols[0].text but it gives extra heaxdecimal chars
        # so what you want here is the caption isnide the hyperlink       
        data_dict = { "Country": cols[0].a.text,
                      "GDP_USD_millions": cols[2].text
                    }
        # Now we concat the existing df with a new DF created with the dict  
        # note that the index=[0] is required when you create a df from a simple dict          
        df = pd.concat([ df,
                         pd.DataFrame(data_dict, index=[0]) ],
                        ignore_index = True
                       )
    
    print(f"Parsed total {len(rows)} rows: good {len(rows)-skipped_count} , skipped {skipped_count} ")    
    print("DF preview (first 5 rows:)") 
    print(df.head(5))
    print("----")
    #
    # return
    return df


def transform(df:pd.DataFrame)->pd.DataFrame:
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    df['GDP_USD_billions'] = df['GDP_USD_millions'].apply(lambda x: round(float(str(x).replace(',',''))/1000,2)) 
    df1 = df[['Country','GDP_USD_billions']]
    print("DF preview after transformation (first 5 rows:)") 
    print(df1.head(5))
    print("----")
    return df1


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


def log_progress(message:str):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. 
    Function returns nothing
    The log message is prepended with a timestamp in the format # Year-Monthname-Day-Hour-Minute-Second 
    '''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    # Note: log_files is defined as a global var to ='etl_project_log.txt'
    with open(log_file,"a") as f: 
        f.write(timestamp + ' : ' + message + '\n')



''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

log_progress('Starting ETL process: extract')
df = extract(url, table_attribs)

log_progress('Extract complete. Starting: Transform')
df = transform(df)

log_progress('Transform complete. Starting: Loading')
load_to_csv(df, csv_file)
log_progress(f'Data saved to CSV file: {csv_file}')
#
# Note: db_name and table names are set as global vars
sql_connection = sqlite3.connect(db_name)
load_to_db(df, sql_connection, table_name)
log_progress(f'Data loaded to Database: {db_name} as table {table_name}. Running the query')
#
query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, sql_connection)
#
sql_connection.close()
log_progress('Connection to DB closed.')
log_progress('Process Complete.')

