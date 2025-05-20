# Team3_Rover.py
"""
Module: Team3_Rover
Provides unified interfaces for:
 - Servo pan/tilt control
 - Face detection and frame capture
 - Distance measurement using LiDAR
 - Motor control (drive and speed)
 - Snapshot capture using Picamera2
"""
import cv2
from picamera2 import Picamera2
import time
import RPi.GPIO as GPIO
import serial
from adafruit_servokit import ServoKit

# --- Camera Setup ---
DISP_W, DISP_H = 640, 360
piCam = Picamera2()
piCam.preview_configuration.main.size = (DISP_W, DISP_H)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.controls.FrameRate = 30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# Haar cascade for face detection (original path)
faceCascade = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

# --- Motor & Servo Setup ---
NSLEEP1, NSLEEP2 = 12, 13
RL11, RL12 = 17, 27
RR11, RR12 = 22, 23
FL11, FL12 = 24, 25
FR11, FR12 = 26, 16
GPIO.setmode(GPIO.BCM)
for pin in (NSLEEP1, NSLEEP2, RL11, RL12, RR11, RR12, FL11, FL12, FR11, FR12):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pwm1 = GPIO.PWM(NSLEEP1, 1000)
pwm2 = GPIO.PWM(NSLEEP2, 1000)
pwm1.start(50)
pwm2.start(50)

kit = ServoKit(channels=16)
ser = serial.Serial('/dev/serial0', 115200, timeout=0)

# --- Functions Section ---
def set_pan_tilt(pan_angle, tilt_angle):
    """
    Rotate pan (channel 0) and tilt (channel 1) servos.
    """
    kit.servo[0].angle = pan_angle
    kit.servo[1].angle = tilt_angle
    time.sleep(0.005)


def capture_frame_and_faces():
    """
    Capture one frame and detect faces.
    Returns frame (BGR) and list of face rectangles.
    """
    frame = piCam.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    return frame, faces


def take_snapshot():
    """
    Take a still image with the existing Picamera2 instance.
    Uses capture_file as per professor's example.
    """
    try:
        piCam.capture_file("test_image.jpg")  # saves a picture to current directory
        print("Took a picture!")
    except Exception as e:
        print(f"An error occurred: {e}")


def MeasureDistance():
    """
    Read a distance value from the LiDAR sensor.
    Returns integer distance in cm.
    """
    while True:
        if ser.in_waiting >= 9:
            data = ser.read(9)
            ser.reset_input_buffer()
            if data[0] == 0x59 and data[1] == 0x59:
                return data[2] + data[3] * 256


def Motor(v1, v2, v3, v4, v5, v6, v7, v8):
    """
    Set GPIO outputs to control motor directions.
    """
    GPIO.output(RL11, v1); GPIO.output(RL12, v2)
    GPIO.output(RR11, v3); GPIO.output(RR12, v4)
    GPIO.output(FL11, v5); GPIO.output(FL12, v6)
    GPIO.output(FR11, v7); GPIO.output(FR12, v8)


def Speed(left, right):
    """
    Set PWM duty cycle for left/right motor enables.
    """
    pwm1.ChangeDutyCycle(left)
    pwm2.ChangeDutyCycle(right)
