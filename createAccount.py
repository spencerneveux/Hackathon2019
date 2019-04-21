import mysql.connector
import cv2 
import face_recognition
import numpy as np
import sys
import logging as log
import datetime as dt
from time import sleep
import smtplib
from stegano import lsb
import yagmail
from tinydb import TinyDB, Query

# -------------------------------------------
# MYSQL DATABASE
# -------------------------------------------
db = mysql.connector.connect(host="35.185.221.29",    # your host, usually localhost
                     user="ian",         # your username
                     passwd="e",  # your password
                     db="test")        # name of the data base
cur = db.cursor()

# # Drop all tables
# cur.execute("DROP TABLE users")
# cur.execute("DROP TABLE messages")
# # cur.execute("DROP TABLE pics")

# Create Tables
# cur.execute('CREATE TABLE users (username VARCHAR(50), password VARCHAR(50), image_path VARCHAR(255))')
# cur.execute('CREATE TABLE messages (message_body VARCHAR(255), person VARCHAR(50))')

def insert_users(values):
    sql = "INSERT INTO users (username, password, image_path) VALUES (%s, %s, %s)"
    username, password, image = values
    val = (username, password, image)
    cur.execute(sql, val)
    db.commit()

def insert_messages(values):
    sql = "INSERT INTO messages (message_body, person) VALUES (%s, %s)"
    message_body, person = values
    val = (message_body, person)
    cur.execute(sql, val)
    db.commit()

def query(table_name):
    cur.execute("SELECT * FROM " + table_name)
    result = cur.fetchall()
    for x in result:
        print(x)

def query_inbox(username):

    cur.execute("SELECT message_body FROM messages WHERE person = '" + username + "'")
    result = cur.fetchall()
    for x in result:
        print(x)

def get_image_path(user_name, password):
    sql = "SELECT image_path FROM users WHERE username = %s AND password = %s"
    user = (user_name, password)
    cur.execute(sql, user)
    result = cur.fetchall()
    return result

def show_all_tables():
    cur.execute("SHOW TABLES") 
    for (table_name,) in cur:
        print(table_name)

# Hard coding a user with their image
# xml cascade for opencv
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

# -------------------------------------------
# Sign Up
# -------------------------------------------
def sign_up():
    user_name, password = get_username_password()
    collect_user_images()
    values = (user_name, password, "/Users/spencerneveux/Desktop/Hackathon/ChatApp/frame8.png")
    insert_users(values)
    main()

# -------------------------------------------
# Method to sign up a user with specific
# username and password
# -------------------------------------------
def get_username_password():
    user_name = input("Enter username\n")
    password = input("Enter password\n")
    return user_name, password

# -------------------------------------------
# Method to sign up a user
# Collects a video feed from which 10 images
# are extracted to be stored in a database
# -------------------------------------------
def collect_user_images():

    face_captured = False
    face_count = 0
    for i in range(5):
    	print("Capturing in:" + str(i))
    	sleep(1)

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        successful__frame_capture, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

     	#display captured image
        if successful__frame_capture and face_count < 10:
        	cv2.imwrite("frame" + str(face_count) + ".png", frame)
        	sleep(.05) # wait inbetween pics
        	face_count += 1

        # If user enters q exit the video feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     	# Draw a rectangle around the face(s)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)

        # Display the resulting frame
        cv2.namedWindow("output")
        cv2.moveWindow("output", 100,100)
        cv2.imshow('output', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

# -------------------------------------------
# Login
# -------------------------------------------   
def login():
    user_name, password = credential_login()
    # Find that matching user in the database
    image_path = get_image_path(user_name, password)[0]
    image_path = image_path[0].strip('(),')
    print(image_path)
    facial_login()
    result = find_user(image_path)

    if result == True:
        user_choice = message_menu()
        if user_choice == '1':
            create_message()
        elif user_choice == '2':
            check_inbox(user_name)

    else:
        print("INVALID LOGIN!")

# -------------------------------------------
# Method to get username/password
# -------------------------------------------
def credential_login():
    user_name = input("Enter username\n")
    password = input("Enter password\n")
    return user_name, password

# -------------------------------------------
# Method to log the user in
# A video feed opens up wherein the user will
# hit c when they wish to capture their picture
# this image will be used to compare to database
# -------------------------------------------
def facial_login():
    # Open a video feed 
    login_video_capture = cv2.VideoCapture(0)
    # Display the video to user
    while True:
        # Collect the success message and frames
        success, frame = login_video_capture.read()

        # Gray out the frames for comparison
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = faceCascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Display video
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite("Login_frame.png", frame)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    login_video_capture.release()
    cv2.destroyAllWindows()

# -------------------------------------------
# Method to compare the login photo taken
# If user is indeed who they are logging in as
# Take them to message stage
# -------------------------------------------
def find_user(image_path):
    # Get an image from the database for that user
    known_user_image = face_recognition.load_image_file(image_path)

    # Get the image from the attempted login
    unknown_pic = face_recognition.load_image_file("Login_frame.png")

    # Encode the known/unknown face images
    known_encoding = face_recognition.face_encodings(known_user_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_pic)[0]

    # Determine if that person is the same
    comparison = face_recognition.compare_faces([known_encoding],unknown_encoding)

    # Print out the results
    if comparison[0] == True:
        print("Successful Login")
        return True
    else:
        print("THAT'S NOT YOU!")
        return False
    return comparison

# -------------------------------------------
# Main Menu
# -------------------------------------------
def main_menu():
    print("Welcome to Chatter")
    print()
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit\n")
    user_choice = input("")
    return user_choice

# -------------------------------------------
# Message Menu
# -------------------------------------------
def message_menu():
    print("1. Create Message")
    print("2. View Message")
    user_choice = input()
    return user_choice

# -------------------------------------------
# Message method
# -------------------------------------------
def create_message():
    receipient = input("TO: ")
    message_body = input("Enter your message\n")
    values = (message_body, receipient)
    insert_messages(values)
    
# -------------------------------------------
# Check inbox method
# -------------------------------------------
def check_inbox(username):
    # Find the messages associated my with username
    query_inbox(username)


# -------------------------------------------
# MAIN!
# -------------------------------------------
def main():
    # user_choice = main_menu()
    # if user_choice == '1':
    #     sign_up()
    # elif user_choice == '2':
    #     login()
    # query('users')
    username = "ian"
    query_inbox(username)

    # query('messages')
main()
