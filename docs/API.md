# Driver Monitoring System API Documentation

## Overview

The Driver Monitoring System (DMS) provides a simple API for tracking and managing driver statuses in real-time.

## Core Classes

### DriverStatus (Enum)

Enumeration of possible driver statuses.

**Values:**
- `ACTIVE`: Driver is currently active and working
- `INACTIVE`: Driver is not currently working but available
- `ON_BREAK`: Driver is on a scheduled break
- `OFFLINE`: Driver is not available

### Driver

Represents a driver in the monitoring system.

#### Constructor

```python
Driver(driver_id: str, name: str, status: DriverStatus = DriverStatus.OFFLINE)
```

**Parameters:**
- `driver_id` (str): Unique identifier for the driver
- `name` (str): Driver's name
- `status` (DriverStatus, optional): Initial status (defaults to OFFLINE)

#### Methods

##### update_status(new_status: DriverStatus) -> None

Updates the driver's status and last_updated timestamp.

**Parameters:**
- `new_status` (DriverStatus): The new status to set

##### get_info() -> dict

Returns driver information as a dictionary.

**Returns:**
- Dictionary with keys: `driver_id`, `name`, `status`, `last_updated`

#### Attributes

- `driver_id` (str): Unique identifier
- `name` (str): Driver's name
- `status` (DriverStatus): Current status
- `last_updated` (datetime): Timestamp of last status update

### DriverMonitor

Main monitoring system for managing driver statuses and information.

#### Constructor

```python
DriverMonitor()
```

Initializes an empty monitoring system.

#### Methods

##### add_driver(driver: Driver) -> None

Adds a new driver to the monitoring system.

**Parameters:**
- `driver` (Driver): Driver instance to add

**Raises:**
- `ValueError`: If driver with same ID already exists

##### remove_driver(driver_id: str) -> None

Removes a driver from the monitoring system.

**Parameters:**
- `driver_id` (str): ID of the driver to remove

**Raises:**
- `KeyError`: If driver with given ID doesn't exist

##### get_driver(driver_id: str) -> Optional[Driver]

Retrieves a driver by ID.

**Parameters:**
- `driver_id` (str): ID of the driver to retrieve

**Returns:**
- Driver instance if found, None otherwise

##### update_driver_status(driver_id: str, new_status: DriverStatus) -> None

Updates a driver's status.

**Parameters:**
- `driver_id` (str): ID of the driver to update
- `new_status` (DriverStatus): New status to set

**Raises:**
- `KeyError`: If driver with given ID doesn't exist

##### get_all_drivers() -> List[Driver]

Returns all drivers in the system.

**Returns:**
- List of all Driver instances

##### get_drivers_by_status(status: DriverStatus) -> List[Driver]

Filters drivers by status.

**Parameters:**
- `status` (DriverStatus): Status to filter by

**Returns:**
- List of Driver instances with the specified status

##### get_active_drivers_count() -> int

Returns the count of active drivers.

**Returns:**
- Number of drivers with ACTIVE status

##### get_summary() -> dict

Generates a summary of all drivers and their statuses.

**Returns:**
- Dictionary containing:
  - `total_drivers` (int): Total number of drivers
  - `by_status` (dict): Count of drivers for each status

## Usage Examples

### Basic Usage

```python
from dms import DriverMonitor, Driver, DriverStatus

# Create monitor
monitor = DriverMonitor()

# Add driver
driver = Driver("D001", "John Doe", DriverStatus.ACTIVE)
monitor.add_driver(driver)

# Update status
monitor.update_driver_status("D001", DriverStatus.ON_BREAK)

# Get info
driver_info = monitor.get_driver("D001").get_info()
```

### Filtering and Queries

```python
# Get all active drivers
active_drivers = monitor.get_drivers_by_status(DriverStatus.ACTIVE)

# Get summary
summary = monitor.get_summary()
print(f"Total: {summary['total_drivers']}")
print(f"Active: {summary['by_status']['active']}")
```

### Error Handling

```python
try:
    monitor.add_driver(duplicate_driver)
except ValueError as e:
    print(f"Driver already exists: {e}")

try:
    monitor.remove_driver("nonexistent_id")
except KeyError as e:
    print(f"Driver not found: {e}")
```

## Type Hints

All functions and methods include type hints for better IDE support and type checking. Use tools like `mypy` for static type checking:

```bash
pip install mypy
mypy src/dms/
```
