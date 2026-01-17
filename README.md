# Driver Monitoring System (DMS)

A Python-based system for monitoring and tracking driver behavior and status in real-time.

## Overview

The Driver Monitoring System provides a simple yet effective way to track multiple drivers, their statuses, and generate monitoring reports. It's designed to be extensible and easy to integrate into existing fleet management or logistics applications.

## Features

- **Driver Management**: Add, remove, and retrieve driver information
- **Status Tracking**: Monitor driver statuses (Active, Inactive, On Break, Offline)
- **Real-time Updates**: Update driver status with automatic timestamp tracking
- **Query Capabilities**: Filter drivers by status and generate summary reports
- **Extensible Design**: Easy to extend with additional monitoring features

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/vsinghce/dms.git
cd dms

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

```python
from dms import DriverMonitor, Driver, DriverStatus

# Create a monitoring instance
monitor = DriverMonitor()

# Add drivers
driver1 = Driver("D001", "John Doe", DriverStatus.ACTIVE)
driver2 = Driver("D002", "Jane Smith", DriverStatus.OFFLINE)

monitor.add_driver(driver1)
monitor.add_driver(driver2)

# Update driver status
monitor.update_driver_status("D001", DriverStatus.ON_BREAK)

# Get driver information
driver = monitor.get_driver("D001")
print(driver.get_info())

# Get all active drivers
active_drivers = monitor.get_drivers_by_status(DriverStatus.ACTIVE)

# Get summary
summary = monitor.get_summary()
print(summary)
```

## Project Structure

```
dms/
├── src/
│   └── dms/
│       ├── __init__.py      # Package initialization
│       ├── driver.py        # Driver class and status definitions
│       └── monitor.py       # DriverMonitor main class
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── examples/                # Example usage scripts
├── requirements.txt         # Project dependencies
├── pyproject.toml          # Package configuration
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Driver Statuses

The system supports the following driver statuses:

- **ACTIVE**: Driver is currently active and working
- **INACTIVE**: Driver is not currently working but available
- **ON_BREAK**: Driver is on a scheduled break
- **OFFLINE**: Driver is not available

## API Reference

### Driver Class

- `Driver(driver_id, name, status)`: Create a new driver instance
- `update_status(new_status)`: Update the driver's status
- `get_info()`: Get driver information as a dictionary

### DriverMonitor Class

- `add_driver(driver)`: Add a new driver to the system
- `remove_driver(driver_id)`: Remove a driver from the system
- `get_driver(driver_id)`: Retrieve a driver by ID
- `update_driver_status(driver_id, new_status)`: Update a driver's status
- `get_all_drivers()`: Get all drivers in the system
- `get_drivers_by_status(status)`: Get drivers filtered by status
- `get_active_drivers_count()`: Get count of active drivers
- `get_summary()`: Get a summary report of all drivers

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Enhancements

- Real-time notifications for status changes
- Integration with GPS tracking systems
- Driver performance metrics and analytics
- Web dashboard for visualization
- REST API for remote access
- Database persistence for driver history
- Mobile app support