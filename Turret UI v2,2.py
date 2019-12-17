# USAGE
# python fps_demo.py
# python fps_demo.py --display 1

# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import sys
import os
import time
import serial
import numpy as np

start_time = time.time()

FACE_LOCATION_POINTER_X = 0
FACE_LOCATION_POINTER_Y = 0
x = 0
y = 0

port = 0
ports = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontWhite = (255, 255, 255)
fontGreen = (0, 255, 0)
fontRed = (0, 0, 255)
fontOrange = (102, 178, 255)
orange_orange = (0, 128, 255)
serial_port = sys.argv[2]
lineType = 1
radius = 10

screen_res = 1280, 720

info = np.zeros((512,512,3), np.uint8)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


# construct the argument parse and parse the arguments

def cv2_text(text, fontColour, location):
	cv2.putText(info, text, location, font, fontScale, fontColour, lineType)


# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling infos from web cam...")
stream = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('info', cv2.WINDOW_NORMAL)

fps = FPS().start()

# loop over some infos

# created a *threaded *video stream, allow the camera senor to warm up,
# and start the FPS counter
print("[INFO] sampling THREADED infos from web cam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

if sys.argv[1] == "-s":
	try:
		ser = serial.Serial(serial_port)

		if serial_port == sys.argv[1]:
			ports = 1
	except serial.SerialException:
		print("Could not open SER port. Running without SER. Use '--help' to see usage/option")
		ports = 0

# loop over some infos...this time using the threaded stream
while True:
	frame = vs.read()
	cv2.rectangle(info, (0, 1000), (512, 0), orange_orange, -1)
	cv2.rectangle(info, (10, 710), (500, 10), fontOrange, 1)
	cv2.rectangle(info, (0, 0), (1278, 500), orange_orange, 5)

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
	cv2_text("POINTER: X=" + str(FACE_LOCATION_POINTER_X) + ", Y=" + str(FACE_LOCATION_POINTER_Y), fontWhite, (15, 40))
	cv2_text("FACES LEN: " + str(len(faces)), fontWhite, (15, 55))
	cv2_text("FPS: " + "15", fontWhite, (15, 70))
	cv2_text("CAM: " + str(stream), fontWhite, (15, 85))
	cv2_text("MAX DETECTION DIS: 10m", fontWhite, (15, 100))
	cv2_text("NEIGHBORS: " + str(10), fontWhite, (15, 130))
	cv2_text("TIME SINCE START: " + str(round(time.time() - start_time, 3)), fontWhite, (15, 145))  # start time

	# end of text on panel

	cv2_text("PRESS 'SPACE' TO EXIT.", fontWhite, (15, 705))
	if ports == 1:
		cv2_text("PORT NAME: " + str(sys.argv[1]), fontWhite, (15, 115))
	else:
		cv2_text("WARNING: RUNNING WITHOUT SER", fontRed, (15, 115))
		print("[WARN] Running without ser. turret will not move")

	if len(faces) == 1:
		if ports == 1:
			cv2_text("LASER: ON", fontWhite, (15, 25))
			ser.write("laser_on")
	else:
		cv2_text("LASER: OFF", fontWhite, (15, 25))
		if ports == 1:
			ser.write("laser_off")
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), fontRed, 1)
		LASER_STAT = 1
		FACE_LOCATION_POINTER_X = x
		FACE_LOCATION_POINTER_Y = y
		cv2.line(frame, (100000, y + h // 2), (0, y + h // 2), fontRed, 1)
		cv2.line(frame, (x + w // 2, 100000), (x + w // 2, 0), fontRed, 1)
		#cv2_text("" + str(x + w // 2) + ":" + str(y + h // 2), fontWhite, (x, y + 15))

	cropped = frame[1:900, 1:1000]
	cv2.imshow("frame", cropped)
	cv2.imshow("info", info)
	fps.update()
	key = cv2.waitKey(1)
	if key == 32:
		break

# update the FPS counter

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
