"""
Drowsiness Detection Module
Monitors eye closure, blinking rates, and head position to detect drowsiness.
"""

from scipy.spatial import distance
import numpy as np


class DrowsinessDetector:
    """Detects driver drowsiness based on eye aspect ratio and head pose."""
    
    # Eye Aspect Ratio threshold
    EAR_THRESHOLD = 0.25
    # Number of consecutive frames the eye must be below threshold
    EAR_CONSEC_FRAMES = 15
    # Yawn threshold (Mouth Aspect Ratio)
    MAR_THRESHOLD = 0.6
    
    def __init__(self, ear_threshold=None, ear_consec_frames=None):
        """
        Initialize the drowsiness detector.
        
        Args:
            ear_threshold: Eye Aspect Ratio threshold for detecting closed eyes
            ear_consec_frames: Number of consecutive frames for drowsiness detection
        """
        self.ear_threshold = ear_threshold or self.EAR_THRESHOLD
        self.ear_consec_frames = ear_consec_frames or self.EAR_CONSEC_FRAMES
        self.frame_counter = 0
        self.total_blinks = 0
        self.drowsy = False
        
    def calculate_eye_aspect_ratio(self, eye_landmarks):
        """
        Calculate the Eye Aspect Ratio (EAR).
        
        Args:
            eye_landmarks: Array of (x, y) coordinates for eye landmarks
            
        Returns:
            float: Eye Aspect Ratio value
        """
        # Compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
        
        # Compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
        
        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        
        return ear
    
    def calculate_mouth_aspect_ratio(self, mouth_landmarks):
        """
        Calculate the Mouth Aspect Ratio (MAR) to detect yawning.
        
        Args:
            mouth_landmarks: Array of (x, y) coordinates for mouth landmarks
            
        Returns:
            float: Mouth Aspect Ratio value
        """
        # Compute vertical distances
        A = distance.euclidean(mouth_landmarks[13], mouth_landmarks[19])
        B = distance.euclidean(mouth_landmarks[14], mouth_landmarks[18])
        C = distance.euclidean(mouth_landmarks[15], mouth_landmarks[17])
        
        # Compute horizontal distance
        D = distance.euclidean(mouth_landmarks[12], mouth_landmarks[16])
        
        # Compute the mouth aspect ratio
        mar = (A + B + C) / (3.0 * D)
        
        return mar
    
    def detect_drowsiness(self, left_eye, right_eye):
        """
        Detect drowsiness based on eye aspect ratios.
        
        Args:
            left_eye: Landmarks for left eye
            right_eye: Landmarks for right eye
            
        Returns:
            dict: Detection results with drowsiness status and metrics
        """
        # Calculate EAR for both eyes
        left_ear = self.calculate_eye_aspect_ratio(left_eye)
        right_ear = self.calculate_eye_aspect_ratio(right_eye)
        
        # Average EAR
        ear = (left_ear + right_ear) / 2.0
        
        # Check if EAR is below threshold
        if ear < self.ear_threshold:
            self.frame_counter += 1
            
            # If eyes closed for sufficient frames, mark as drowsy
            if self.frame_counter >= self.ear_consec_frames:
                self.drowsy = True
        else:
            # If eyes were closed, increment blink counter
            if self.frame_counter >= 2:
                self.total_blinks += 1
            
            # Reset counter and drowsy status
            self.frame_counter = 0
            self.drowsy = False
        
        return {
            "drowsy": self.drowsy,
            "ear": ear,
            "frame_counter": self.frame_counter,
            "total_blinks": self.total_blinks
        }
    
    def detect_yawning(self, mouth_landmarks):
        """
        Detect yawning based on mouth aspect ratio.
        
        Args:
            mouth_landmarks: Landmarks for mouth
            
        Returns:
            dict: Yawning detection results
        """
        mar = self.calculate_mouth_aspect_ratio(mouth_landmarks)
        yawning = mar > self.MAR_THRESHOLD
        
        return {
            "yawning": yawning,
            "mar": mar
        }
    
    def reset(self):
        """Reset the detector state."""
        self.frame_counter = 0
        self.total_blinks = 0
        self.drowsy = False
