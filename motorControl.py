#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
Motor1 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
def start_motor(motor_steps, direction):
        try:
                global Motor1
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
                        time.sleep(2)
                        return
                else:
                    Motor1.SetMicroStep('hardward','fullstep')
                    Motor1.TurnStep(Dir=direction, steps=motor_steps, stepdelay = 0.005)
                    time.sleep(2)
                
                #reset_motor(motor_steps, direction)
        except:
                Motor1.Stop()
                #GPIO.cleanup()
                print("\nMotor_Control Error: start_motor")
                exit()
def reset_motor(steps, direction):
        """
        Resets the motor back to the base station by 
        negating (param) direction and starting the motor. 

        Args:
        steps (int): the number of steps the motor has gone.
        direction (string): the direction chosen for param steps.
        Returns:
        """
        try:
                _direction = negate_direction(direction)
                global Motor1 #= DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
                Motor1.TurnStep(Dir=_direction, steps=steps, stepdelay = 0.005)
        except:
                Motor1.Stop()
                #GPIO.cleanup()
                print("\nMotor_Control Error: reset_motor")
                exit()
def negate_direction(direction):
         """
        Simple helper function to reverse the direction of the stepper motor
        Args:
                direction (string): direction of the motor. 'forward' (counter-clockwise) or 'backward' (clockwise)
        Returns:
                _direction (string): negation of direction ('forward' or 'backward')
        
        """
        if direction == 'forward':
                _direction = 'backward'
        else:
                _direction = 'forward'
        return _direction
def stop_motor():
        """
                Cuts the power to the motor. effectivly turning it off.
                Args:
                Returns:
        """
    try:
        global Motor1
        Motor1.Stop()
        #GPIO.cleanup()
        print("motor shutdown.")
    except:
        Motor1.Stop()
        #GPIO.cleanup()
        print("\nMotor_Control Error: stop_motor")
        exit()