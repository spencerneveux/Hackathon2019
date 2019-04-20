import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

#udjut for size and color
face_captured = False
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
face_count = 0
count = 5


while count > 0:
	print(count)
	count -= 1
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
    	sleep(.25) # wait inbetween pics
    	#cv2.imshow("frame.png", frame)
    	face_count += 1
    	print("captured image")
    if count == 10:
    	video_capture.release()
    	cv2,destroyAllWindows()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

 	# Draw a rectangle around the face(s)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
	
#---------------------------------------------
# Now user login
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
        cv2.imwrite("Login_frame" + str(face_count) + ".png", frame)
        break


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

login_video_capture.release()
cv2.destroyAllWindows()
