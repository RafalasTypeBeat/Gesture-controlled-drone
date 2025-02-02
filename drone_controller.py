import threading
import time
import cv2
from djitellopy import Tello

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.is_flying = False

        self.current_command = None
        self.command_in_progress = False

        self.active_command = None
        
        self.video_writer = None
        self.frame_width = 640
        self.frame_height = 480

        # Start a background thread to process commands
        self.running = True
        self.command_thread = threading.Thread(target=self._process_commands, daemon=True)
        self.command_thread.start()

    def connect(self):
        self.tello.connect()
        battery = self.tello.get_battery()
        print(f"[INFO] Drone battery: {battery}%")

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.video_writer = cv2.VideoWriter(
            f'flight_{timestamp}.avi',
            cv2.VideoWriter_fourcc(*'XVID'),
            30,
            (self.frame_width, self.frame_height)
        )

    def send_command(self, command: str):
        """
        Set a command to be executed by the background thread.
        If a command is already in progress or set, this will overwrite it.
        """
        self.current_command = command

    def _process_commands(self):
        """
        Background thread target function:
        Continuously checks if there's a command to run, then executes it.
        """
        while self.running:
            # If we have a command and we're not in the middle of another command
            if self.current_command and not self.command_in_progress:
                self.command_in_progress = True
                cmd = self.current_command
                self.current_command = None

                self._execute_command(cmd)
                self.command_in_progress = False

            time.sleep(0.05)  # small delay to avoid busy-wait

    def _execute_command(self, command: str):
        print(f"[CMD SENT] {command}")  # Print the command to console
        self.active_command = command
        try:
            if command == "TOGGLE_FLIGHT":
                if not self.is_flying:
                    # Take off
                    self.tello.takeoff() 
                    self.is_flying = True
                else:
                    # Land
                    self.tello.land()
                    self.is_flying = False
            elif self.is_flying:
                # Only move if the drone is in the air
                if command == "LEFT":
                    self.tello.move_left(30)  # blocks ~1s
                elif command == "RIGHT":
                    self.tello.move_right(30)
                elif command == "UP" and self.is_flying:
                    self.tello.move_up(30)
                elif command == "HOVER":
                    # Just zero out any motion
                    self.tello.send_rc_control(0,0,0,0)

        except Exception as e:
            print(f"[ERROR] Command {command} failed: {e}")

    def end(self):
        """
        Clean up resources when program exits.
        """
        self.running = False
        self.command_thread.join()

        if self.is_flying:
            try:
                self.tello.land()
            except:
                pass

        if self.video_writer:
            self.video_writer.release()

        self.tello.end()
