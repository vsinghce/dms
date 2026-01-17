"""
Driver class representing a driver entity in the monitoring system.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class DriverStatus(Enum):
    """Enumeration of possible driver statuses."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_BREAK = "on_break"
    OFFLINE = "offline"


class Driver:
    """
    Represents a driver in the monitoring system.
    
    Attributes:
        driver_id (str): Unique identifier for the driver
        name (str): Driver's name
        status (DriverStatus): Current status of the driver
        last_updated (datetime): Timestamp of last status update
    """
    
    def __init__(self, driver_id: str, name: str, status: DriverStatus = DriverStatus.OFFLINE):
        """
        Initialize a new Driver instance.
        
        Args:
            driver_id: Unique identifier for the driver
            name: Driver's name
            status: Initial status (defaults to OFFLINE)
        """
        self.driver_id = driver_id
        self.name = name
        self.status = status
        self.last_updated = datetime.now(timezone.utc)
    
    def update_status(self, new_status: DriverStatus) -> None:
        """
        Update the driver's status.
        
        Args:
            new_status: The new status to set
        """
        self.status = new_status
        self.last_updated = datetime.now(timezone.utc)
    
    def get_info(self) -> dict:
        """
        Get driver information as a dictionary.
        
        Returns:
            Dictionary containing driver information
        """
        return {
            "driver_id": self.driver_id,
            "name": self.name,
            "status": self.status.value,
            "last_updated": self.last_updated.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"Driver(id={self.driver_id}, name={self.name}, status={self.status.value})"
