### Requirements
## Hardware
Tello Drone and a laptop with a working camera.
## Software
Python 3.7+
Operating system with a camera driver (Windows, Linux, or macOS).
### Installation
## Clone or Download the repository:
bash
git clone https://github.com/yourusername/drone-gesture-control.git
cd drone-gesture-control
## Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```
## Install dependencies:
```
pip install djitellopy mediapipe opencv-python
```
### Project Structure

main.py: Entry point. Initializes threads, captures frames, runs gesture detection, and displays HUD.
drone_controller.py: Manages background command execution for Tello.
gesture_detector.py: Contains Mediapipe logic for detecting gestures.
camera_thread.py: Implements a threaded camera capture class.
### Running the Application
Connect your computer to the Tello’s Wi-Fi network.
Run the main script:
```
python main.py
```
Observe the camera feed window. Perform gestures in front of the laptop camera:
Left arm raised ⇒ Moves drone left
Right arm raised ⇒ Moves drone right
Both arms raised for 4 seconds ⇒ Toggles takeoff/land
Otherwise ⇒ Hover command
Keyboard Commands (as implemented in main.py):
Press t for take off or landing.
Press q to quit/exit the program.
### Future Enhancements
Add more gestures like forward/backward, rotate.
Add error handling.
Enhance reliability with confidence thresholds or additional landmark checks.
Voice commands as a fallback or supplementary control method.