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
    tables = data.find_all('tbody')
    #
    # add all rows of table 0 to the df created
    for row in tables[0].find_all('tr'):
        col = row.find_all('td')
        if len(col)!=0:
            print(col)

    #
    # return
    return df


def transform(df:pd.DataFrame)->pd.DataFrame:
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    return df


def load_to_csv(df:pd.DataFrame, csv_path:str):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''


def load_to_db(df:pd.DataFrame, sql_connection:sqlite3.Connection, table_name:str):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''


def run_query(query_statement:str, sql_connection:sqlite3.Connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''


def log_progress(message:str):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. 
    Function returns nothing
    '''


''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

extract(url,table_attribs)