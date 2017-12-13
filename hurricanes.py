#Imports
from __future__ import division
from bs4 import BeautifulSoup
import sqlite3
import hurricane_helper as help



#Set up SQL database
conn = sqlite3.connect("hurricanes.db")
conn.execute('''CREATE TABLE if not exists ATLANTIC_HURRICANES
      (YEAR INT,
      TROPICAL_STORMS INT,
      HURRICANES INT,
      MAJOR_HURRICANES INT,
      DEATHS INT,
      DAMAGE INT,
      NOTES TEXT);''')

conn.commit()

#Set up beautiful soup

soup = BeautifulSoup(open("hurricanes.html", 'r'), "lxml")

# Pull tables out of soup

#Ignoring first table loop through all other tables in the html file
for table in soup.find_all('table')[1:]:
    #get the headings of the table from the first row
    headings = help.table_mapper(table.find_all('tr')[0])
    #loop through each actual data row of each table
    for row in table.find_all('tr')[1:]:
        #fit the data to the format of our db
        row_data = help.fit_data(row, headings)
        #and put it in the database
        help.put_db(row_data)
conn.close()

print("\nDatabase setup complete.")


