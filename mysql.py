#!/usr/bin/env python
import mysql.connector

db = mysql.connector.connect(host="35.185.221.29",    # your host, usually localhost
                     user="ian",         # your username
                     passwd="e",  # your password
                     db="test")        # name of the data base
cur = db.cursor()

def insert_users(table_name, values):
	sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
	username, password = values
	val = (username, password)
	cur.execute(sql, val)
	db.commit()

def insert_messages(values):
	sql = "INSERT INTO messages (message_body, receipient, sender) VALUES (%s, %s, %s)"
	message_body, receipient, sender = values
	val = (message_body, receipient, sender)
	cur.execute(sql, val)
	db.commit()

def query(table_name):
	cur.execute("SELECT * FROM " + table_name)
	result = cur.fetchall()
	for x in result:
		print(x)
# value = ("body", "ian", "spencer")
# insert_messages(value)
query("users")

cur.execute("SHOW TABLES") 
for (table_name,) in cur:
	print(table_name)

# cur.execute("ALTER TABLE messages ADD COLUMN receipient VARCHAR(25)")
# cur.execute("ALTER TABLE users ADD COLUMN photo LONGBLOB")
#cur.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# cur.execute('CREATE TABLE users (username VARCHAR(50), password VARCHAR(50))')
# cur.execute('CREATE TABLE messages (message_body VARCHAR(255))')
# cur.execute('INSERT INTO users (username, password) VALUES("spencer", "password")')
# cur.execute('INSERT INTO users (username, password) VALUES("ian", "fuck")')
