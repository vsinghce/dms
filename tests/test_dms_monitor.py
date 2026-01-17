"""
Test suite for the DMSMonitor module.
"""

import unittest
import numpy as np
from dms.dms_monitor import DMSMonitor


class TestDMSMonitor(unittest.TestCase):
    """Test cases for DMSMonitor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = DMSMonitor()
        self.sample_landmarks = self._create_sample_landmarks()
    
    def _create_sample_landmarks(self):
        """Create sample facial landmarks for testing."""
        return {
            'left_eye': np.array([
                [100, 200], [105, 195], [110, 195],
                [115, 200], [110, 205], [105, 205]
            ]),
            'right_eye': np.array([
                [150, 200], [155, 195], [160, 195],
                [165, 200], [160, 205], [155, 205]
            ]),
            'mouth': np.array([[120 + i, 250] for i in range(20)]),
            'face_landmarks': np.random.rand(68, 2) * 50 + [100, 180],
            'face_center': np.array([132, 220])
        }
    
    def test_initialization(self):
        """Test monitor initialization."""
        self.assertIsNotNone(self.monitor)
        self.assertFalse(self.monitor.monitoring)
        self.assertEqual(self.monitor.frame_count, 0)
    
    def test_custom_config(self):
        """Test initialization with custom configuration."""
        config = {
            'ear_threshold': 0.3,
            'ear_consec_frames': 20,
            'alert_cooldown': 3.0
        }
        monitor = DMSMonitor(config)
        
        self.assertEqual(monitor.drowsiness_detector.ear_threshold, 0.3)
        self.assertEqual(monitor.drowsiness_detector.ear_consec_frames, 20)
        self.assertEqual(monitor.alert_system.cooldown_period, 3.0)
    
    def test_start_monitoring(self):
        """Test starting monitoring session."""
        self.monitor.start_monitoring()
        
        self.assertTrue(self.monitor.monitoring)
        self.assertIsNotNone(self.monitor.start_time)
    
    def test_stop_monitoring(self):
        """Test stopping monitoring session."""
        self.monitor.start_monitoring()
        self.monitor.stop_monitoring()
        
        self.assertFalse(self.monitor.monitoring)
        self.assertGreater(self.monitor.stats['session_duration'], 0)
    
    def test_process_frame(self):
        """Test processing a single frame."""
        self.monitor.start_monitoring()
        
        result = self.monitor.process_frame(self.sample_landmarks)
        
        self.assertIn('frame_number', result)
        self.assertIn('timestamp', result)
        self.assertIn('detections', result)
        self.assertIn('alerts', result)
        self.assertEqual(result['frame_number'], 1)
    
    def test_process_frame_without_monitoring(self):
        """Test processing frame when monitoring not started."""
        result = self.monitor.process_frame(self.sample_landmarks)
        
        self.assertIn('error', result)
    
    def test_drowsiness_detection(self):
        """Test drowsiness detection in processing."""
        self.monitor.start_monitoring()
        
        result = self.monitor.process_frame(self.sample_landmarks)
        
        self.assertIn('drowsiness', result['detections'])
        drowsiness = result['detections']['drowsiness']
        self.assertIn('drowsy', drowsiness)
        self.assertIn('ear', drowsiness)
    
    def test_yawning_detection(self):
        """Test yawning detection in processing."""
        self.monitor.start_monitoring()
        
        result = self.monitor.process_frame(self.sample_landmarks)
        
        self.assertIn('yawning', result['detections'])
        yawning = result['detections']['yawning']
        self.assertIn('yawning', yawning)
        self.assertIn('mar', yawning)
    
    def test_distraction_detection(self):
        """Test distraction detection in processing."""
        self.monitor.start_monitoring()
        
        result = self.monitor.process_frame(self.sample_landmarks)
        
        self.assertIn('distraction', result['detections'])
        distraction = result['detections']['distraction']
        self.assertIn('distracted', distraction)
        self.assertIn('head_pose', distraction)
    
    def test_frame_counting(self):
        """Test frame counting."""
        self.monitor.start_monitoring()
        
        for i in range(5):
            result = self.monitor.process_frame(self.sample_landmarks)
            self.assertEqual(result['frame_number'], i + 1)
        
        self.assertEqual(self.monitor.frame_count, 5)
    
    def test_statistics_tracking(self):
        """Test statistics tracking."""
        self.monitor.start_monitoring()
        
        # Process some frames
        for _ in range(10):
            self.monitor.process_frame(self.sample_landmarks)
        
        stats = self.monitor.get_statistics()
        
        self.assertEqual(stats['total_frames'], 10)
        self.assertIn('alert_stats', stats)
    
    def test_get_status(self):
        """Test getting current status."""
        self.monitor.start_monitoring()
        self.monitor.process_frame(self.sample_landmarks)
        
        status = self.monitor.get_status()
        
        self.assertTrue(status['monitoring'])
        self.assertGreater(status['session_duration'], 0)
        self.assertEqual(status['frame_count'], 1)
        self.assertIn('active_alerts', status)
        self.assertIn('stats', status)
    
    def test_reset(self):
        """Test monitor reset."""
        self.monitor.start_monitoring()
        
        # Process some frames
        for _ in range(5):
            self.monitor.process_frame(self.sample_landmarks)
        
        # Reset
        self.monitor.reset()
        
        # Check state is reset
        self.assertEqual(self.monitor.frame_count, 0)
        self.assertEqual(self.monitor.stats['total_frames'], 0)
        self.assertEqual(self.monitor.stats['total_blinks'], 0)
    
    def test_multiple_frames_processing(self):
        """Test processing multiple frames."""
        self.monitor.start_monitoring()
        
        results = []
        for _ in range(20):
            result = self.monitor.process_frame(self.sample_landmarks)
            results.append(result)
        
        # All frames should be processed
        self.assertEqual(len(results), 20)
        
        # Frame numbers should increment
        for i, result in enumerate(results):
            self.assertEqual(result['frame_number'], i + 1)


if __name__ == '__main__':
    unittest.main()
