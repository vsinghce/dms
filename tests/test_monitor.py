"""
Unit tests for the DriverMonitor class.
"""

import pytest
from dms import DriverMonitor, Driver, DriverStatus


def test_monitor_initialization():
    """Test monitor initialization."""
    monitor = DriverMonitor()
    assert len(monitor.drivers) == 0


def test_add_driver():
    """Test adding drivers to the monitor."""
    monitor = DriverMonitor()
    driver = Driver("D001", "John Doe")
    
    monitor.add_driver(driver)
    assert len(monitor.drivers) == 1
    assert "D001" in monitor.drivers


def test_add_duplicate_driver():
    """Test that adding duplicate driver raises error."""
    monitor = DriverMonitor()
    driver1 = Driver("D001", "John Doe")
    driver2 = Driver("D001", "Jane Smith")
    
    monitor.add_driver(driver1)
    with pytest.raises(ValueError):
        monitor.add_driver(driver2)


def test_remove_driver():
    """Test removing a driver from the monitor."""
    monitor = DriverMonitor()
    driver = Driver("D001", "John Doe")
    
    monitor.add_driver(driver)
    monitor.remove_driver("D001")
    assert len(monitor.drivers) == 0


def test_remove_nonexistent_driver():
    """Test that removing non-existent driver raises error."""
    monitor = DriverMonitor()
    
    with pytest.raises(KeyError):
        monitor.remove_driver("D999")


def test_get_driver():
    """Test getting a driver by ID."""
    monitor = DriverMonitor()
    driver = Driver("D001", "John Doe")
    
    monitor.add_driver(driver)
    retrieved = monitor.get_driver("D001")
    
    assert retrieved is not None
    assert retrieved.driver_id == "D001"
    assert monitor.get_driver("D999") is None


def test_update_driver_status():
    """Test updating driver status through monitor."""
    monitor = DriverMonitor()
    driver = Driver("D001", "John Doe", DriverStatus.OFFLINE)
    
    monitor.add_driver(driver)
    monitor.update_driver_status("D001", DriverStatus.ACTIVE)
    
    assert monitor.get_driver("D001").status == DriverStatus.ACTIVE


def test_update_nonexistent_driver_status():
    """Test that updating non-existent driver raises error."""
    monitor = DriverMonitor()
    
    with pytest.raises(KeyError):
        monitor.update_driver_status("D999", DriverStatus.ACTIVE)


def test_get_all_drivers():
    """Test getting all drivers."""
    monitor = DriverMonitor()
    driver1 = Driver("D001", "John Doe")
    driver2 = Driver("D002", "Jane Smith")
    
    monitor.add_driver(driver1)
    monitor.add_driver(driver2)
    
    all_drivers = monitor.get_all_drivers()
    assert len(all_drivers) == 2


def test_get_drivers_by_status():
    """Test filtering drivers by status."""
    monitor = DriverMonitor()
    driver1 = Driver("D001", "John Doe", DriverStatus.ACTIVE)
    driver2 = Driver("D002", "Jane Smith", DriverStatus.OFFLINE)
    driver3 = Driver("D003", "Bob Johnson", DriverStatus.ACTIVE)
    
    monitor.add_driver(driver1)
    monitor.add_driver(driver2)
    monitor.add_driver(driver3)
    
    active_drivers = monitor.get_drivers_by_status(DriverStatus.ACTIVE)
    assert len(active_drivers) == 2
    
    offline_drivers = monitor.get_drivers_by_status(DriverStatus.OFFLINE)
    assert len(offline_drivers) == 1


def test_get_active_drivers_count():
    """Test getting count of active drivers."""
    monitor = DriverMonitor()
    driver1 = Driver("D001", "John Doe", DriverStatus.ACTIVE)
    driver2 = Driver("D002", "Jane Smith", DriverStatus.OFFLINE)
    driver3 = Driver("D003", "Bob Johnson", DriverStatus.ACTIVE)
    
    monitor.add_driver(driver1)
    monitor.add_driver(driver2)
    monitor.add_driver(driver3)
    
    assert monitor.get_active_drivers_count() == 2


def test_get_summary():
    """Test getting summary report."""
    monitor = DriverMonitor()
    driver1 = Driver("D001", "John Doe", DriverStatus.ACTIVE)
    driver2 = Driver("D002", "Jane Smith", DriverStatus.OFFLINE)
    driver3 = Driver("D003", "Bob Johnson", DriverStatus.ON_BREAK)
    
    monitor.add_driver(driver1)
    monitor.add_driver(driver2)
    monitor.add_driver(driver3)
    
    summary = monitor.get_summary()
    
    assert summary["total_drivers"] == 3
    assert summary["by_status"]["active"] == 1
    assert summary["by_status"]["offline"] == 1
    assert summary["by_status"]["on_break"] == 1
    assert summary["by_status"]["inactive"] == 0
