import cv2
import time

from gesture_detector import GestureDetector
from drone_controller import DroneController
from camera_thread import CameraThread

def main():
    detector = GestureDetector()
    drone = DroneController()
    drone.connect()

    camera_thread = CameraThread(src=0, width=640, height=480)
    camera_thread.start()

    # Variables to handle continuous-gesture detection
    current_gesture = None
    gesture_start_time = None

    # For 1.5-second logic
    command_executed_1_5 = False

    # Special for "UP" logic: 4-second flight toggle
    up_move_time = None            # Timestamp after we send the UP command
    toggle_executed_4 = False      # Whether we've toggled flight after 4s

    try:
        while True:
            frame = camera_thread.frame
            if frame is None:
                continue

            annotated_frame, gesture = detector.detect_gesture(frame)

            # Check if gesture changed from previous iteration
            if gesture != current_gesture:
                # Reset everything because we have a new gesture
                current_gesture = gesture
                gesture_start_time = time.time()
                command_executed_1_5 = False
                up_move_time = None
                toggle_executed_4 = False

            # Calculate how long we've held this gesture
            hold_time = time.time() - gesture_start_time

            # Handle different gestures
            if gesture == "UP":
                # 1) After 1.5s, move up once (if not done yet)
                if not command_executed_1_5 and hold_time >= 1.5:
                    drone.send_command("UP")       # Single upward movement
                    command_executed_1_5 = True
                    up_move_time = time.time()     # Start 4s timer from now

                # 2) If we've already moved up, check if we should toggle flight
                if command_executed_1_5 and not toggle_executed_4:
                    elapsed_since_up = time.time() - up_move_time
                    # If user holds UP for an additional 4 seconds, toggle flight
                    if elapsed_since_up >= 3.0:
                        drone.send_command("TOGGLE_FLIGHT")
                        toggle_executed_4 = True

            elif gesture in ["LEFT", "RIGHT", "HOVER"]:
                # If we've held the gesture for 1.5 seconds, execute once
                if not command_executed_1_5 and hold_time >= 1.5:
                    drone.send_command(gesture)  # e.g. LEFT, RIGHT, or HOVER
                    command_executed_1_5 = True

            # Read the background-thread "active_command" to show on screen
            active_cmd = drone.active_command if drone.active_command else "HOVER"

            # Check keyboard for manual overrides
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                drone.send_command("TOGGLE_FLIGHT")

            # HUD
            cv2.putText(annotated_frame, f"Gesture: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Active: {active_cmd}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(annotated_frame, f"Battery: {drone.tello.get_battery()}%", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

            # If you want to record from your laptop camera:
            if drone.video_writer:
                drone.video_writer.write(annotated_frame)

            cv2.imshow("Drone Control", annotated_frame)

    finally:
        camera_thread.stop()
        camera_thread.join()
        drone.end()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
