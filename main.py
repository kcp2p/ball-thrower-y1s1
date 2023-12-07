import gamepad
from cyberpi import *
import time
import math
import random

#
#   Usage
#
# Ly - Left motor Forward, backward
# Ry - Right motor Forward, backward
# L1 - Gripper close
# L2 - Gripper open
# R1 - Gripper handler up
# R2 - Gripper handler down
# N1 - Launch and retract back
# N2 - Gripper handler middle
# N3 - Retrack back (failsafe)


#
#   Parameters configuration
#
flip = False # invert or not
THROW_SPEED = 200 # 0 - 200 range of speed
THROW_TIME = 500 # in ms
RETRACT_SPEED = 150 # 0 - 200 range of speed
RETRACT_TIME = 100 # in ms


#
#   Port declaration
#
# s1 - Handler servo
# s3 - Small servo 1 (Left grip)
# s4 - Small servo 2 (Right grip)
# em1 - Left encoder motor
# em2 - Right encoder motor
# m1, m2 - Throw motor

# Defines
HANDLER_SERVO = 's1'
LEFT_GRIP = 's3'
RIGHT_GRIP = 's4'


#
#   RGB Pulse function
#
def rgb_pulse(rgb_count):
    led.set_bri(math.sin(rgb_count / 4) * 50 + 52) 
    # Use the trigonometric function of the math library to enable the lightness of the LEDs to change periodically.
    led.move(1) 
    # Use the LED scrolling function of the cyberpi library to enable the colors of the LEDs to scroll.
    rgb_count += 1
    time.sleep(50/1000)
    return (rgb_count)


#
#   Initialization function
#
def init():
    # Initialization
    led.show("r g b y c")
    mbot2.servo_set(180, HANDLER_SERVO) # Default position, gripper handler should be up
    mbot2.servo_set(90, LEFT_GRIP) # Default position, should be forward
    mbot2.servo_set(90, RIGHT_GRIP) # Default position, should be forward


#
#   Main function, mother of all kind
#
def main():
    init() # Initialize the position
    rgb_count = 0
    while True:
        # RGB is love, RGB is life.
        rgb_count = rgb_pulse(rgb_count)

        # Press L1 and gripper should be closed.
        if (gamepad.is_key_pressed('L1')):
            mbot2.servo_set(120, LEFT_GRIP)
            mbot2.servo_set(60, RIGHT_GRIP)

        # Press L2 and gripper should be opened.
        if (gamepad.is_key_pressed('L2')):
            mbot2.servo_set(60, LEFT_GRIP)
            mbot2.servo_set(120, RIGHT_GRIP)

        # Press R1 and gripper handler should be up.
        if (gamepad.is_key_pressed('R1')):
            mbot2.servo_set(180, HANDLER_SERVO)

        # Press R2 and gripper handler should be down.
        if (gamepad.is_key_pressed('R2')):
            mbot2.servo_set(0, HANDLER_SERVO)

        # Press N2 and gripper handler should be in the middle.
        if (gamepad.is_key_pressed('N2')):
            mbot2.servo_set(55, HANDLER_SERVO)

        # Press N1 and it should throw.
        if (gamepad.is_key_pressed('N1')):
            # This part will throw.
            if (flip):
                mbot2.motor_set(-THROW_SPEED, 'm1')
                mbot2.motor_set(THROW_SPEED, 'm2')
            else:
                mbot2.motor_set(THROW_SPEED, 'm1')
                mbot2.motor_set(-THROW_SPEED, 'm2')
            time.sleep(THROW_TIME / 1000)

            # This part will retract.
            if (flip):
                mbot2.motor_set(RETRACT_SPEED, 'm1')
                mbot2.motor_set(-RETRACT_SPEED, 'm2')
            else:
                mbot2.motor_set(-RETRACT_SPEED, 'm1')
                mbot2.motor_set(RETRACT_SPEED, 'm2')    
            time.sleep(RETRACT_TIME / 1000)

            # Turn both motors off, rest in peace.
            mbot2.motor_set(0, 'm1')
            mbot2.motor_set(0, 'm2')
            
            # Halt for 100 ms before moving on
            time.sleep(0.1)
            

        # Press N3 and it should retract.
        if (gamepad.is_key_pressed('N3')):
            if (flip):
                mbot2.motor_set(RETRACT_SPEED, 'm1')
                mbot2.motor_set(-RETRACT_SPEED, 'm2')
            else:
                mbot2.motor_set(-RETRACT_SPEED, 'm1')
                mbot2.motor_set(RETRACT_SPEED, 'm2')
            time.sleep(RETRACT_TIME / 1000)

            # Turn both motors off, rest in peace.
            mbot2.motor_set(0, 'm1')
            mbot2.motor_set(0, 'm2')

            # Halt for 100 ms before moving on
            time.sleep(0.1)

        # Encoder Motor driver, obtain as x, y
        # Joystick range: -100 to 100, EM speed accepts -200 to 200.
        left_speed = int(gamepad.get_joystick('Ly') * 2)
        right_speed = int(gamepad.get_joystick('Ry') * 2)

        if (left_speed != 0 or right_speed != 0): # Joystick drift will ruin this code, I love my life.
            mbot2.drive_speed(left_speed, -right_speed)
        else:
            mbot2.EM_stop('all')

        # Debug
        console.println('L1: %d L2: %d R1: %d R2: %d x: %d y: %d N1: %d N3: %d' % (gamepad.is_key_pressed('L1'), gamepad.is_key_pressed('L2'), gamepad.is_key_pressed('R1'), gamepad.is_key_pressed('R2'), left_speed, right_speed, gamepad.is_key_pressed('N1'), gamepad.is_key_pressed('N3')))


main()
