#pyUBX used to bootstrap UBX communication to the Pi
#Messages will be recieved, parsed and sent to sss_triangle.
import serial
import serial.tools
import re
with serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=None, xonxoff=True) as ser:
    print(ser.isOpen)
    while(ser.isOpen):
        foo = ser.read()
        print(foo) #testing
    ser.close()
       



