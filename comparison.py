import cv2
import face_recognition

known_pic_of_ian = face_recognition.load_image_file("frame8.png")
unknown_pic = face_recognition.load_image_file("frame7.png")


ian_encoding = face_recognition.face_encodings(known_pic_of_ian)[0]
unknown_encoding = face_recognition.face_encodings(unknown_pic)[0]


comparison = face_recognition.compare_faces([ian_encoding],unknown_encoding)
print(comparison)