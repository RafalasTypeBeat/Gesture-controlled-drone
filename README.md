## Requirements
### Hardware
Tello Drone and a laptop with a working camera.
### Software
Python 3.7+
Operating system with a camera driver (Windows, Linux, or macOS).
## Installation
### Clone or Download the repository:
```
git clone https://github.com/RafalasTypeBeat/Gesture-controlled-drone.git
cd drone-gesture-control
```
### Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```
### Install dependencies:
```
pip install djitellopy mediapipe opencv-python
```
## Project Structure
* main.py: Entry point. Initializes threads, captures frames, runs gesture detection, and displays HUD.
* drone_controller.py: Manages background command execution for Tello.
* gesture_detector.py: Contains Mediapipe logic for detecting gestures.
* camera_thread.py: Implements a threaded camera capture class.
## Running the Application
1. Connect your computer to the Tello’s Wi-Fi network.
2. Run the main script:
```
python main.py
```
3. Perform gestures in front of the laptop camera:
* Left arm raised ⇒ Moves drone left
* Right arm raised ⇒ Moves drone right
* Both arms raised for 4 seconds ⇒ Toggles takeoff/land
* Otherwise ⇒ Hover command
### Keyboard Commands:
* Press t for take off or landing.
* Press q to quit/exit the program.
## Future Enhancements
* Add more gestures like forward/backward, rotate.
* Add error handling.
* Enhance reliability with confidence thresholds or additional landmark checks.
* Voice commands as a fallback or supplementary control method.