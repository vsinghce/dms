"""
Test suite for the DrowsinessDetector module.
"""

import unittest
import numpy as np
from dms.drowsiness_detector import DrowsinessDetector


class TestDrowsinessDetector(unittest.TestCase):
    """Test cases for DrowsinessDetector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = DrowsinessDetector()
    
    def test_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.frame_counter, 0)
        self.assertEqual(self.detector.total_blinks, 0)
        self.assertFalse(self.detector.drowsy)
    
    def test_custom_thresholds(self):
        """Test initialization with custom thresholds."""
        detector = DrowsinessDetector(ear_threshold=0.3, ear_consec_frames=20)
        self.assertEqual(detector.ear_threshold, 0.3)
        self.assertEqual(detector.ear_consec_frames, 20)
    
    def test_calculate_eye_aspect_ratio(self):
        """Test EAR calculation."""
        # Create sample eye landmarks (6 points)
        eye = np.array([
            [100, 200],  # left corner
            [105, 195],  # top left
            [110, 195],  # top right
            [115, 200],  # right corner
            [110, 205],  # bottom right
            [105, 205]   # bottom left
        ])
        
        ear = self.detector.calculate_eye_aspect_ratio(eye)
        
        # EAR should be positive
        self.assertGreater(ear, 0)
        # For open eyes, EAR should be relatively high
        self.assertGreater(ear, 0.2)
    
    def test_calculate_mouth_aspect_ratio(self):
        """Test MAR calculation."""
        # Create sample mouth landmarks (20 points)
        mouth = np.array([[100 + i, 250] for i in range(20)])
        
        mar = self.detector.calculate_mouth_aspect_ratio(mouth)
        
        # MAR should be non-negative
        self.assertGreaterEqual(mar, 0)
    
    def test_detect_drowsiness_alert_eyes(self):
        """Test drowsiness detection with alert eyes."""
        # Open eyes
        left_eye = np.array([
            [100, 200], [105, 195], [110, 195],
            [115, 200], [110, 205], [105, 205]
        ])
        right_eye = np.array([
            [150, 200], [155, 195], [160, 195],
            [165, 200], [160, 205], [155, 205]
        ])
        
        result = self.detector.detect_drowsiness(left_eye, right_eye)
        
        self.assertIn('drowsy', result)
        self.assertIn('ear', result)
        self.assertFalse(result['drowsy'])
    
    def test_detect_drowsiness_closed_eyes(self):
        """Test drowsiness detection with closed eyes."""
        # Closed eyes (very small vertical distance)
        left_eye = np.array([
            [100, 200], [105, 200], [110, 200],
            [115, 200], [110, 200], [105, 200]
        ])
        right_eye = np.array([
            [150, 200], [155, 200], [160, 200],
            [165, 200], [160, 200], [155, 200]
        ])
        
        # Process multiple frames to trigger drowsiness
        for _ in range(20):
            result = self.detector.detect_drowsiness(left_eye, right_eye)
        
        # After many frames with closed eyes, should detect drowsiness
        self.assertTrue(result['drowsy'])
        self.assertLess(result['ear'], self.detector.ear_threshold)
    
    def test_detect_yawning(self):
        """Test yawning detection."""
        # Create mouth landmarks with large opening (yawning)
        mouth = np.array([
            [120, 230], [122, 235], [124, 240], [126, 245],
            [128, 250], [130, 255], [132, 260], [134, 265],
            [136, 270], [138, 275], [140, 280], [142, 285],
            [144, 280], [146, 275], [148, 270], [150, 265],
            [152, 260], [154, 255], [156, 250], [158, 245]
        ])
        
        result = self.detector.detect_yawning(mouth)
        
        self.assertIn('yawning', result)
        self.assertIn('mar', result)
        # With large vertical opening, should detect yawning
        self.assertTrue(result['yawning'])
    
    def test_blink_counting(self):
        """Test blink counting functionality."""
        open_eye = np.array([
            [100, 200], [105, 195], [110, 195],
            [115, 200], [110, 205], [105, 205]
        ])
        closed_eye = np.array([
            [100, 200], [105, 200], [110, 200],
            [115, 200], [110, 200], [105, 200]
        ])
        
        # Simulate a blink: open -> closed -> open
        initial_blinks = self.detector.total_blinks
        
        # Open eyes
        self.detector.detect_drowsiness(open_eye, open_eye)
        
        # Close eyes briefly
        for _ in range(3):
            self.detector.detect_drowsiness(closed_eye, closed_eye)
        
        # Open eyes again
        result = self.detector.detect_drowsiness(open_eye, open_eye)
        
        # Should have counted one blink
        self.assertGreater(result['total_blinks'], initial_blinks)
    
    def test_reset(self):
        """Test detector reset functionality."""
        # Modify detector state
        self.detector.frame_counter = 10
        self.detector.total_blinks = 5
        self.detector.drowsy = True
        
        # Reset
        self.detector.reset()
        
        # Check state is reset
        self.assertEqual(self.detector.frame_counter, 0)
        self.assertEqual(self.detector.total_blinks, 0)
        self.assertFalse(self.detector.drowsy)


if __name__ == '__main__':
    unittest.main()
