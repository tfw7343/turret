import serial#send as "X90:Y90"



ser = serial.Serial("/dev/cu.usbserial-1410",timeout=1)


raw_input1 = raw_input(">>>")#use any number from 1-180

while True:
    ser.write(raw_input1())
    
