#Position data in .txt format and output distant and/or x/y as a List.
import sys
import binascii
from struct import *
#Pixy position data.
#cam_data is a text file path. String.
#returns and averaged tuple of x, y float vlaues. 
def camera_pos_data(cam_data):
    temp_data = [0, 0]
    count = 0
    try:
        with open(cam_data, "r") as cam_file:
            #x and y are index 3 & 5 respectivly. 
            for line in cam_file:
                count += 1
                data_list = line.split(' ') 
                temp_data[0] += int(data_list[3])
                temp_data[1] += int(data_list[5])
        cam_file.closed
    except(OSError):
        print("Error in opening/reading file. " + str(OSError))
        return None
    #average over the number of x,y values
    camera_data = (temp_data[0]/count, temp_data[1]/count)
    print(str(camera_data[0]) + ' ' + str(camera_data[1]))
    return camera_data
#GPS RTK distance between base station and rover.
#gps_data, text file, HEX. Argument type: String
#Returns a list of reletive distance measurements in meters.
def GPS_pos_data(gps_data):
    ubx_data = []
    try:
        with open(gps_data, "rb") as gps_file:
            _data = gps_file.read()
            #                                           UBX packet structure                                            #
            # SyncChar1 | SyncChar2 |  Class   |   ID     |   Length   |             Payload              |  CHK_SUM |  #
            #  1 Byte   |  1 Byte   |  1 Byte  |  1 Byte  |   2 Byte   |     Variable 4 Byte increment    |  2 Byte  |  #
            for index in range(len(_data)-1): #reading the file two bytes at a time.
                if _data[index:(index+2)].hex() == 'b562': #check two bytes to verify UBX packet
                    payload_length = int.from_bytes(_data[(index+4):(index+6)], byteorder='little', signed=False)
                    if _data[(index+2):(index+4)].hex() == '013c': #Check the Class & ID
                        #TO_DO: check the packet for validity
                        ubx_data = UBX_packet_data(_data[(index+6):(index+46)])
                    #It is not a NAV_RELPOSNED packet. find the length and skip that + 2 bytes.
                    else:
                        index += payload_length + 2
                        continue
                elif (len(_data) - index) < 8:
                    pass
                index += 1
        gps_file.closed
    except(OSError):
        print("Error in opening/reading file. " + str(OSError))
        return None
    print(ubx_data)
    return ubx_data
#UWB distance data.
#umb_data, text file, ascii. Argument type: String.
#Returns a list of reletive distance measurements in meters. Otherwise returns None object    
def UWB_pos_data(uwb_data):
    _data = []
    try:
        with open(uwb_data, "rb") as uwb_file:
            for line in uwb_file:
                data_list = line.split(b',')
                if len(data_list) == 8 and (b'\n' in data_list[7]):
                    _data.append(float(data_list[7].strip(b'\n')))
    except(OSError):
        print("Error in opening/reading file. " + str(OSError))
        return None
    return _data

#The payload of the UBX packet to be decoded and useful information returned.
#return 2 element list with Reletive North and East.
def UBX_packet_data(payload):
    #print('Reletive north ' + str(int.from_bytes(payload[8:12], byteorder='little', signed=True))
    #        + ' Reletive east ' + str(int.from_bytes(payload[12:16], byteorder='little', signed=True))
    #        + ' Reletive depth ' + str(int.from_bytes(payload[16:20], byteorder='little', signed=True)))
    return [int.from_bytes(payload[8:12], byteorder='little', signed=True)/100, int.from_bytes(payload[12:16], byteorder='little', signed=True)/100]

def verify_packet(_data, chksum):
    A = 0
    B = 0
    calc_B = B.to_bytes(1, byteorder='little', signed=False)
    calc_A = A.to_bytes(1, byteorder='little', signed=False)
    print(calc_A[0])
    chksum_A = chksum[0:1]
    chksum_B = chksum[1:2]
    for x in range(len(_data)):
        calc_A = calc_A[0] + _data[x].to_bytes(1, byteorder='little', signed=False)
        calc_B = calc_B[0] + calc_A
    print('calculated = ' + str(calc_A) + ' and ' + str(calc_B))
    print('given = ' + str(int.from_bytes(chksum_A, byteorder='little')) + ' and ' + str(int.from_bytes(chksum_B, 
            byteorder='little')))
    return True

#end of file
#If the files are passed in at compile/execution time.
if __name__ == "__main__":
    #test
    camera_pos_data(sys.argv[1])