import serial
import time
k = 2.0
ser = serial.Serial('/dev/serial/by-id/usb-SEGGER_J-Link_000760044549-if00', 115200, timeout=None, xonxoff=True)
print(ser)
print (ser.is_open)
ser.write(b'\r\r')
time.sleep(1)
ser.write(b'lec\r')
time.sleep(2)
print(ser.isOpen)
start = time.time()
running_ave = 0.0

def get_runavg():
	return running_ave
	

while(ser.is_open):

	
	result = ser.readline().split(b',')
	if result[0] == b'DIST':
		temp = float(result[7].decode('utf-8'))
		if running_ave > 0.0:
			running_ave = running_ave - (1.0/k)*(running_ave-temp)
		else:
			running_ave = (1.0/k)*temp
		print("temp : ",(temp))
		print("running : ", running_ave)
		print("addr : " ,id(running_ave))
	if start + 10 < time.time():
		ser.write(b'lec\r')
		time.sleep(1)
		ser.write(b'quit\r')
		time.sleep(1)		
		ser.close()


print('end of session')	
	
