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

10. [Demo Videos](#demo-videos)

11. [License](#license)
    
12. [Acknowledgements](#acknowledgements)

---



## Introduction & Purpose



Our four-wheel rover is designed to **detect and follow human faces**—“threats” in a security scenario—**while maintaining a safe distance**. It uses:



- A **TF-Luna** LiDAR sensor for obstacle/distance detection  

- A **Pan/Tilt** assembly for camera and sensor aiming  

- **OpenCV face detection** for visual tracking  



This project demonstrates integrating hardware, mechanical design, and control software into a cohesive, autonomous system.



---



## Team Members & Professor


- **Professor Zahra Noroozi** — IVC IDEA Department Chair, Integrated Design, Automation & Engineering
  
- [**Cole M.**](https://github.com/CGeipel) — Mechanical design, hardware testing
  
- [**Zaid A.**](https://github.com/HeadHoncho21) — Component selection & integration
  
- [**Zesen L.**](https://github.com/OrionHachiii) — Flowchart & code implementation, GitHub repo management
  
- **Davoud G.** — SolidWorks bracket design & key features  


> Note: While roles were divided for clarity, all team members collaborated across all project stages, including hardware setup, coding, testing, and presentation.

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
       - **Too far** → forward  
       - **Just right**:
         - if camera angle > center + tolerance → turn right  
         - if camera angle < center − tolerance → turn left  
         - else → go forward



4. **Cleanup on Ctrl+C**  



A full flowchart diagram is provided in `Team 3 Final Presentation.pdf`.



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



## Demo Videos



- **Live Demo 1**: [IVC ENGR 100 Team 3 | Face-Following Rover Live Demo 1](https://youtube.com/shorts/JToTrOTbqbI?feature=share)  
- **Live Demo 2**: [IVC ENGR 100 Team 3 | Face-Following Rover Live Demo 2](https://youtu.be/TYwNfeY9g4M)  



---



## 11. License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute the code with proper attribution.  
See the [LICENSE](./LICENSE) file for full terms.

> The file `haarcascade_frontalface_default.xml` used for face detection was obtained from the official [OpenCV project](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)  
> and is licensed under the **BSD license**.

---

## 12. Acknowledgements

We would like to thank:

- **Professor Zahra Noroozi**, for her continued support and academic guidance throughout the course.  
- The **OpenCV team**, for providing powerful and accessible computer vision tools.  
- Our IVC ENGR 100 classmates, lab staff, and reviewers.  
- And each other—as a team—for collaborating across all stages of development.

This project was developed as part of the Spring 2025 offering of **IVC ENGR 100**,  
and reflects our collective effort in integrating Raspberry Pi hardware, Python code, servo control, and LiDAR sensing into a fully functional face-following rover.

---


**Thank you for exploring our final project!**

Feel free to open issues or pull requests for improvements.
