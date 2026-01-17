"""
DriverMonitor class for managing and monitoring multiple drivers.
"""

from typing import Dict, List, Optional
from .driver import Driver, DriverStatus


class DriverMonitor:
    """
    Main monitoring system for managing driver statuses and information.
    
    Attributes:
        drivers (Dict[str, Driver]): Dictionary of drivers indexed by driver_id
    """
    
    def __init__(self):
        """Initialize a new DriverMonitor instance."""
        self.drivers: Dict[str, Driver] = {}
    
    def add_driver(self, driver: Driver) -> None:
        """
        Add a new driver to the monitoring system.
        
        Args:
            driver: Driver instance to add
            
        Raises:
            ValueError: If driver with same ID already exists
        """
        if driver.driver_id in self.drivers:
            raise ValueError(f"Driver with ID {driver.driver_id} already exists")
        self.drivers[driver.driver_id] = driver
    
    def remove_driver(self, driver_id: str) -> None:
        """
        Remove a driver from the monitoring system.
        
        Args:
            driver_id: ID of the driver to remove
            
        Raises:
            KeyError: If driver with given ID doesn't exist
        """
        if driver_id not in self.drivers:
            raise KeyError(f"Driver with ID {driver_id} not found")
        del self.drivers[driver_id]
    
    def get_driver(self, driver_id: str) -> Optional[Driver]:
        """
        Get a driver by ID.
        
        Args:
            driver_id: ID of the driver to retrieve
            
        Returns:
            Driver instance if found, None otherwise
        """
        return self.drivers.get(driver_id)
    
    def update_driver_status(self, driver_id: str, new_status: DriverStatus) -> None:
        """
        Update a driver's status.
        
        Args:
            driver_id: ID of the driver to update
            new_status: New status to set
            
        Raises:
            KeyError: If driver with given ID doesn't exist
        """
        if driver_id not in self.drivers:
            raise KeyError(f"Driver with ID {driver_id} not found")
        self.drivers[driver_id].update_status(new_status)
    
    def get_all_drivers(self) -> List[Driver]:
        """
        Get all drivers in the system.
        
        Returns:
            List of all Driver instances
        """
        return list(self.drivers.values())
    
    def get_drivers_by_status(self, status: DriverStatus) -> List[Driver]:
        """
        Get all drivers with a specific status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of Driver instances with the specified status
        """
        return [driver for driver in self.drivers.values() if driver.status == status]
    
    def get_active_drivers_count(self) -> int:
        """
        Get the count of active drivers.
        
        Returns:
            Number of drivers with ACTIVE status
        """
        return len(self.get_drivers_by_status(DriverStatus.ACTIVE))
    
    def get_summary(self) -> dict:
        """
        Get a summary of all drivers and their statuses.
        
        Returns:
            Dictionary containing driver counts by status
        """
        summary = {
            "total_drivers": len(self.drivers),
            "by_status": {}
        }
        
        for status in DriverStatus:
            count = len(self.get_drivers_by_status(status))
            summary["by_status"][status.value] = count
        
        return summary
