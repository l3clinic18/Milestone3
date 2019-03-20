import math
import statistics
import pos_data
import decawave
import RoboComA
import motorControl
R = 6371000 #radius of the earth
motor_steps = 200 # steps per rotation


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
    return angle_deg*(motor_steps/360)
    
def rtk_calc(north, east):
    return math.sqrt(math.pow(north,2) + math.pow(east,2))
    
def is_triangle(a, b, c):
    if (a > b + c) or (b > a + c) or (c > a + b):
        print ("No")
    else:
        print ("Yes")

if __name__ == '__main__':

    base_laser = 2.388
    rover_laser = 2.626
    rtk = 1.886
    base_dist = decawave.start_decawave() #robot_A
    print("base_dist: " + str(base_dist))
    #roboComB.main(12333, 192.168.1.10, base_dist)
    rover_dist = float(RoboComA.main())
    print(str(rover_dist))


    angles_from_deca = angle_calc(rtk, base_dist, rover_dist)
    angles_from_laser = angle_calc(rtk, base_laser, rover_laser)

    steps_for_motor = angle_to_steps(angles_from_deca[0])
    motorControl.start_motor(int(steps_for_motor))
    print("angles from deca: " + str(angles_from_deca))
    print("angles from laser: " + str(angles_from_laser))
    print("Motor steps: " + str(steps_for_motor))


    #while True:
       # try:
           # base_dist_measure = pos_data.UWB_pos_data(base_dist_file)
           # rover_dist_measure = pos_data.UWB_pos_data(rover_dist_file)
            #base_dist_mean = stats(base_dist_measure[-10:])
            #rover_dist_mean = stats(rover_dist_measure[-10:])
            #angles_from_deca = angle_calc(base_dist_mean, rover_dist_mean, rtk)
            #angles_from_laser = angle_calc(base_laser, rover_laser, rtk)

            #print("angles from deca: " + str(angles_from_deca))
            #print("angles from laser: " + str(angles_from_laser))
            
            #print("in the loop")
        #except KeyboardInterrupt:
            #break

  #  print("successful")
   


