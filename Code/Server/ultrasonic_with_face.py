import asyncio
import RPi.GPIO as GPIO
import time
from Motor import *
from servo import *
from Ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()

async def start_ultrasonic():
    
    print ('Ultrasonic is starting...')
    servo=Servo()
    servo.setServoPwm('0',90)
    servo.setServoPwm('1',140)
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0)
        servo.setServoPwm('0',90)
        servo.setServoPwm('1',140)
        print ("\nEnd of program")


async def main():
    task_ultrasonic = asyncio.create_task(start_ultrasonic())
    await task_ultrasonic

asyncio.run(main())
