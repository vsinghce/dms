"""
Unit tests for the Driver class.
"""

import pytest
from datetime import datetime
from dms import Driver, DriverStatus


def test_driver_initialization():
    """Test driver initialization with default and custom status."""
    driver = Driver("D001", "John Doe")
    assert driver.driver_id == "D001"
    assert driver.name == "John Doe"
    assert driver.status == DriverStatus.OFFLINE
    
    driver_active = Driver("D002", "Jane Smith", DriverStatus.ACTIVE)
    assert driver_active.status == DriverStatus.ACTIVE


def test_driver_update_status():
    """Test updating driver status."""
    driver = Driver("D001", "John Doe", DriverStatus.OFFLINE)
    initial_time = driver.last_updated
    
    driver.update_status(DriverStatus.ACTIVE)
    assert driver.status == DriverStatus.ACTIVE
    assert driver.last_updated > initial_time


def test_driver_get_info():
    """Test getting driver information as dictionary."""
    driver = Driver("D001", "John Doe", DriverStatus.ACTIVE)
    info = driver.get_info()
    
    assert info["driver_id"] == "D001"
    assert info["name"] == "John Doe"
    assert info["status"] == "active"
    assert "last_updated" in info


def test_driver_repr():
    """Test driver string representation."""
    driver = Driver("D001", "John Doe", DriverStatus.ACTIVE)
    repr_str = repr(driver)
    
    assert "D001" in repr_str
    assert "John Doe" in repr_str
    assert "active" in repr_str
