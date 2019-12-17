import cv2
import numpy as np
import sys
import serial
import os
import time
import calendar

start_time = time.time()

if sys.argv[2] == "--help":
    print("==========================<USAGE>==========================")
    print("== python GUI_recognition <serial_port_name> <options>   ==")
    print("===========================================================")
    print("")
    print("-s             |           Serial data is truned on; if not the turret will not move or shoot the lazer. To leave serial data off do not use -s")
    print("--help         |           Displays this help msg.")
    sys.exit()

ports = 0
port = 0
LASER_STAT = 0
TopRightCorner = (5, 15)

FACE_LOCATION_POINTER_X = 0
FACE_LOCATION_POINTER_Y = 0
fps = 0


escape_char = " "

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.4
fontWhite = (255, 255, 255)
fontGreen = (0, 255, 0)
fontRed = (0, 0, 255)
fontOrange = (102, 178, 255)
orange_orange = (0, 128, 255)
serial_port = sys.argv[1]
lineType = 1
radius = 10

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
video_capture1 = cv2.VideoCapture(0)
def cv2_textA(text, TopRightCorner1):
    cv2.putText(frame, text, TopRightCorner1, font, fontScale, fontRed, lineType)

def cv2_text(text, fontColour, location):
    cv2.putText(frame,text, location, font, fontScale, fontColour, lineType)

if sys.argv[2] == "-s":
    try:
        ser = serial.Serial(serial_port)

        if serial_port == sys.argv[1]:
            ports = 1
    except serial.SerialException:
        print("Could not open SER port. Running without SER. Use '--help' to see usage/option")
        ports = 0

while True:

    # Capture frame-by-frame
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    ret, frame = video_capture.read()
    ret1 , frame1   = video_capture1.read()
    cv2.rectangle(frame,(0, 1000),(300,0), orange_orange, -1)
    cv2.rectangle(frame,(10, 710),(290, 10), fontOrange, 1)
    cv2.rectangle(frame,(0,0),(1278,718), orange_orange, 5)

    if port == 1:
        ser.write("X" + str(x / 5) + ":Y" + str(y / 5))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30, 30),
    )
    # text on panel
    cv2_text("POINTER: X=" + str(FACE_LOCATION_POINTER_X)+ ", Y=" + str(FACE_LOCATION_POINTER_Y), fontWhite, (15,40))
    cv2_text("FACES LEN: " + str(len(faces)), fontWhite, (15, 55))
    cv2_text("FPS: " + str(fps), fontWhite, (15, 70))
    cv2_text("CAM: " + str(video_capture), fontWhite, (15,85))
    cv2_text("MAX DETECTION DIS: 10m", fontWhite, (15,100))
    cv2_text("NEIGHBORS: " + str(10), fontWhite, (15, 130))
    cv2_text("TIME SINCE START: " + str(round(time.time() - start_time, 3)), fontWhite, (15, 145)) #start time

    # end of text on panel


    cv2_text("PRESS 'SPACE' TO EXIT.", fontWhite, (15, 705))
    if ports == 1:
        cv2_text("PORT NAME: " + str(sys.argv[1]), fontWhite, (15, 115))
    else:
        cv2_text("WARNING: RUNNING WITHOUT SER", fontRed, (15,115))


    if len(faces) == 1:
        cv2_text("LASER: ON", fontWhite, (15,25))
        ser.write("laser_on")
    else:
        cv2_text("LASER: OFF", fontWhite, (15,25))
        ser.write("laser_off")
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x , y), (x+w, y+h), fontRed, 1)
        LASER_STAT = 1
        FACE_LOCATION_POINTER_X = x
        FACE_LOCATION_POINTER_Y = y
        cv2.line(frame, (100000, y + h // 2), (300, y + h // 2), fontRed, 1)
        cv2.line(frame, (x + w // 2, 100000), (x + w // 2, 0), fontRed, 1)
        cv2_text("" + str(x + w //2) + ":" + str(y + h // 2), fontWhite, (x, y + 15))

    # Display the resulting frame
    cv2.flip(frame, 0)
    cv2.imshow('TURRET UI', frame)

    if cv2.waitKey(1) == 32:
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
