"""
Distraction Detection Module
Monitors gaze direction and head pose to detect driver distraction.
"""

import numpy as np
from scipy.spatial import distance


class DistractionDetector:
    """Detects driver distraction based on gaze direction and head pose."""
    
    # Thresholds for distraction detection
    GAZE_THRESHOLD = 30  # degrees
    HEAD_POSE_THRESHOLD = 25  # degrees
    DISTRACTION_FRAMES = 20  # consecutive frames for distraction
    
    def __init__(self, gaze_threshold=None, head_pose_threshold=None):
        """
        Initialize the distraction detector.
        
        Args:
            gaze_threshold: Maximum gaze angle deviation (degrees)
            head_pose_threshold: Maximum head pose angle deviation (degrees)
        """
        self.gaze_threshold = gaze_threshold or self.GAZE_THRESHOLD
        self.head_pose_threshold = head_pose_threshold or self.HEAD_POSE_THRESHOLD
        self.distraction_counter = 0
        self.distracted = False
        
    def calculate_gaze_direction(self, eye_landmarks, face_center):
        """
        Calculate gaze direction from eye landmarks.
        
        Args:
            eye_landmarks: Array of (x, y) coordinates for eye landmarks
            face_center: (x, y) coordinates of face center
            
        Returns:
            dict: Gaze direction information
        """
        # Calculate eye center
        eye_center = np.mean(eye_landmarks, axis=0)
        
        # Calculate gaze vector
        gaze_vector = eye_center - face_center
        
        # Calculate gaze angle (approximation)
        gaze_angle = np.arctan2(gaze_vector[1], gaze_vector[0]) * 180 / np.pi
        
        return {
            "gaze_angle": gaze_angle,
            "gaze_vector": gaze_vector
        }
    
    def estimate_head_pose(self, face_landmarks):
        """
        Estimate head pose from facial landmarks.
        
        Args:
            face_landmarks: Array of facial landmark coordinates
            
        Returns:
            dict: Head pose angles (pitch, yaw, roll)
        """
        # Simplified head pose estimation
        # In a real system, this would use PnP algorithm with 3D model
        
        # Extract key points for pose estimation
        nose_tip = face_landmarks[30]
        chin = face_landmarks[8]
        left_eye = np.mean(face_landmarks[36:42], axis=0)
        right_eye = np.mean(face_landmarks[42:48], axis=0)
        left_mouth = face_landmarks[48]
        right_mouth = face_landmarks[54]
        
        # Calculate approximate angles
        # Yaw (horizontal rotation)
        eye_center = (left_eye + right_eye) / 2
        mouth_center = (left_mouth + right_mouth) / 2
        yaw = np.arctan2(nose_tip[0] - eye_center[0], 
                         nose_tip[1] - eye_center[1]) * 180 / np.pi
        
        # Pitch (vertical rotation)
        pitch = np.arctan2(nose_tip[1] - chin[1], 
                          nose_tip[0] - chin[0]) * 180 / np.pi
        
        # Roll (tilt)
        roll = np.arctan2(right_eye[1] - left_eye[1], 
                         right_eye[0] - left_eye[0]) * 180 / np.pi
        
        return {
            "pitch": pitch,
            "yaw": yaw,
            "roll": roll
        }
    
    def detect_distraction(self, head_pose, gaze_info=None):
        """
        Detect driver distraction based on head pose and gaze.
        
        Args:
            head_pose: Dictionary with pitch, yaw, roll angles
            gaze_info: Optional gaze direction information
            
        Returns:
            dict: Distraction detection results
        """
        # Check if head pose indicates looking away
        head_distracted = (
            abs(head_pose["yaw"]) > self.head_pose_threshold or
            abs(head_pose["pitch"]) > self.head_pose_threshold
        )
        
        # Check gaze if available
        gaze_distracted = False
        if gaze_info:
            gaze_distracted = abs(gaze_info["gaze_angle"]) > self.gaze_threshold
        
        # Determine overall distraction
        is_distracted = head_distracted or gaze_distracted
        
        if is_distracted:
            self.distraction_counter += 1
            if self.distraction_counter >= self.DISTRACTION_FRAMES:
                self.distracted = True
        else:
            self.distraction_counter = 0
            self.distracted = False
        
        return {
            "distracted": self.distracted,
            "head_distracted": head_distracted,
            "gaze_distracted": gaze_distracted,
            "distraction_counter": self.distraction_counter,
            "head_pose": head_pose,
            "gaze_info": gaze_info
        }
    
    def detect_phone_usage(self, hand_landmarks, face_region):
        """
        Detect potential phone usage near face.
        
        Args:
            hand_landmarks: Hand landmark positions
            face_region: Face bounding box region
            
        Returns:
            dict: Phone usage detection results
        """
        # Simplified phone detection
        # Check if hand is near face region
        phone_detected = False
        
        if hand_landmarks is not None:
            # Check if hand overlaps with face region
            for landmark in hand_landmarks:
                if self._point_in_region(landmark, face_region):
                    phone_detected = True
                    break
        
        return {
            "phone_detected": phone_detected
        }
    
    def _point_in_region(self, point, region):
        """
        Check if a point is within a rectangular region.
        
        Args:
            point: (x, y) coordinates
            region: (x, y, w, h) bounding box
            
        Returns:
            bool: True if point is in region
        """
        x, y = point
        rx, ry, rw, rh = region
        return rx <= x <= rx + rw and ry <= y <= ry + rh
    
    def reset(self):
        """Reset the detector state."""
        self.distraction_counter = 0
        self.distracted = False
