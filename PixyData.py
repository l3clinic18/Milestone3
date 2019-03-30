#Pixy (x,y) Data
#Author Trevor Overby, CMUlabs @John Leimon
from pixy import *
from ctypes import *
import statistics
import motorControl
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
def sample_blocks(sample_size):
    blocks = BlockArray(100)
    frame  = 0
    global blocks_x_pos
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
                if(len(blocks_x_pos) < 200):
                    blocks_x_pos.append(blocks[index].x)
                else:
                    get_pixy_x()
        
        
#find the mean, variance and std deviation of the sample
def get_pixy_x():
    global blocks_x_pos
    m = statistics.mean(blocks_x_pos)
    stdev = statistics.stdev(blocks_x_pos)
    var = statistics.variance(blocks_x_pos, m)
    if 130 < m < 160:
        return m
    else:
        #move motor
        motorControl.start_motor(5)
        #call sample blocks
        sample_blocks(200)