import serial
import time
k = 2.0 # the number of samples in tau and diviser in the running average
sample_rate = 10 #sample/second this is the sample rate of the decawave
measurement_duration = k/sample_rate # sample/(sample/second) = seconds: time of taken measurements

running_ave = 0.0

def get_runavg():
	return running_ave
	
def start_decawave():
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
			temp = float(result[7].decode('utf-8'))
			if running_ave > 0.0:
				running_ave = running_ave - (1.0/k)*(running_ave-temp)
			else:
				running_ave = (1.0/k)*temp
			print("raw data : ",(temp))
			print("running average : ", running_ave)
		if start + measurement_duration < time.time():
			ser.write(b'lec\r')
			time.sleep(1)
			ser.write(b'quit\r')
			time.sleep(1)		
			ser.close()


	print('end of session')	
	
