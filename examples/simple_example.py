#!/usr/bin/env python3
"""
Simple example showing basic DMS usage.
"""

import numpy as np
from dms import DMSMonitor


def main():
    """Simple example of using the DMS Monitor."""
    
    # Create monitor instance with custom config
    config = {
        'ear_threshold': 0.25,
        'ear_consec_frames': 10,
        'alert_cooldown': 5.0
    }
    
    monitor = DMSMonitor(config)
    monitor.start_monitoring()
    
    # Simulate a few frames with sample data
    for i in range(5):
        # Create sample landmarks (normally these would come from a camera)
        landmarks = {
            'left_eye': np.array([
                [100, 200], [105, 195], [110, 195],
                [115, 200], [110, 205], [105, 205]
            ]),
            'right_eye': np.array([
                [150, 200], [155, 195], [160, 195],
                [165, 200], [160, 205], [155, 205]
            ]),
            'mouth': np.array([[120 + j, 250] for j in range(20)]),
            'face_landmarks': np.random.rand(68, 2) * 50 + [100, 180],
            'face_center': np.array([132, 220])
        }
        
        # Process the frame
        result = monitor.process_frame(landmarks)
        
        print(f"Frame {result['frame_number']}:")
        if 'drowsiness' in result['detections']:
            print(f"  EAR: {result['detections']['drowsiness']['ear']:.3f}")
        if result.get('alerts'):
            print(f"  Alerts: {len(result['alerts'])}")
    
    # Stop monitoring
    monitor.stop_monitoring()


if __name__ == "__main__":
    main()
