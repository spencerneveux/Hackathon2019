#!/usr/bin/python
import mysql.connector

db = mysql.connector.connect(host="35.185.221.29",    # your host, usually localhost
                     user="ian",         # your username
                     passwd="e",  # your password
                     db="test")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
print(db)
cur = db.cursor()
#cur.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
cur.execute("SHOW TABLES") 
for (table_name,) in cur:
	print(table_name)
