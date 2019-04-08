#Pixy (x,y) Data
#Author Trevor Overby, CMUlabs @John Leimon
import sys
sys.path.insert(0, './pixy/build/libpixyusb_swig')
from pixy import *
from ctypes import *
import statistics
import motorControl
import math
import time
# Initialize Pixy Interpreter thread #
pixy_init()
class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]
blocks_x_pos = []
x_center = 160
_sample_size = 20
#TO-DO: 
#Get sample information.
#Is it in the center of the field of view: Yes, No? 150 +- 20
#Yes:
#   return best/average 'x' value.
#No:
#   if mean x outside of 150 +- 20. Turn cam +-5 steps.
#   run sample function again. Repeat.
#   rerun a max of 3 or 5 times.
#
#Function to get the sample
#Function to calc variance, mean & std deviation
def sample_blocks():
    global blocks_x_pos
    global _sample_size
    global _sample_size
    blocks_x_pos = []
    blocks = BlockArray(100)
    frame  = 0
    # Wait for blocks #
    while True:
        count = pixy_get_blocks(100, blocks)
        if count > 0:
            # Blocks found #
            print('frame %3d:' % (frame))
            frame = frame + 1
            for index in range (0, count):
                print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % 
                (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height))
                #Add x values to a list SAMPLE_SIZE = 200
                if(len(blocks_x_pos) < _sample_size):
                    blocks_x_pos.append(blocks[index].x)
                else:
                    break
                    
        
#find the mean, variance and std deviation of the sample
def get_pixy_x():
    global blocks_x_pos
    global _sample_size
    if len(blocks_x_pos) < _sample_size:
        sample_blocks()
        mean = statistics.mean(blocks_x_pos)
    else:
        mean = statistics.mean(blocks_x_pos)
    print("mean x_pos:" + str(mean))
    return mean

def center_camera():
    global blocks_x_pos
    global _sample_size
    if len(blocks_x_pos) < _sample_size:
        sample_blocks()
    else:
        mean = statistics.mean(blocks_x_pos)
    print("mean x_pos: " + str(mean))
    if mean > 175:
        #clockwise
        motorControl.start_motor(1, direction='backward')
        time.sleep(2)
        sample_blocks()
    elif mean < 145:
        #counter-clockwise
        motorControl.start_motor(1, direction='forward')
        time.sleep(2)
        sample_blocks()
    return mean