"""
Example usage of the Driver Monitoring System.

This script demonstrates basic functionality including:
- Creating a monitoring system
- Adding drivers
- Updating statuses
- Querying driver information
"""

from dms import DriverMonitor, Driver, DriverStatus


def main():
    # Create a new monitoring system
    print("=== Driver Monitoring System Demo ===\n")
    monitor = DriverMonitor()
    
    # Add some drivers
    print("Adding drivers...")
    drivers = [
        Driver("D001", "John Doe", DriverStatus.ACTIVE),
        Driver("D002", "Jane Smith", DriverStatus.ACTIVE),
        Driver("D003", "Bob Johnson", DriverStatus.OFFLINE),
        Driver("D004", "Alice Williams", DriverStatus.ON_BREAK),
        Driver("D005", "Charlie Brown", DriverStatus.INACTIVE),
    ]
    
    for driver in drivers:
        monitor.add_driver(driver)
        print(f"  Added: {driver}")
    
    # Get summary
    print("\n--- System Summary ---")
    summary = monitor.get_summary()
    print(f"Total drivers: {summary['total_drivers']}")
    print("Drivers by status:")
    for status, count in summary['by_status'].items():
        print(f"  {status}: {count}")
    
    # Get active drivers
    print("\n--- Active Drivers ---")
    active_drivers = monitor.get_drivers_by_status(DriverStatus.ACTIVE)
    for driver in active_drivers:
        print(f"  {driver.name} (ID: {driver.driver_id})")
    
    # Update a driver's status
    print("\n--- Updating Driver Status ---")
    print("Setting D001 (John Doe) to ON_BREAK...")
    monitor.update_driver_status("D001", DriverStatus.ON_BREAK)
    
    # Get updated driver info
    driver = monitor.get_driver("D001")
    print(f"Updated info: {driver.get_info()}")
    
    # Get new active driver count
    print(f"\nActive drivers now: {monitor.get_active_drivers_count()}")
    
    # Get all drivers
    print("\n--- All Drivers ---")
    all_drivers = monitor.get_all_drivers()
    for driver in all_drivers:
        info = driver.get_info()
        print(f"  {info['name']} - Status: {info['status']}")


if __name__ == "__main__":
    main()
