#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

def start_motor(motor_steps, direction):
        try:
                Motor1 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
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
                
                #rotate counterclockwise
                if motor_steps >= 220:
                        _direction = negate_direction(direction)
                        new_steps = (400-motor_steps)
                        start_motor(new_steps, _direction)
                        return
                else:
                    Motor1.SetMicroStep('hardward','fullstep')
                    Motor1.TurnStep(Dir=direction, steps=motor_steps, stepdelay = 0.005)
                    time.sleep(5)
                
                reset_motor(motor_steps, direction)
                
        except:
                Motor1.Stop()
                GPIO.cleanup()
                print("\nMotor_Control Error: start_motor")
                exit()
def reset_motor(steps, direction):
        try:
                _direction = negate_direction(direction)
                Motor1 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
                Motor1.TurnStep(Dir=_direction, steps=steps, stepdelay = 0.005)
        except:
                Motor1.Stop()
                GPIO.cleanup()
                print("\nMotor_Control Error: reset_motor")
                exit()
def negate_direction(direction):
        if direction == 'forward':
                _direction = 'backward'
        else:
                _direction = 'forward'
        return _direction
def stop_motor():
    try:
        Motor1 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        Motor1.Stop()
        GPIO.cleanup()
    except:
        Motor1.Stop()
        GPIO.cleanup()
        print("\nMotor_Control Error: stop_motor")
        exit()