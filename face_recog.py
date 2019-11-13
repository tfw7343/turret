import os
import cv2
import serial #documentation: https://pythonhosted.org/pyserial/
import time
import sys
import numpy as np
import math
import serial
# ser = serial.Serial('/dev/ttyUSB0')  # open serial port
# print(ser.name)         # check which port was really used

framerate = 30


#ser = serial.Serial("/dev/cu.usbserial-1410",timeout=1)

def sendData(data):
    #ser.write(bytes(data))
    print("")


"""
radius = 60;
angle  = 140;
xthing = radius * Math.sin(Math.PI * 2 * angle / 360);
ything = radius * Math.cos(Math.PI * 2 * angle / 360);
print('Points coors are  x='+ math.round(x * 100) / 100 +', y=' + math.round(y * 100) / 100)"""

# formula to detect the co-ords of the face in the camera
# x_face = radius * Math.sin(Math.PI * 2 * angle / 360);

# y_face = radius * Math.cos(Math.PI * 2 * angle / 360);



font = cv2.FONT_HERSHEY_SIMPLEX
#bottomLeftCornerOfText = (x,y)# moveed to ine 46
fontScale = 0.5
fontColor = (255,255,255)
lineType = 2
radius = 10

#haarcascade = https://pysource.com/wp-content/uploads/2018/10/haarcascades.zip

def nothing(x):
    pass


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)


cv2.namedWindow("Frame")
cv2.createTrackbar("Neighbours", "Frame", 5, 20, nothing)

while True:
    fps = int(cap.get(5))
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    neighbours = cv2.getTrackbarPos("Neighbours", "Frame")

    faces = face_cascade.detectMultiScale(gray, 1.3, neighbours)
    for rect in faces:

        (x, y, w, h) = rect
        bottomLeftCornerOfText = (x,y)

        p1 = (x, y )
        p2 = (x + w // 2, y + h) #bottom point
        p3 = (x + w, y ) #top line

        # Drawing the triangle
        # on the black window With given points
        cv2.line(frame, p1, p2, (0, 0, 255), 3)
        cv2.line(frame, p2, p3, (0, 0, 255), 3)
        cv2.line(frame, p1, p3, (0, 0, 255), 3)


        cv2.putText(frame,"x = " + str(x) + " y= " + str(y), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        cv2.imshow("Frame", frame)


        degrees = math.atan2(y,x)/math.pi * 180

            print("y position = " + str(round(degrees, 1)))
            time.sleep(0.1)
            os.system("clear")


        #         # (X, Y) = (x1 + x2 + x3//3, y1 + y2 + y3//3)
        centroid = ((p1[0]+p2[0]+p3[0])//3, (p1[1]+p2[1]+p3[1])//3)

        # detects the angle of the face on the circle using y

        key = cv2.waitKey(1)
        if key == 32:#32 = space key
            ser.close()
            break

cap.release()
cv2.destroyAllWindows()
ser.close()
