# Driver Monitoring System (DMS)

A comprehensive Python-based Driver Monitoring System for detecting driver drowsiness, distraction, and unsafe behaviors in real-time.

## Features

- **Drowsiness Detection**: Monitors eye closure patterns and blink rates using Eye Aspect Ratio (EAR)
- **Distraction Detection**: Tracks head pose and gaze direction to identify when drivers look away from the road
- **Yawning Detection**: Detects yawning using Mouth Aspect Ratio (MAR) analysis
- **Alert System**: Multi-level alert system (INFO, WARNING, CRITICAL) with configurable cooldown periods
- **Real-time Monitoring**: Process video frames in real-time with comprehensive statistics
- **Modular Architecture**: Clean separation of detection modules for easy extension and testing

## Installation

### Requirements

- Python 3.7+
- NumPy
- SciPy
- OpenCV (optional, for camera integration)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vsinghce/dms.git
cd dms
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Quick Start

Run the demo application to see the system in action:

```bash
python examples/demo.py
```

### Basic Example

```python
import numpy as np
from dms import DMSMonitor

# Create monitor instance
monitor = DMSMonitor()
monitor.start_monitoring()

# Process frames with facial landmarks
landmarks = {
    'left_eye': np.array([[100, 200], [105, 195], ...]),
    'right_eye': np.array([[150, 200], [155, 195], ...]),
    'mouth': np.array([[120, 250], [122, 250], ...]),
    'face_landmarks': np.array([[x, y], ...]),
    'face_center': np.array([132, 220])
}

result = monitor.process_frame(landmarks)

# Check for drowsiness
if result['detections']['drowsiness']['drowsy']:
    print("Driver is drowsy!")

# Stop monitoring
monitor.stop_monitoring()
```

### Custom Configuration

```python
config = {
    'ear_threshold': 0.25,        # Eye Aspect Ratio threshold
    'ear_consec_frames': 15,      # Frames for drowsiness detection
    'gaze_threshold': 30,         # Gaze angle threshold (degrees)
    'head_pose_threshold': 25,    # Head pose threshold (degrees)
    'alert_cooldown': 5.0         # Alert cooldown period (seconds)
}

monitor = DMSMonitor(config)
```

## Architecture

The system is organized into modular components:

```
dms/
├── __init__.py               # Package initialization
├── drowsiness_detector.py    # Drowsiness detection module
├── distraction_detector.py   # Distraction detection module
├── alert_system.py          # Alert management system
└── dms_monitor.py           # Main monitoring coordinator
```

### Components

#### 1. Drowsiness Detector
- Calculates Eye Aspect Ratio (EAR)
- Detects prolonged eye closure
- Counts blinks
- Detects yawning using Mouth Aspect Ratio (MAR)

#### 2. Distraction Detector
- Estimates head pose (pitch, yaw, roll)
- Calculates gaze direction
- Detects prolonged distraction
- Phone usage detection (with hand landmarks)

#### 3. Alert System
- Multi-level alerts (INFO, WARNING, CRITICAL)
- Cooldown management to prevent alert spam
- Alert history and statistics
- Extensible alert dispatch mechanism

#### 4. DMS Monitor
- Coordinates all detection modules
- Manages monitoring session lifecycle
- Tracks comprehensive statistics
- Provides unified API

## Detection Methods

### Eye Aspect Ratio (EAR)

The system uses the Eye Aspect Ratio formula to detect eye closure:

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

Where p1-p6 are the eye landmark coordinates. When EAR falls below the threshold for consecutive frames, drowsiness is detected.

### Mouth Aspect Ratio (MAR)

Yawning is detected using the Mouth Aspect Ratio:

```
MAR = (||p14 - p20|| + ||p15 - p19|| + ||p16 - p18||) / (3 * ||p13 - p17||)
```

Higher MAR values indicate mouth opening, which can indicate yawning.

### Head Pose Estimation

Head pose angles (pitch, yaw, roll) are estimated from facial landmarks to determine if the driver is looking away from the road.

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_drowsiness_detector.py

# Run with coverage
python -m pytest tests/ --cov=dms --cov-report=html
```

Or using unittest:

```bash
python -m unittest discover tests/
```

## Examples

### 1. Simple Example
```bash
python examples/simple_example.py
```

### 2. Full Demo
```bash
python examples/demo.py
```

The demo simulates different driving scenarios:
- Normal driving
- Drowsy driver
- Distracted driver

## API Reference

### DMSMonitor

Main monitoring coordinator class.

**Methods:**
- `start_monitoring()`: Start monitoring session
- `stop_monitoring()`: Stop monitoring and print summary
- `process_frame(landmarks)`: Process a single frame
- `get_status()`: Get current monitoring status
- `get_statistics()`: Get detailed statistics
- `reset()`: Reset all state

### DrowsinessDetector

Detects driver drowsiness based on eye and mouth analysis.

**Methods:**
- `detect_drowsiness(left_eye, right_eye)`: Detect drowsiness from eye landmarks
- `detect_yawning(mouth_landmarks)`: Detect yawning from mouth landmarks
- `calculate_eye_aspect_ratio(eye_landmarks)`: Calculate EAR
- `calculate_mouth_aspect_ratio(mouth_landmarks)`: Calculate MAR

### DistractionDetector

Detects driver distraction based on head pose and gaze.

**Methods:**
- `detect_distraction(head_pose, gaze_info)`: Detect distraction
- `estimate_head_pose(face_landmarks)`: Estimate head pose angles
- `calculate_gaze_direction(eye_landmarks, face_center)`: Calculate gaze
- `detect_phone_usage(hand_landmarks, face_region)`: Detect phone usage

### AlertSystem

Manages alerts and notifications.

**Methods:**
- `trigger_alert(alert_type, alert_level, message)`: Trigger an alert
- `clear_alert(alert_type)`: Clear an active alert
- `get_active_alerts()`: Get list of active alerts
- `get_alert_history(last_n)`: Get recent alert history
- `get_alert_stats()`: Get alert statistics

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ear_threshold` | 0.25 | Eye Aspect Ratio threshold for closed eyes |
| `ear_consec_frames` | 15 | Consecutive frames needed for drowsiness detection |
| `gaze_threshold` | 30 | Maximum gaze angle deviation (degrees) |
| `head_pose_threshold` | 25 | Maximum head pose angle deviation (degrees) |
| `alert_cooldown` | 5.0 | Minimum time between repeated alerts (seconds) |

## Performance

The system is designed for real-time performance:
- Lightweight algorithms suitable for embedded systems
- Minimal computational overhead
- Efficient frame processing
- Configurable detection sensitivity

## Future Enhancements

Potential areas for improvement:
- Camera integration with live video feed
- Deep learning models for improved accuracy
- Driver identification and personalization
- Integration with vehicle systems (CAN bus)
- Cloud logging and analytics
- Mobile app integration
- Multi-camera support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

Based on research in driver monitoring systems and computer vision techniques for automotive safety.

## Contact

For questions or issues, please open an issue on GitHub.