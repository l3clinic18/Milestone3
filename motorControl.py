import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

steps = 0
degrees = 0.0
step_degree = .9
def start_motor(motor_steps, direction):
        try:
                Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
                """
                # .9 degree: nema17
                # softward Control :
                # 'fullstep': A cycle = 400 steps
                # 'halfstep': A cycle = 400 * 2 steps
                # '1/4step': A cycle = 400 * 4 steps
                # '1/8step': A cycle = 400 * 8 steps
                # '1/16step': A cycle = 400 * 16 steps
                # '1/32step': A cycle = 400 * 32 steps
                """
                global step_degree
                degrees = motor_steps * step_degree

                Motor1.SetMicroStep('hardward','fullstep')
                Motor1.TurnStep(Dir=direction, steps=motor_steps, stepdelay = 0.005)
                time.sleep(5)
                #rotate counterclockwise
                if degrees >= 200:
                        _direction = negate_direction(direction)
                        new_steps = int((360-degrees)/step_degree)
                        start_motor(new_steps, _direction)
                        return
                reset_motor(motor_steps, direction)                
        except:
                Motor1.Stop()
                GPIO.cleanup()
                print("\nMotor_Control Error")
                exit()
def reset_motor(steps, _direction):
        try:
                Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
                Motor1.TurnStep(Dir=_direction, steps=steps, stepdelay = 0.005)
                #time.sleep(20)
                #Motor1.Stop
        except:
                Motor1.Stop()
                GPIO.cleanup()
                print("\nMotor_Control Error")
                exit()
def negate_direction(direction):
        if direction == 'forward':
                _direction = 'backward'
        else:
                _direction = 'forward'
        return _direction