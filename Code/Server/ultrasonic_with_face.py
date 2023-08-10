import argparse
import asyncio
import RPi.GPIO as GPIO
import time
import cv2 as cv
import dlib
from picamera2 import Picamera2
from pygame import mixer as audio_mixer

from Motor import *
from servo import *
from Ultrasonic import Ultrasonic

# Initialize ultrasonic module
ultrasonic = Ultrasonic()
# define a video capture object
cam = Picamera2()

async def start_ultrasonic():
    
    print ('Ultrasonic is starting...')
    servo=Servo()
    servo.setServoPwm('0',90)
    servo.setServoPwm('1',140)
    try:
        await asyncio.to_thread(ultrasonic.run)
        #ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0)
        servo.setServoPwm('0',90)
        servo.setServoPwm('1',140)
        print ("\nEnd of program")


async def start_camera(flip = True, res=(640,480), audio_out=None):

    # Configure the camera
    config = cam.create_preview_configuration(main={"size": res, "format": "BGR888"})
    cam.configure(config)
    cam.start()
    print ('Camera is running')
    # dlib face detector
    face_detector = dlib.get_frontal_face_detector()

    while(True):
        try:
            t1 = time.time()
            # Read the frame
            frame = cam.capture_array()
            # Frame conversion to gray
            img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Flip
            if flip:
                img_gray = cv.rotate(img_gray, cv.ROTATE_180)
            # Face detection
            rects = face_detector(img_gray, 0)

            if len(rects) != 0:
                print (f'Face detected: {len(rects)}')
                # if audio_out is not None:
                #     # If audio is enabled
                #     if not audio_out.music.get_busy():
                #         # If the audio is not playing then play the audio
                #         audio_out.music.play()
        
            t2 = time.time()
            print (f'frame_time: {t2-t1}')

        except Exception as e:
            print (e)
            # On error, release the camera object
            cam.stop()
            break


async def main():
    task_ultrasonic = asyncio.create_task(start_ultrasonic())
    task_camera = asyncio.create_task(start_camera())
    await task_ultrasonic
    await task_camera

asyncio.run(main())
