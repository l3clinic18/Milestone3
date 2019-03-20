import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

def start_motor(motor_steps):
    try:
        Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        #motor_steps = 400
        """
        # 1.8 degree: nema17
        # softward Control :
        # 'fullstep': A cycle = 200 steps
        # 'halfstep': A cycle = 200 * 2 steps
        # '1/4step': A cycle = 200 * 4 steps
        # '1/8step': A cycle = 200 * 8 steps
        # '1/16step': A cycle = 200 * 16 steps
        # '1/32step': A cycle = 200 * 32 steps
        """
        Motor1.SetMicroStep('hardward','fullstep')
        Motor1.TurnStep(Dir='backward', steps=motor_steps, stepdelay = 0.005)
        time.sleep(5)
        Motor1.TurnStep(Dir='forward', steps=motor_steps, stepdelay = 0.005)
        #time.sleep(20)
        #Motor1.Stop()
        GPIO.cleanup()
    except:
        GPIO.cleanup()
        print("\nMotor stop")
        Motor1.Stop()
        exit()
