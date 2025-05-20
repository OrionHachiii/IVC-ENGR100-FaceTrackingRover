# IVC-ENGR100-FaceTrackingRover

## IVC ENGR 100 Final Project



**Under the guidance of Professor Zahra Noroozi**  

_Assembled by Cole M., Zaid A., Zesen L., and Davoud Ghassemiyeh_



---



## Table of Contents



1. [Introduction & Purpose](#introduction--purpose)  

2. [Team Members & Professor](#team-members--professor)  

3. [Hardware & Components](#hardware--components)  

4. [Mechanical Design (SolidWorks)](#mechanical-design-solidworks)  

5. [Key Features](#key-features)  

6. [Control Flow & Flowchart](#control-flow--flowchart)  

7. [Sample Code Structure](#sample-code-structure)  

8. [Challenges & Solutions](#challenges--solutions)  

9. [Conclusion & Future Work](#conclusion--future-work)  



---



## Introduction & Purpose



Our four-wheel rover is designed to **detect and follow human faces**—“threats” in a security scenario—**while maintaining a safe distance**. It uses:



- A **TF-Luna** LiDAR sensor for obstacle/distance detection  

- A **Pan/Tilt** assembly for camera and sensor aiming  

- **OpenCV face detection** for visual tracking  



This project demonstrates how to integrate hardware, mechanical design, and control software into a cohesive, autonomous system.



---



## Team Members & Professor



- **Professor Zahra Noroozi** —IDEA Department Chair, Integrated Design, Automation & Engineering  

- **Cole M.** —Mechanical design & challenges  

- **Zaid A.** —Component selection & integration  

- **Zesen L.** —Flowchart & code implementation  

- **Davoud G.** —SolidWorks bracket design & key features  



---



## Hardware & Components



- **4WD Mecanum Wheel Chassis** (omnidirectional wheels)  

- **TF-Luna LiDAR** for distance measurement  

- **Raspberry Pi + 4WD H-Bridge Hat** to drive four motors  

- **Raspberry Pi Camera (Module v2)** for real-time video  

- **Two Hobby Servos** (pan & tilt) mounted via custom 3D-printed brackets  

- **Custom Pan/Tilt Brackets** designed in SolidWorks  



---



## Mechanical Design (SolidWorks)



- **Pan Bracket** holds camera and LiDAR on a horizontal pivot (180° sweep).  

- **Tilt Bracket** pitches that assembly up/down (~45°).  

- Iterative prints ensured **rigid support** and **minimal wobble** under motion.  

- Final design positions all electronics securely, preserving wiring clearance.



---



## Key Features



1. **Face & Eye Recognition** via OpenCV’s Haar cascades  

2. **Pan/Tilt Mobility**  

   - **Pan**: 45°–150° (≈180° total sweep)  

   - **Tilt**: 45°–150° (≈90° vertical range)  

3. **LiDAR-Based Distance Keeping**  

   - Maintains ~30 cm following distance  

4. **“Puppy-Like” Behavior**  

   - Scans surroundings before locking on  

   - Stops when face is lost  

   - Backs up if too close, moves forward if too far  

   - Turns in place when face drifts left/right  



---



## Control Flow & Flowchart



1. **Startup Scan** (for pan/tilt positions: Center → Left → Right → Up → Down)  

2. **First Face Detected** → take one snapshot  

3. **Continuous Loop**:  

   - Capture frame + detect faces  

   - If **no face**, stop  

   - Else, for the **first** face:  

     - Center servos on face (`pan_error` & `tilt_error`)  

     - Measure LiDAR distance  

     - **Decision**:  

       - **Too close** → backward  

       - **Too far**  → forward  

       - **Just right** → if camera angle > center+tol → turn right  

                         if angle < center−tol → turn left  

                         else → forward  

4. **Cleanup on Ctrl+C**  



A full flowchart diagram is provided in `docs/flowchart.png`.



---



## Sample Code Structure



- **`Team3_Rover.py`**: low-level hardware API  

  - Servo control (`set_pan_tilt`)  

  - Motor direction (`Motor`) + PWM (`Speed`)  

  - Camera capture + face detection (`capture_frame_and_faces`)  

  - LiDAR read (`MeasureDistance`)  

  - Snapshot (`take_snapshot`)  

- **`Team3_Final_FaceTracking_Rover.py`**: top-level script  

  - Imports **only** `Team3_Rover`  

  - Implements the scan, snapshot, and continuous loop logic  



See inline comments in each file for detailed explanations.



---



## Challenges & Solutions

| Challenge                                                         | Solution                                                                      |
|-------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Weak/custom-printed bracket parts                                 | Iterated SolidWorks design; added stiffening ribs                             |
| Face detection jitter & servo twitching                           | Introduced a **5° dead-band** around center; clamped servo angles            |
| LiDAR serial packet alignment                                     | Poll for complete 9-byte frames before parsing                                |
| Differential PWM steering proved jerky on 4WD chassis             | Switched to **discrete Motor patterns** (forward, backward, turn in place)    |
| Camera initialization errors in Thonny                            | Unified PiCamera2 init once; avoided repeated `__init__` calls                |

---


## Conclusion & Future Work



- **Achieved**: a stable, hardware-modular, face-following rover that behaves like a loyal puppy.  

- **Lessons**: modular design, clear flowchart → pseudocode → iterative tuning.  

- **Next steps**: upgrade to DNN-based face recognition for robustness, improve bracket materials, integrate obstacle avoidance back into the tracking loop.



---



**Thank you for exploring our final project!**  

This repository contains our team’s original Python code, presentation slides, and demonstration video. The OpenCV Haar Cascade files (haar/*.xml) are from the official OpenCV project and are licensed under the BSD license. All hardware selection and driver code were designed and implemented by our team under the guidance of Professor Zahra Noroozi.

Feel free to open issues or pull requests for improvements.
