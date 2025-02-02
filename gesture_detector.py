import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.prev_gesture = None

    def detect_gesture(self, frame):
        """
        Return (annotated_frame, gesture).
          - "LEFT" if left elbow is higher than left shoulder.
          - "RIGHT" if right elbow is higher than right shoulder.
          - "UP" if both elbows are higher.
          - "HOVER" if none of the above.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        gesture = "HOVER"

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )
            landmarks = results.pose_landmarks.landmark

            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow    = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow   = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]

            # mirrored commands. This works if the drone is facing the user. If you want the drone 
            # to move to its actual left or right swap right_up with left_up 
            right_up = (left_elbow.y < left_shoulder.y)
            left_up = (right_elbow.y < right_shoulder.y)

            if left_up and right_up:
                gesture = "UP"
            elif left_up:
                gesture = "LEFT"
            elif right_up:
                gesture = "RIGHT"
            else:
                gesture = "HOVER"

        return frame, gesture
