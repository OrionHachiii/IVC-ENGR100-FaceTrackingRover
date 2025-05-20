# Team3_Final_FaceTracking_Rover.py
"""
Final face-tracking script with:
1) Initial 5?way scan (Center?Left?Right?Up?Down), holding SCAN_PAUSE seconds each.
2) On first face detection, take one snapshot.
3) Continuous tracking loop with inner for?loop over the first face:
   a) Center servos on the face.
   b) Measure distance.
   c) If distance < DIST_THRESHOLD ? BACKWARD.
      Elif distance > DIST_THRESHOLD ? FORWARD.
      Else (within band) ? if pan_angle > CENTER_ANGLE+ANGLE_TOLERANCE ? TURN RIGHT,
                          elif pan_angle < CENTER_ANGLE-ANGLE_TOLERANCE ? TURN LEFT,
                          else ? FORWARD.
   After each Motor() call, call Speed(BASE_SPEED, BASE_SPEED).
4) Ctrl+C for clean shutdown.
"""

import time
import cv2
import RPi.GPIO as GPIO
import Team3_Rover


# --- Configuration Parameters ---
DIST_THRESHOLD  = 20     # cm to maintain
BASE_SPEED      = 60     # PWM duty cycle for all motions
SERVO_SCALE     = 30     # divisor for pixel?servo adjustment
LOOP_DELAY      = 0.02   # seconds between control loops
SCAN_PAUSE      = 2.0    # seconds to hold at each scan position
CENTER_ANGLE    = 90     # servo center
ANGLE_TOLERANCE = 15      # degrees tolerance around center

# --- Initialization ---
pan_angle, tilt_angle = CENTER_ANGLE, CENTER_ANGLE
Team3_Rover.set_pan_tilt(pan_angle, tilt_angle)
Team3_Rover.Motor(0,0,0,0,0,0,0,0)  # start stationary
cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)

# --- 1) Initial 5?Way Scan ---
scan_positions = [
    (90,  90),   # center
    (30,  90),   # left
    (150, 90),   # right
    (90,  45),   # up
    (90,  150)   # down
]

face_found = False
while not face_found:
    for pan, tilt in scan_positions:
        Team3_Rover.set_pan_tilt(pan, tilt)
        frame, faces = Team3_Rover.capture_frame_and_faces()
        cv2.imshow("Camera", frame)
        cv2.waitKey(1)
        time.sleep(SCAN_PAUSE)
        if len(faces) > 0:
            face_found = True
            break

# --- 2) Take one snapshot ---
Team3_Rover.take_snapshot()

# --- 3) Continuous Tracking Loop ---
try:
    while True:
        frame, faces = Team3_Rover.capture_frame_and_faces()

        # 3a) No face ? STOP
        if len(faces) == 0:
            Team3_Rover.Motor(0,0,0,0,0,0,0,0)
            Team3_Rover.Speed(BASE_SPEED, BASE_SPEED)
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)
            time.sleep(LOOP_DELAY)
            continue

        # 3b) Process only the first detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 3)

            # Compute pixel errors
            pan_error  = (x + w/2) - (Team3_Rover.DISP_W  / 2)
            tilt_error = (y + h/2) - (Team3_Rover.DISP_H  / 2)

            # Center the face with servos
            pan_angle  = max(45, min(150, pan_angle  - pan_error  / SERVO_SCALE))
            tilt_angle = max(45, min(150, tilt_angle - tilt_error / SERVO_SCALE))
            Team3_Rover.set_pan_tilt(pan_angle, tilt_angle)

            # Measure forward distance
            dist = Team3_Rover.MeasureDistance()

            # 3c) Decision & Actuation
            if dist < DIST_THRESHOLD:
                # Too close ? BACKWARD
                Team3_Rover.Motor(1,0,1,0,1,0,1,0)
            elif dist > DIST_THRESHOLD:
                # Face moved away ? FORWARD
                Team3_Rover.Motor(0,1,0,1,0,1,0,1)
            else:
                # Within threshold ? steer by pan_angle
                if pan_angle > CENTER_ANGLE + ANGLE_TOLERANCE:
                    # servo pointed right ? TURN RIGHT
                    Team3_Rover.Motor(1,0,0,1,1,0,0,1)
                elif pan_angle < CENTER_ANGLE - ANGLE_TOLERANCE:
                    # servo pointed left ? TURN LEFT
                    Team3_Rover.Motor(0,1,1,0,0,1,1,0)
                else:
                    # servo centered ? FORWARD
                    Team3_Rover.Motor(0,1,0,1,0,1,0,1)

            # Apply uniform speed
            Team3_Rover.Speed(BASE_SPEED, BASE_SPEED)
            break  # only handle the first face

        # Display and loop delay
        cv2.imshow("Camera", frame)
        cv2.waitKey(1)
        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    # --- Shutdown and Cleanup ---
    Team3_Rover.Motor(0,0,0,0,0,0,0,0)
    GPIO.cleanup()
    cv2.destroyAllWindows()
    Team3_Rover.piCam.stop()
    Team3_Rover.piCam.close()
    Team3_Rover.ser.close()
    print("Program ended.")