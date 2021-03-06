
"""
Messages will be recieved, parsed and sent to sss_triangle.
                                           UBX packet structure                                            #
 SyncChar1 | SyncChar2 |  Class   |   ID     |   Length   |             Payload              |  CHK_SUM |  #
  1 Byte   |  1 Byte   |  1 Byte  |  1 Byte  |   2 Byte   |     Variable 4 Byte increment    |  2 Byte  |  #
"""
import serial
import serial.tools
import math
def _nav_data():
    """
    _nav_data: checks ever packet coming over the USB interface. Once the NAV-UBX_RELPOSNED 
    (Ublox_M8 protocol sheet. 13003221) grab reletive position north and east.
    """
    north_pos = 0.0
    east_pos = 0.0
    with serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00', 9600, timeout=None, xonxoff=True) as ser: #Used for rPI
    #with serial.Serial("/dev/cu.usbmodem14101", 9600, timeout=None, xonxoff=True) as ser: #macOS enviroment.
        print(ser.isOpen)
        while(ser.isOpen):
            ublox_data = ser.read(100)
            #print(ublox_data)
            ubx_index = ublox_data.find(b'\xb5b\x01<')
            if ubx_index >= 0:
                payload = ublox_data[ubx_index+6:ubx_index+46]
                print(payload.hex())
                #print(len(payload))
                if len(payload) != 40:
                    continue
                """
                Byte Offsets
                index + 8 = north position, index + 12 = east position, 
                index + 20 high presiscion north, index + 21 high presiscion east.
                """
                #iTOW
                print("iTow: " + str(int.from_bytes(payload[4:8], byteorder='little', signed=False)))
                ##TO-DO validate nav data
                print("northData: " + payload[8:12].hex())
                north_pos = (int.from_bytes(payload[8:12], byteorder= 'little', signed=True)
                 + (int.from_bytes(payload[20:21], byteorder= 'little', signed=True) * .01))
                print("eastData: "+ str(payload[12:16].hex()))
                east_pos  = (int.from_bytes(payload[12:16], byteorder= 'little', signed=True)
                 + (int.from_bytes(payload[21:22], byteorder= 'little', signed=True) * .01))
                print("north: " + str(north_pos))
                print("east: "+ str(east_pos))
                break
        ser.close()
    if (north_pos + east_pos) == 0.0:
        return None
    else:
        return (north_pos, east_pos)

def RTK_dist():
    """
    Args:
    Returns:
        dist (float): RTK distance from the Ublox GPS board.
    """
    ubx_data = _nav_data()
    if ubx_data:
        dist = math.sqrt(math.pow(ubx_data[0],2) + math.pow(ubx_data[1],2))
        return dist*.01
    else:
        return 0.0


