import math
import statistics
import pos_data
import decawave
import RoboComA
import motorControl
import PixyData
import UbloxData
import time
R = 6371000 #radius of the earth
motor_steps = 400 # steps per rotation

def angle_calc(rtk, base_deca_tag, rover_deca_tag):
    #              /\
    #             /  \
    #      base  /    \  rover
    #           /      \
    #          /________\
    #               rtk
    rtk_base_angle = sss_triangle_angle_calc(rover_deca_tag, base_deca_tag, rtk)
    rtk_rover_angle = sss_triangle_angle_calc(base_deca_tag, rover_deca_tag, rtk)
    base_rover_angel = sss_triangle_angle_calc(rtk, base_deca_tag, rover_deca_tag)
    return rtk_base_angle, rtk_rover_angle, base_rover_angel

def sss_triangle_angle_calc(a,b,c):
    a_squared = math.pow(a,2)
    b_squared = math.pow(b,2)
    c_squared = math.pow(c,2)
    argument = (b_squared + c_squared - a_squared)/(2*b*c)
    #print(argument)
    angle = math.degrees(math.acos(argument))
    return angle
def stats(distance_array):
    return statistics.mean(distance_array)

def gps_to_cartesian( latitude, longitude):
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)
    x = R*math.cos(latitude)*math.cos(longitude)
    y = R*math.cos(latitude)*math.sin(longitude)
    z = R*math.sin(latitude)
    return x, y, z

def cartesion_to_gps(x, y, z):
    latitude = math.degrees(math.asin(z/R))
    longitude = math.degrees(math.atan2(y,x))
    return latitude, longitude

def trilateration(rtk, rad1, rad2):
    # rad1 is the distance from the base station to the object of interest
    # rad1 should be place at (0,0) on the cartesion plane
    #rad2 is a similar measurement but it sould be placed on the x axis
    # based on the distance it is from the base station at (rtk,0) on the 
    #cartesion plane
    x =(math.pow(rad1,2) - math.pow(rad2,2) + math.pow(rtk,2))/(2*rtk)
    y_plus = math.sqrt(math.pow(rad1,2) - math.pow(x,2))
    y_minus = -math.sqrt(math.pow(rad1,2) - math.pow(x,2))
    return x, y_plus, y_minus

def angle_to_steps(angle_deg):
    return round(angle_deg*(motor_steps/360))
    
def rtk_calc(north, east):
    return math.sqrt(math.pow(north,2) + math.pow(east,2))
    
def is_triangle(a, b, c):
    if (a > b + c) or (b > a + c) or (c > a + b):
        print ("No")
    else:
        print ("Yes")
def pixy_angle_correction(camera_to_target_dist,blocks_offset,steps_moved_by_motor,focal_length):
    print("block_offset: "+ str(blocks_offset))
    #Number of blocks from the center of the target to the center of the image.
    blocksFromCenter = blocks_offset# need this values from the Camera after it has moved.
    #width of a block.
    blockWidth = 12E-6
    #Focal length of camera.
    focalLength = focal_length*.8
    print("focal length used: " + str(focalLength))
    #Actual distance from camera to target (meters).
    distance = camera_to_target_dist #need this distance from the Decawave
    #Calculation for actual distance from the direction the camera is pointing to the actual center of the target. 
    realWidth = ((blocksFromCenter*blockWidth)/(focalLength))*(distance)
    #Arclength formula. 
    angle = steps_moved_by_motor*0.9 #Degrees. this number will come from
    r = distance; #Meters
    #arcLength = (r*2*math.pi)*(angle/360)
    temp = angle_calc(abs(realWidth), distance, distance)


    #Angle error correction.
    #correctedArcLength = arcLength + realWidth
    #correctedAngle = (correctedArcLength*360)/(2*math.pi*r)
    print(temp[2])
    if realWidth < 0.0:
        correctedAngle = angle + temp[2]
    else:
        correctedAngle = angle - temp[2]
    print("real width is " + str(realWidth))
    print("corrected angle is " + str(correctedAngle))
    #print("arc length is " + str(arcLength))
    #print("new arc length is " + str(correctedArcLength))
    #print("target is " + str((correctedArcLength-arcLength)) + " centimeters from the direction of the camera")
    return correctedAngle

# to calculate the true distance from the center of the base/rover
# because the decawave is adhered to the side of the base/rover
def decawave_offset_correction(angle_deg,dist_to_target):
    offset = 42E-3 #the decawave is 42mm from the center of the base/rover module
    rad = math.radians(angle_deg) + math.pi/2 # adding 90 degrees to the angle 
    a_sqr = math.pow(dist_to_target,2)
    b_sqr = math.pow(offset,2)
    if rad > math.pi:
        rad = rad - math.pi
        corrected_dist = math.sqrt(a_sqr + b_sqr - 2*dist_to_target*offset*math.cos(rad)) 
    elif rad < math.pi:
        corrected_dist = math.sqrt(a_sqr + b_sqr - 2*dist_to_target*offset*math.cos(rad))
    else:
        corrected_dist = dist_to_target + offset
    
    return corrected_dist

def focal_length_calc(block_width, distance, num_blocks_wide, real_width):
    fl = (num_blocks_wide*block_width*distance)/real_width
    return fl

if __name__ == '__main__':
    #Base has camera
    motorControl.start_motor(0, direction = 'backward')
    base_laser = 18.039
    rover_laser = 17.501
    rtk_laser = 10.615

    base_dist = decawave.start_decawave() #robot_A
    rover_dist = float(RoboComA.main())
    #rtk = rtk_laser
    rtk = UbloxData.RTK_dist()
    print("base_dist: " + str(base_dist))
    print("rover_dist: " + str(rover_dist))
    print("rtk_dist: " + str(rtk))

    #Camera reference point for corrections
    camera_center = PixyData.center_camera()
    #camera_center = 135
    print("before cam_error: " + str(base_dist-base_laser))
    print("before roboB: " + str(rover_dist-rover_laser))
    angles_from_deca = angle_calc(rtk, base_dist, rover_dist)
    angles_from_laser = angle_calc(rtk_laser, base_laser, rover_laser)
    base_dist = decawave_offset_correction(angles_from_deca[0], base_dist)
    rover_dist = decawave_offset_correction(angles_from_deca[1], rover_dist)

    steps_for_motor = angle_to_steps(angles_from_deca[0])
    motorControl.start_motor(int(round(steps_for_motor)), direction='backward')
    print("angles from deca: " + str(angles_from_deca))
    print("angles from laser: " + str(angles_from_laser))
    print("Motor steps: " + str(steps_for_motor))
    pixy_x = PixyData.get_pixy_x()
    print("target x_pos:" + str(pixy_x))
    focal_length = focal_length_calc(block_width=12e-6,distance=10.615,num_blocks_wide=49,real_width=80e-3) 
    corrected_angle = pixy_angle_correction(base_dist,camera_center-pixy_x,steps_for_motor,focal_length)

    print("corrected angle: " + str(corrected_angle))
    print("rtk - laser (error): "+ str(rtk - rtk_laser))
    print("cam_distance - cam_laser: " + str(base_dist - base_laser))
    print("robotB_dist - robotB_laser: " + str(rover_dist - rover_laser))
    print("error margin: " + str(corrected_angle-angles_from_laser[0]))
    time.sleep(5)
    motorControl.reset_motor(steps_for_motor, 'backward')
