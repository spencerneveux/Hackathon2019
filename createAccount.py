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

# Create database
database = TinyDB("/Users/spencerneveux/Desktop/Hackathon/ChatApp/db.json")
database.purge()
database.insert({"username": 'spencer', "password": 'password'})
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
    create_user(user_name, password)

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
        cv2.imshow('Video', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

# -------------------------------------------
# Login
# -------------------------------------------   
def login():
    user_name, password = credential_login()
    # Find that matching user in the database
    User = Query()

    # Search for that user
    user = database.search(User.user_name==user_name & User.password==password)
    # Get the image from that user
    image = user['image']
    print(image)
    facial_login()
    find_user()

# -------------------------------------------
# Method to get username/password
# -------------------------------------------
def credential_login():
    user_name = input("Enter username\n")
    password = input("Enter pasword\n")
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
def find_user():
    # Get an image from the database for that user
    known_user_image = face_recognition.load_image_file("frame8.png")

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
    else:
        print("THAT'S NOT YOU!")
    return comparison

# -------------------------------------------
# Email Stuff
# -------------------------------------------
def email():
    yag = yagmail.SMTP('spencerneveux@gmail.com', 'kvlaiyiycdkncahi')
    # Collect Email address to send to
    recipient = input("To: ")
    # Subject
    subject = input("Subject: ")
    # Body
    text_body = input("Message: ")
    # Encrypt message
    image = encrypt_message(text_body)
    contents = ["This is a super secret message"]
    yag.send(recipient, subject, contents, attachments=image)
    print("SENT!")

# -------------------------------------------
# Steganography Stuff
# -------------------------------------------
def encrypt_message(user_message):
    # Take the user message and save it in the image
    secret_message = lsb.hide("/Users/spencerneveux/Desktop/Hackathon/ChatApp/Images/cat.png", user_message)
    secret_message.save("/Users/spencerneveux/Desktop/Hackathon/ChatApp/Images/secret_cat.png")
    return "/Users/spencerneveux/Desktop/Hackathon/ChatApp/Images/secret_cat.png"

def decrypt_message(image_path):
    decrypted_message = lsb.reveal()
    print(decrypted_message)

# -------------------------------------------
# Database
# -------------------------------------------
def create_user(username, password):
    image_path = 'frame5.png'
    database.insert({'username': username, 'password': password, 'image': image_path})
    print(database.all())

# -------------------------------------------
# MAIN!
# -------------------------------------------
def main():
    # # Collect user input
    # user_input = input("1.Sign Up\n2.Login\n3.Exit\n")
    # if user_input == "1":
    #     sign_up()
    # elif user_input == "2":
    #     login()
    #     comparison_result = find_user()
    #     if comparison_result[0] == True:
    #         email()
    # elif user_input == "3":
    #     break
    User = Query()
    user = database.search(User.username=='spencer')
    print(user[0]['password'])
main()
