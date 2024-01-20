# Download the csv file from  https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/INSTRUCTOR.csv
# This is a small script used as an example of an interaction with sqlite3
import pandas as pd 
import sqlite3

# If there is no DB this will create a DB which in this case is a file
# If there is, this will connect to the DB (i.e. open and read the file)
conn = sqlite3.connect('STAFF.db')

# Setting some values
table_name = 'INSTRUCTOR'
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']
# Assuming the file has been downloaded in the local folder
file_path = './INSTRUCTOR.csv'
# the csv has no columns.. so we use the ones defined above
df = pd.read_csv(file_path, names = attribute_list)

# This will create the table; note tha value of if_exists:
#.  if_exists = 'fail'	Default. The command doesn't work if a table with the same name exists in the database.
#.  if_exists = 'replace'	The command replaces the existing table in the database with the same name.
#. if_exists = 'append'	The command appends the new data to the existing table with the same name.
df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')

# Now runs a few queries
print("Running a few test queries using pd.read_sql(<query>,<conn>) now:")
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)
print("----")

query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)
print("----")

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)
print("----")

print("--- Now we append crafted new data via pandas")
data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}
# New dataframe with just one entry            
data_append = pd.DataFrame(data_dict)
# This uses the new df and the connection to append the local new data
data_append.to_sql(table_name, conn, if_exists = 'append', index =False)
print('Data appended successfully.. \nrunning COUNT Query Again')
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)
print("----")
conn.close()
print("Connection closed")