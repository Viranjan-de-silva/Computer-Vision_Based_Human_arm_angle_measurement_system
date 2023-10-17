# Computer-Vision_Based_Human_arm_angle_measurement_system
Here Google mediapipe is used with python-opencv to detect arm posture. Background webserver is running to communicate with mobile application. This project provides you to ability to measure each angle of human arm posture using one single web camera. 

- before run this program You have to import google mediapipe and python opencv libraries.
use,
    pip install google mediapipe
    pip install python-opencv
commands in command prompt or relavent virtual environment.

- then enter your local IP address inside the relevent place of httpServer.py file.
- You have to send a http request to python server in order to start measuring.
- Mathematical angle calculation part is included inside the controller.py file.
