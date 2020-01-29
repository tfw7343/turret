# USAGE
# python fps_demo.py
# python fps_demo.py --display 1

# import the necessary packages

import sys
import datetime

import cv2
import numpy as np
import serial
from imutils.video import FPS
from imutils.video import WebcamVideoStream


start_time = datetime.datetime.utcnow()

FACE_LOCATION_POINTER_X = 0
FACE_LOCATION_POINTER_Y = 0
x = 0
y = 0

Total_faces = 0
total_faces1 = 0
Face_detect_last = 0
Open_port = 0
eyes = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontWhite = (255, 255, 255)
fontGreen = (0, 255, 0)
fontRed = (0, 0, 255)
fontOrange = (102, 178, 255)
orange_orange = (0, 128, 255)

filename = "RECORDING_" + str(datetime.datetime.utcnow())

try:
	serial_port = sys.argv[2]
except IndexError:
	serial_port = ""
	pass

lineType = 1
radius = 10

screen_res = 1280, 720

info = np.zeros((512, 512, 3), np.uint8)

faceCascade = cv2.CascadeClassifier("Haarcascades\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("C:\\Users\\teren.LAPTOP-1DP9K0KI\\Project\\Files\\Haarcascades\\RTMaps_test_tools_opencv_haarcascades_haarcascade_lefteye_2splits.xml")
port = 0
ports = 0

#cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)


def Log_clear():
	log_target = open("logs\Log.txt", "w")
	log_target.write("")
	log_target.close()


Log_clear()


def Log(log):
	log_file = open("logs\Log.txt", "a")
	Data = log + "\n"
	log_file.write(Data)
	print(log)
	log_file.close()


def write_error(error1):
	error2 = open("logs\Error_report", "w")
	error2.write(error1)
	error2.close()


def send_data(data):
	Error = open("logs\Error_report", "r")  # reads for open port. if port closed stat = 0
	stat = Error.readline()
	if stat == "1":
		try:
			ser.write(data)
			write_error("1")
		except serial.serialutil.SerialException:
			Log("[WARN] LOST CONNECTION TO SER. RETURNING TO NORMAL PROCESSES WITHOUT SER. ERROR == serialutil.SerialException")
			write_error("0")

	elif stat == 0:
		Log("[WARN] LOST CONNECTION TO SER. RETURNING TO NORMAL PROCESSES WITHOUT SER")
		write_error("0")
def cv2_text(text, fontColour, location):
	cv2.putText(info, text, location, font, fontScale, fontColour, lineType)


# grab a pointer to the video stream and initialize the FPS counter
Log("-" * 10 + "[START " + str(datetime.datetime.utcnow()) + "]" + "-" * 10)
Log("[INFO] sampling frames from web cam...")
stream = cv2.VideoCapture(3)
fps = stream.get(cv2.CAP_PROP_FPS)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('info', cv2.WINDOW_NORMAL)

Log("[INFO] sampling THREADED frames from web cam...")
vs = WebcamVideoStream(src=1).start()
fps = FPS().start()

try:
	if sys.argv[1] == "-s":
		try:
			ser = serial.Serial(serial_port)
			send_data("")

			if serial_port == sys.argv[2]:
				ports = 1
				write_error("1")
				Log("[ OK ] Connection established with SER")
				Log("[INFO] Port name: " + sys.argv[2])
			else:
				Log("[WARN] Running without ser. Turret will not move (Options not specified)")
				pass
		except serial.SerialException:
			Log("[HELP] Could not open SER port. Running without SER. Use '--help' to see usage/option")
			ports = 0
			Log("[WARN] Running without ser. turret will not move")
			write_error("0")
	else:
		Log("[WARN] Running without ser. Turret will not move (Options not specified)")
except IndexError:
	Log("[WARN] Running without ser. Turret will not move (-s not specified)")
	pass


Log("[INFO] CAM name: " + str(stream))

def getleftmosteye(eyes1):
	leftmost=9999999
	leftmostindex=-1
	for i in range(0,2):
		if eyes1[i][0] < leftmost:
			leftmost = eyes1[0][i]
			leftmostindex = i
		return eyes1[leftmostindex]
# loop over some frames...this time using the threaded stream
while True:
	frame = vs.read()
	cv2.rectangle(info, (0, 1000), (512, 0), orange_orange, -1)
	cv2.rectangle(info, (10, 710), (500, 10), fontOrange, 1)
	cv2.rectangle(info, (0, 0), (1278, 500), orange_orange, 5)


	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=8,
		minSize=(30, 30),
	)

	if len(faces) == 1:
		if Face_detect_last == 0:
			Face_detect_last = 1
			Total_faces += 1
			Log("[INFO] New face found at " + str(datetime.datetime.utcnow()) + ": Current Total Faces detected: " + str(Total_faces))
	elif len(faces) == 0:
		Face_detect_last = 0

	# text on panel
	cv2_text("LASER POINTER: X=" + str(FACE_LOCATION_POINTER_X) + ", Y=" + str(FACE_LOCATION_POINTER_Y), fontWhite, (15, 40))
	cv2_text("TOTAL FACES DETECTED: " + str(Total_faces), fontWhite, (15, 55))
	cv2_text("FPS: " + str(fps), fontWhite, (15, 70))
	cv2_text("CAM: " + str(stream), fontWhite, (15, 85))
	cv2_text("MAX DETECTION DIS: 10m", fontWhite, (15, 100))
	cv2_text("NEIGHBORS: " + str(18), fontWhite, (15, 130))
	cv2_text("START TIME: " + str(start_time), fontWhite, (15, 145))  # start time

	# end of text on panel

	cv2_text("PRESS 'SPACE' TO EXIT.", fontWhite, (15, 705))
	if ports == 1:
		cv2_text("PORT NAME: " + str(sys.argv[2]), fontWhite, (15, 115))
	else:
		cv2_text("WARNING: RUNNING WITHOUT SER", fontRed, (15, 115))

	if len(faces) == 1:
		Total_faces1 = Total_faces + 1
		if ports == 1:
			cv2_text("LASER: ON", fontWhite, (15, 23))
			send_data("laser_on\n")
	else:
		cv2_text("LASER: OFF", fontWhite, (15, 23))
		if ports == 1:
			send_data("laser_off\n")

	for (x, y, w, h) in faces:
		FACE_LOCATION_POINTER_X = (x + w // 2)
		FACE_LOCATION_POINTER_Y = (y + h // 2)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, 1.3, 5)
		cv2.line(frame, (100000, y + h // 2), (0, y + h // 2), fontRed, 1)
		cv2.line(frame, (x + w // 2, 100000), (x + w // 2, 0), fontRed, 1)
		cv2.putText(frame, "X=" + str(FACE_LOCATION_POINTER_X) + ":Y=" + str(FACE_LOCATION_POINTER_Y) , (x - 10, y - 10), font, fontScale, fontRed, 1)
		ser.write(str(FACE_LOCATION_POINTER_X) + ":" + str(FACE_LOCATION_POINTER_Y))
		Log(str(FACE_LOCATION_POINTER_X) + ":" + str(FACE_LOCATION_POINTER_Y))

		roi_gray = gray[y:y + h, x:x + w]
		roi_color = frame[y:y + h, x:x + w]
		eyes = eye_cascade.detectMultiScale(roi_gray)

		cv2.rectangle(frame, (x, y), (x + w, y + h), fontRed, 2)
		# for (ex, ey, ew, eh) in eyes:
		# 	LASER_stat = 1
		# 	cv2.line(roi_color, (100000, ey + eh // 2), (0, ey + eh // 2), fontRed, 1)
		# 	cv2.line(roi_color, (ex + ew // 2, 100000), (ex + ew // 2, 0), fontRed, 1)
		# 	cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)


	cropped = frame[1:900, 1:1000]
	cv2.imshow("frame", cropped)
	cv2.imshow("info", info)
	fps.update()
	key = cv2.waitKey(1)
	if key == 32:#ascii space
		Log("[STOP] '" + str(key) + "' HAS BEEN PUSHED... STARTING ENDING SEQUENCE")
		break
	elif key == ord("s"):
		out = cv2.VideoWriter(filename + '.avi', -1, 20.0, (640, 480))
		out.write(frame)
		Log("[SAVE] " + filename + ".avi" + " has been saved")

fps.stop()

Log("[INFO] Total faces detected: " + str(Total_faces1))
Log("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))
Log("[INFO] Elapsed time: {:.2f} Seconds".format(fps.elapsed()))
Log("-" *10 + "[END OF LOG {}]".format(datetime.datetime.utcnow()) + "-" * 10)

if ports == 1:
	ser.close()

cv2.destroyAllWindows()
vs.stop()
