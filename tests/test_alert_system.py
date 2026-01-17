"""
Test suite for the AlertSystem module.
"""

import unittest
import time
from dms.alert_system import AlertSystem, AlertType, AlertLevel


class TestAlertSystem(unittest.TestCase):
    """Test cases for AlertSystem."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.alert_system = AlertSystem(cooldown_period=1.0)
    
    def test_initialization(self):
        """Test alert system initialization."""
        self.assertIsNotNone(self.alert_system)
        self.assertEqual(len(self.alert_system.active_alerts), 0)
        self.assertEqual(len(self.alert_system.alert_history), 0)
    
    def test_trigger_alert(self):
        """Test triggering an alert."""
        alert = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert['type'], 'drowsiness')
        self.assertEqual(alert['level'], 'WARNING')
        self.assertIn('message', alert)
        self.assertIn('timestamp', alert)
    
    def test_alert_cooldown(self):
        """Test alert cooldown period."""
        # Trigger first alert
        alert1 = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        self.assertIsNotNone(alert1)
        
        # Try to trigger same alert immediately (should be blocked)
        alert2 = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        self.assertIsNone(alert2)
        
        # Wait for cooldown period
        time.sleep(1.1)
        
        # Should be able to trigger again
        alert3 = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        self.assertIsNotNone(alert3)
    
    def test_multiple_alert_types(self):
        """Test triggering different alert types."""
        alert1 = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        alert2 = self.alert_system.trigger_alert(
            AlertType.DISTRACTION,
            AlertLevel.WARNING
        )
        
        self.assertIsNotNone(alert1)
        self.assertIsNotNone(alert2)
        self.assertEqual(len(self.alert_system.alert_history), 2)
    
    def test_alert_levels(self):
        """Test different alert levels."""
        # Test INFO level
        alert_info = self.alert_system.trigger_alert(
            AlertType.YAWNING,
            AlertLevel.INFO
        )
        self.assertEqual(alert_info['level'], 'INFO')
        
        time.sleep(1.1)
        
        # Test CRITICAL level
        alert_critical = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.CRITICAL
        )
        self.assertEqual(alert_critical['level'], 'CRITICAL')
    
    def test_custom_message(self):
        """Test alert with custom message."""
        custom_msg = "Custom alert message"
        alert = self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING,
            message=custom_msg
        )
        
        self.assertEqual(alert['message'], custom_msg)
    
    def test_active_alerts(self):
        """Test active alerts tracking."""
        self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        
        active = self.alert_system.get_active_alerts()
        self.assertEqual(len(active), 1)
        self.assertIn(AlertType.DROWSINESS, active)
    
    def test_clear_alert(self):
        """Test clearing an alert."""
        self.alert_system.trigger_alert(
            AlertType.DROWSINESS,
            AlertLevel.WARNING
        )
        
        self.assertEqual(len(self.alert_system.get_active_alerts()), 1)
        
        self.alert_system.clear_alert(AlertType.DROWSINESS)
        
        self.assertEqual(len(self.alert_system.get_active_alerts()), 0)
    
    def test_alert_history(self):
        """Test alert history tracking."""
        # Trigger multiple alerts
        self.alert_system.trigger_alert(AlertType.DROWSINESS, AlertLevel.WARNING)
        time.sleep(1.1)
        self.alert_system.trigger_alert(AlertType.DISTRACTION, AlertLevel.WARNING)
        time.sleep(1.1)
        self.alert_system.trigger_alert(AlertType.YAWNING, AlertLevel.INFO)
        
        history = self.alert_system.get_alert_history()
        self.assertEqual(len(history), 3)
    
    def test_alert_history_limit(self):
        """Test alert history with limit."""
        # Trigger many alerts
        for i in range(15):
            self.alert_system.trigger_alert(AlertType.YAWNING, AlertLevel.INFO)
            time.sleep(1.1)
        
        # Get last 10
        history = self.alert_system.get_alert_history(last_n=10)
        self.assertEqual(len(history), 10)
    
    def test_alert_statistics(self):
        """Test alert statistics."""
        self.alert_system.trigger_alert(AlertType.DROWSINESS, AlertLevel.WARNING)
        time.sleep(1.1)
        self.alert_system.trigger_alert(AlertType.DROWSINESS, AlertLevel.CRITICAL)
        time.sleep(1.1)
        self.alert_system.trigger_alert(AlertType.DISTRACTION, AlertLevel.WARNING)
        
        stats = self.alert_system.get_alert_stats()
        
        self.assertEqual(stats['total_alerts'], 3)
        self.assertEqual(stats['by_type']['drowsiness'], 2)
        self.assertEqual(stats['by_type']['distraction'], 1)
        self.assertEqual(stats['by_level']['WARNING'], 2)
        self.assertEqual(stats['by_level']['CRITICAL'], 1)
    
    def test_reset(self):
        """Test alert system reset."""
        # Trigger some alerts
        self.alert_system.trigger_alert(AlertType.DROWSINESS, AlertLevel.WARNING)
        time.sleep(1.1)
        self.alert_system.trigger_alert(AlertType.DISTRACTION, AlertLevel.WARNING)
        
        # Reset
        self.alert_system.reset()
        
        # Check state is reset
        self.assertEqual(len(self.alert_system.alert_history), 0)
        self.assertEqual(len(self.alert_system.active_alerts), 0)
        self.assertEqual(len(self.alert_system.last_alert_time), 0)


if __name__ == '__main__':
    unittest.main()
