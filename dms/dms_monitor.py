"""
DMS Monitor - Main Driver Monitoring System
Integrates all detection modules and manages the monitoring workflow.
"""

import time
import numpy as np
from .drowsiness_detector import DrowsinessDetector
from .distraction_detector import DistractionDetector
from .alert_system import AlertSystem, AlertType, AlertLevel


class DMSMonitor:
    """Main driver monitoring system that coordinates all detection modules."""
    
    def __init__(self, config=None):
        """
        Initialize the DMS Monitor.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Initialize detection modules
        self.drowsiness_detector = DrowsinessDetector(
            ear_threshold=self.config.get('ear_threshold'),
            ear_consec_frames=self.config.get('ear_consec_frames')
        )
        
        self.distraction_detector = DistractionDetector(
            gaze_threshold=self.config.get('gaze_threshold'),
            head_pose_threshold=self.config.get('head_pose_threshold')
        )
        
        self.alert_system = AlertSystem(
            cooldown_period=self.config.get('alert_cooldown', 5.0)
        )
        
        # Monitoring state
        self.monitoring = False
        self.start_time = None
        self.frame_count = 0
        
        # Statistics
        self.stats = {
            "total_frames": 0,
            "drowsiness_events": 0,
            "distraction_events": 0,
            "total_blinks": 0,
            "session_duration": 0
        }
    
    def start_monitoring(self):
        """Start the monitoring session."""
        self.monitoring = True
        self.start_time = time.time()
        print("🚗 Driver Monitoring System Started")
        print("=" * 50)
    
    def stop_monitoring(self):
        """Stop the monitoring session."""
        self.monitoring = False
        self.stats["session_duration"] = time.time() - self.start_time
        print("\n" + "=" * 50)
        print("🛑 Driver Monitoring System Stopped")
        self._print_summary()
    
    def process_frame(self, facial_landmarks):
        """
        Process a single frame with facial landmarks.
        
        Args:
            facial_landmarks: Dictionary containing facial landmark data
                Expected keys: 'left_eye', 'right_eye', 'mouth', 'face_landmarks'
                
        Returns:
            dict: Processing results including detections and alerts
        """
        if not self.monitoring:
            return {"error": "Monitoring not started"}
        
        self.frame_count += 1
        self.stats["total_frames"] += 1
        
        results = {
            "frame_number": self.frame_count,
            "timestamp": time.time() - self.start_time,
            "detections": {},
            "alerts": []
        }
        
        try:
            # Drowsiness detection
            if 'left_eye' in facial_landmarks and 'right_eye' in facial_landmarks:
                drowsiness_result = self.drowsiness_detector.detect_drowsiness(
                    facial_landmarks['left_eye'],
                    facial_landmarks['right_eye']
                )
                results["detections"]["drowsiness"] = drowsiness_result
                
                # Update blink statistics
                self.stats["total_blinks"] = drowsiness_result["total_blinks"]
                
                # Trigger drowsiness alert if needed
                if drowsiness_result["drowsy"]:
                    alert = self.alert_system.trigger_alert(
                        AlertType.DROWSINESS,
                        AlertLevel.CRITICAL
                    )
                    if alert:
                        results["alerts"].append(alert)
                        self.stats["drowsiness_events"] += 1
            
            # Yawning detection
            if 'mouth' in facial_landmarks:
                yawn_result = self.drowsiness_detector.detect_yawning(
                    facial_landmarks['mouth']
                )
                results["detections"]["yawning"] = yawn_result
                
                if yawn_result["yawning"]:
                    alert = self.alert_system.trigger_alert(
                        AlertType.YAWNING,
                        AlertLevel.INFO
                    )
                    if alert:
                        results["alerts"].append(alert)
            
            # Distraction detection
            if 'face_landmarks' in facial_landmarks:
                head_pose = self.distraction_detector.estimate_head_pose(
                    facial_landmarks['face_landmarks']
                )
                
                # Optional gaze calculation
                gaze_info = None
                if 'left_eye' in facial_landmarks and 'face_center' in facial_landmarks:
                    gaze_info = self.distraction_detector.calculate_gaze_direction(
                        facial_landmarks['left_eye'],
                        facial_landmarks['face_center']
                    )
                
                distraction_result = self.distraction_detector.detect_distraction(
                    head_pose,
                    gaze_info
                )
                results["detections"]["distraction"] = distraction_result
                
                # Trigger distraction alert if needed
                if distraction_result["distracted"]:
                    alert = self.alert_system.trigger_alert(
                        AlertType.DISTRACTION,
                        AlertLevel.WARNING
                    )
                    if alert:
                        results["alerts"].append(alert)
                        self.stats["distraction_events"] += 1
            
            # Phone usage detection (if hand landmarks available)
            if 'hand_landmarks' in facial_landmarks and 'face_region' in facial_landmarks:
                phone_result = self.distraction_detector.detect_phone_usage(
                    facial_landmarks['hand_landmarks'],
                    facial_landmarks['face_region']
                )
                results["detections"]["phone_usage"] = phone_result
                
                if phone_result["phone_detected"]:
                    alert = self.alert_system.trigger_alert(
                        AlertType.PHONE_USAGE,
                        AlertLevel.CRITICAL
                    )
                    if alert:
                        results["alerts"].append(alert)
        
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def get_status(self):
        """
        Get current monitoring status.
        
        Returns:
            dict: Current status information
        """
        return {
            "monitoring": self.monitoring,
            "session_duration": time.time() - self.start_time if self.start_time else 0,
            "frame_count": self.frame_count,
            "active_alerts": self.alert_system.get_active_alerts(),
            "stats": self.stats
        }
    
    def get_statistics(self):
        """
        Get detailed statistics.
        
        Returns:
            dict: Detailed statistics
        """
        stats = self.stats.copy()
        stats["alert_stats"] = self.alert_system.get_alert_stats()
        return stats
    
    def _print_summary(self):
        """Print monitoring session summary."""
        print("\n📊 Session Summary:")
        print(f"   Duration: {self.stats['session_duration']:.1f} seconds")
        print(f"   Frames Processed: {self.stats['total_frames']}")
        print(f"   Total Blinks: {self.stats['total_blinks']}")
        print(f"   Drowsiness Events: {self.stats['drowsiness_events']}")
        print(f"   Distraction Events: {self.stats['distraction_events']}")
        
        alert_stats = self.alert_system.get_alert_stats()
        print(f"\n   Total Alerts: {alert_stats['total_alerts']}")
        if alert_stats['by_type']:
            print("   Alerts by Type:")
            for alert_type, count in alert_stats['by_type'].items():
                print(f"      - {alert_type}: {count}")
    
    def reset(self):
        """Reset all monitoring state and statistics."""
        self.drowsiness_detector.reset()
        self.distraction_detector.reset()
        self.alert_system.reset()
        self.frame_count = 0
        self.stats = {
            "total_frames": 0,
            "drowsiness_events": 0,
            "distraction_events": 0,
            "total_blinks": 0,
            "session_duration": 0
        }
