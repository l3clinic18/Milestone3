#pyUBX used to bootstrap UBX communication to the Pi
#Messages will be recieved, parsed and sent to sss_triangle.
#                                           UBX packet structure                                            #
# SyncChar1 | SyncChar2 |  Class   |   ID     |   Length   |             Payload              |  CHK_SUM |  #
#  1 Byte   |  1 Byte   |  1 Byte  |  1 Byte  |   2 Byte   |     Variable 4 Byte increment    |  2 Byte  |  #
import serial
import serial.tools
import math

def _nav_data():
    north_pos = 0.0
    east_pos = 0.0
    with serial.Serial('/dev/ttyACM0', 9600, timeout=None, xonxoff=True) as ser: #Used for rPI
    #with serial.Serial("/dev/cu.usbmodem14101", 9600, timeout=None, xonxoff=True) as ser: #macOS enviroment.
        print(ser.isOpen)
        while(ser.isOpen):
            ublox_data = str(ser.readline().hex())
            ubx_index = ublox_data.find('b562013c')
            if ubx_index > 0:
                ubx_nav_data = ublox_data[ubx_index:ubx_index+48]
                #Byte Offsets
                #index + 8 = north position, index + 12 = east position, 
                #index + 20 high presiscion north, index + 21 high presiscion east.
                ##TO-DO validate nav data
                north_pos = (int.from_bytes(bytes.fromhex(ubx_nav_data[ubx_index+8:ubx_index+12]), byteorder= 'little', signed=False)
                 + int.from_bytes(bytes.fromhex(ubx_nav_data[ubx_index+20:ubx_index+21]), byteorder= 'little', signed=False) * .001)
                
                east_pos  = (int.from_bytes(bytes.fromhex(ubx_nav_data[ubx_index+12:ubx_index+16]), byteorder= 'little', signed= False)
                 + int.from_bytes(bytes.fromhex(ubx_nav_data[ubx_index+21:ubx_index+22]), byteorder= 'little', signed= False) * .001)
                break
            #print(str(foo.hex()))
            #print(str(foo.hex()).find('b562013c'))
            #foo2 = str(foo.hex())[80:128]
            #print("foo2: " + foo2)
        ser.close()
    if (north_pos + east_pos) == 0.0:
        return None
    else:
        return (north_pos, east_pos)
       
#def RTK_dist():
#triangle math
ubx_data = _nav_data()
if ubx_data:
    dist = math.sqrt(math.pow(ubx_data[0],2) + math.pow(ubx_data[1],2))
    #return dist
else:
    foo=None
    #return None
print("derp")


