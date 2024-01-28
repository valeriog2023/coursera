#Objectives
# Use the requests and BeautifulSoup libraries to extract the contents of a web page
# Analyze the HTML code of a webpage to find the relevant information
# Extract the relevant information and save it in the required form
# Consider that you have been hired by a Multiplex management organization to extract the information 
# of the top 50 movies with the best average rating from the web link shared below.

import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# Setting some initial values
url="https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/project/top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

if __name__ == "__main__":
    # 1) Get the html page and init the BS object (tree)
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    #
    # 2) Finad all the tables (the table we want is the first one.. thi come from visual inspection)
    #    so we get all the rows from teh first table
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    #
    # 3) interate for all the rows (we stop at 50 anyway)
    for row in rows:
        if count<50:
            # get the list of cells
            col = row.find_all('td')
            if len(col)>=3:
                data_dict = {"Average Rank": col[0].contents[0],
                             "Film": col[1].contents[0],
                             "Year": col[2].contents[0]}
                # Create a new df with a single row and add it to df             
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
                count+=1
        else:
            break
    #
    # 3. Print the first lines of the DF and saving to file
    print(df.head(10))        
    print(f"Saving to: {csv_path}")
    df.to_csv(csv_path)
    print("done..")
    #
    # 4. Now createing sql lite db and saving there too
    print(f"Now creating DB(File)/table: {db_name}/{table_name} in SQL lite and saving there too..")
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print("done..")