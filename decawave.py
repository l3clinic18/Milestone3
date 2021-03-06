import serial
import time
import re
import math
k = 2.0 # the number of samples in tau and diviser in the running average
counter = 0 #
measurement_duration = 10*k # sample/(sample/second) = seconds: time of taken measurements

def start_decawave():
    global k # the number of samples in tau and diviser in the running average
    global counter #
    global measurement_duration # sample/(sample/second) = seconds: time of taken measurements
    running_ave = 0.0

    ser = serial.Serial('/dev/serial/by-id/usb-SEGGER_J-Link_000760044549-if00', 115200, timeout=None, xonxoff=True)
    print(ser)
    print (ser.is_open)
    ser.write(b'\r\r')
    time.sleep(1)
    ser.write(b'lec\r')
    time.sleep(2)
    print(ser.isOpen)
    start = time.time()
    while(ser.is_open):
    
        result = ser.readline().split(b',')
        if result[0] == b'DIST':
            raw_data = (result[7].decode('utf-8'))
            if re.fullmatch('[A-Za-z]', raw_data):
                continue
            else:
                raw_data = float(raw_data)
                running_ave = running_ave - (1.0/k)*(running_ave-raw_data)
            #print("raw data : ",(raw_data))
            print("running average : ", running_ave)
        if start + 60 < time.time():
            ser.write(b'lec\r')
            time.sleep(1)
            ser.write(b'quit\r')
            time.sleep(1)       
            ser.close()
    print('end of session')
    return running_ave*0.9998 + 0.2419	#corrected running average using Linear Regression
    #return regression_correction(running_ave) # corrected running average using a 4th order regression

def regression_correction(data_to_correct):
    data = data_to_correct
    coef = [-2.0158E-9,-2.857E-7,9.4140E-5,0.9944,0.3114]
    N = len(coef)  
    corrected_data = 0
    for k  in range (N):
        corrected_data = corrected_data + coef[k]*math.pow(data,(N-1)-k)
    return corrected_data

