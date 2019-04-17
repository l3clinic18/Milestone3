"""
Pixy (x,y) Signature Data
Author Trevor Overby, CMUlabs @John Leimon
"""
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
_sample_size = 1000

def sample_blocks():
    """
    Samples signature 1 or signature 2 and stores them in a global list 
    Globals:
        blocks_x_pos (List): stores the signatures' block x_position.
        _sample_size  (int): the amount of samples to take.   
    Returns:
    """
    global blocks_x_pos
    global _sample_size
    blocks_x_pos = []
    blocks = BlockArray(100)
    frame  = 0
    # Wait for blocks #
    while True:
        count = pixy_get_blocks(100, blocks)
        if count > 0:
            # Blocks found #
            #print('frame %3d:' % (frame))
            frame = frame + 1
            for index in range (0, count):
                print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % 
                (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height))
                #Add x values to a list SAMPLE_SIZE = 200
                if len(blocks_x_pos) < _sample_size and blocks[index].signature == 1:
                    blocks_x_pos.append(blocks[index].x)
                elif len(blocks_x_pos) < _sample_size and blocks[index].signature == 2:
                    blocks_x_pos.append(blocks[index].x)
                else:
                    return
                    
        
#find the mean, variance and std deviation of the sample
def get_pixy_x():
    """
        Args:
        Returns:
            float: average of the 1000 signatures recorded from sample_blocks()
    """
    global blocks_x_pos
    global _sample_size
    sample_blocks()
    mean = statistics.mean(blocks_x_pos)
    print("mean in get_pixy_x: "+str(mean))
    return mean

def center_camera():
    """
        Centers the camera within a range to set the center value used in module sss_triangle_calculation.py
        Args:
        Returns:
            float: average of the target x-value.
    """
    global blocks_x_pos
    global _sample_size
    if len(blocks_x_pos) < _sample_size:
        sample_blocks()
        mean = statistics.mean(blocks_x_pos)
    else:
        mean = statistics.mean(blocks_x_pos)
    print("mean x_pos: " + str(mean))
    while mean > 200 or mean < 25:
        print("mean x_pos: " + str(mean))
        mean = statistics.mean(blocks_x_pos)
        if mean > 200:
            #clockwise
            motorControl.start_motor(1, direction='backward')
            time.sleep(2)
            sample_blocks()
        elif mean < 100:
            #counter-clockwise
            motorControl.start_motor(1, direction='forward')
            time.sleep(2)
            sample_blocks()
    return mean
