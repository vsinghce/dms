#!/usr/bin/env python3
"""
DMS Demo Application
Demonstrates the Driver Monitoring System with simulated data.
"""

import numpy as np
import time
from dms import DMSMonitor


def generate_sample_landmarks(scenario="normal"):
    """
    Generate sample facial landmarks for testing.
    
    Args:
        scenario: Type of scenario to simulate
                  "normal" - normal driving
                  "drowsy" - drowsy driver
                  "distracted" - distracted driver
    
    Returns:
        dict: Simulated facial landmarks
    """
    # Simulate eye landmarks (6 points per eye)
    if scenario == "drowsy":
        # Closed or nearly closed eyes
        left_eye = np.array([
            [100, 200], [105, 198], [110, 198],
            [115, 200], [110, 199], [105, 199]
        ])
        right_eye = np.array([
            [150, 200], [155, 198], [160, 198],
            [165, 200], [160, 199], [155, 199]
        ])
    else:
        # Open eyes
        left_eye = np.array([
            [100, 200], [105, 195], [110, 195],
            [115, 200], [110, 205], [105, 205]
        ])
        right_eye = np.array([
            [150, 200], [155, 195], [160, 195],
            [165, 200], [160, 205], [155, 205]
        ])
    
    # Simulate mouth landmarks (20 points)
    if scenario == "drowsy":
        # Mouth for yawning
        mouth = np.array([
            [132, 230], [133, 235], [134, 240], [135, 245],
            [136, 250], [137, 255], [138, 260], [139, 265],
            [140, 270], [141, 275], [142, 280], [143, 285],
            [144, 280], [145, 275], [146, 270], [147, 265],
            [148, 260], [149, 255], [150, 250], [151, 245]
        ])
    else:
        # Normal closed mouth
        mouth = np.array([
            [120, 250], [122, 250], [124, 250], [126, 250],
            [128, 250], [130, 250], [132, 250], [134, 250],
            [136, 250], [138, 250], [140, 250], [142, 250],
            [144, 250], [146, 250], [148, 250], [150, 250],
            [152, 250], [154, 250], [156, 250], [158, 250]
        ])
    
    # Simulate face landmarks (68 points - simplified)
    face_center = np.array([132, 220])
    
    if scenario == "distracted":
        # Head turned to the side
        face_landmarks = np.random.rand(68, 2) * 50 + [80, 150]
        face_landmarks[30] = [60, 220]  # nose tip shifted
    else:
        # Normal head position
        face_landmarks = np.random.rand(68, 2) * 50 + [100, 180]
        face_landmarks[30] = [132, 220]  # nose tip centered
    
    return {
        'left_eye': left_eye,
        'right_eye': right_eye,
        'mouth': mouth,
        'face_landmarks': face_landmarks,
        'face_center': face_center
    }


def run_demo():
    """Run a demonstration of the DMS."""
    print("=" * 60)
    print("  Driver Monitoring System - Demo Application")
    print("=" * 60)
    print("\nThis demo simulates different driving scenarios:\n")
    print("  1. Normal driving (10 frames)")
    print("  2. Drowsy driver (15 frames)")
    print("  3. Normal driving (10 frames)")
    print("  4. Distracted driver (25 frames)")
    print("  5. Normal driving (10 frames)")
    print("\n" + "=" * 60 + "\n")
    
    # Initialize DMS Monitor
    config = {
        'ear_threshold': 0.25,
        'ear_consec_frames': 10,
        'alert_cooldown': 3.0
    }
    
    monitor = DMSMonitor(config)
    monitor.start_monitoring()
    
    # Simulate different scenarios
    scenarios = [
        ("normal", 10),
        ("drowsy", 15),
        ("normal", 10),
        ("distracted", 25),
        ("normal", 10)
    ]
    
    try:
        for scenario_type, frame_count in scenarios:
            print(f"\n--- Simulating: {scenario_type.upper()} ({frame_count} frames) ---")
            
            for i in range(frame_count):
                # Generate sample landmarks for the scenario
                landmarks = generate_sample_landmarks(scenario_type)
                
                # Process frame
                result = monitor.process_frame(landmarks)
                
                # Print frame info every 5 frames or if there's an alert
                if i % 5 == 0 or result.get("alerts"):
                    print(f"\nFrame {result['frame_number']} @ {result['timestamp']:.1f}s")
                    
                    # Print detection results
                    if "drowsiness" in result["detections"]:
                        drowsy_data = result["detections"]["drowsiness"]
                        status = "DROWSY" if drowsy_data["drowsy"] else "ALERT"
                        print(f"  Eyes: {status} (EAR: {drowsy_data['ear']:.3f}, Blinks: {drowsy_data['total_blinks']})")
                    
                    if "distraction" in result["detections"]:
                        dist_data = result["detections"]["distraction"]
                        status = "DISTRACTED" if dist_data["distracted"] else "FOCUSED"
                        print(f"  Attention: {status}")
                    
                    # Print alerts
                    if result.get("alerts"):
                        for alert in result["alerts"]:
                            print(f"  🚨 ALERT: {alert['message']}")
                
                # Simulate frame processing delay
                time.sleep(0.1)
        
        # Stop monitoring and show summary
        monitor.stop_monitoring()
        
        # Show detailed statistics
        print("\n" + "=" * 60)
        print("📈 Detailed Statistics:")
        print("=" * 60)
        stats = monitor.get_statistics()
        alert_stats = stats.get('alert_stats', {})
        
        print(f"\nPerformance Metrics:")
        print(f"  Frames Processed: {stats['total_frames']}")
        print(f"  Average FPS: {stats['total_frames'] / stats['session_duration']:.1f}")
        
        print(f"\nDriver Behavior:")
        print(f"  Total Blinks: {stats['total_blinks']}")
        print(f"  Blink Rate: {stats['total_blinks'] / (stats['session_duration'] / 60):.1f} per minute")
        
        print(f"\nSafety Events:")
        print(f"  Drowsiness Events: {stats['drowsiness_events']}")
        print(f"  Distraction Events: {stats['distraction_events']}")
        print(f"  Total Alerts: {alert_stats.get('total_alerts', 0)}")
        
        if alert_stats.get('by_level'):
            print(f"\nAlerts by Severity:")
            for level, count in alert_stats['by_level'].items():
                print(f"  {level}: {count}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        monitor.stop_monitoring()
    
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_demo()
