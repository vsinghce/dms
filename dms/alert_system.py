"""
Alert System Module
Manages alerts and warnings for the driver monitoring system.
"""

import time
from enum import Enum


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = 1
    WARNING = 2
    CRITICAL = 3


class AlertType(Enum):
    """Types of alerts."""
    DROWSINESS = "drowsiness"
    DISTRACTION = "distraction"
    PHONE_USAGE = "phone_usage"
    YAWNING = "yawning"


class AlertSystem:
    """Manages alerts and notifications for driver monitoring."""
    
    def __init__(self, cooldown_period=5.0):
        """
        Initialize the alert system.
        
        Args:
            cooldown_period: Minimum time (seconds) between repeated alerts
        """
        self.cooldown_period = cooldown_period
        self.last_alert_time = {}
        self.alert_history = []
        self.active_alerts = set()
        
    def trigger_alert(self, alert_type, alert_level, message=None):
        """
        Trigger an alert if not in cooldown period.
        
        Args:
            alert_type: Type of alert (AlertType enum)
            alert_level: Severity level (AlertLevel enum)
            message: Optional custom alert message
            
        Returns:
            dict: Alert information if triggered, None if in cooldown
        """
        current_time = time.time()
        alert_key = f"{alert_type.value}"
        
        # Check cooldown
        if alert_key in self.last_alert_time:
            time_since_last = current_time - self.last_alert_time[alert_key]
            if time_since_last < self.cooldown_period:
                return None
        
        # Generate alert
        alert = {
            "type": alert_type.value,
            "level": alert_level.name,
            "message": message or self._get_default_message(alert_type, alert_level),
            "timestamp": current_time
        }
        
        # Update state
        self.last_alert_time[alert_key] = current_time
        self.alert_history.append(alert)
        self.active_alerts.add(alert_type)
        
        # Trigger appropriate alert mechanism
        self._dispatch_alert(alert)
        
        return alert
    
    def clear_alert(self, alert_type):
        """
        Clear an active alert.
        
        Args:
            alert_type: Type of alert to clear
        """
        if alert_type in self.active_alerts:
            self.active_alerts.remove(alert_type)
    
    def _get_default_message(self, alert_type, alert_level):
        """
        Get default message for alert type and level.
        
        Args:
            alert_type: Type of alert
            alert_level: Severity level
            
        Returns:
            str: Default alert message
        """
        messages = {
            AlertType.DROWSINESS: {
                AlertLevel.WARNING: "Driver appears drowsy. Please take a break.",
                AlertLevel.CRITICAL: "CRITICAL: Driver drowsiness detected! Pull over safely."
            },
            AlertType.DISTRACTION: {
                AlertLevel.WARNING: "Driver distraction detected. Focus on the road.",
                AlertLevel.CRITICAL: "CRITICAL: Prolonged distraction detected!"
            },
            AlertType.PHONE_USAGE: {
                AlertLevel.WARNING: "Phone usage detected. Keep hands on wheel.",
                AlertLevel.CRITICAL: "CRITICAL: Stop phone usage while driving!"
            },
            AlertType.YAWNING: {
                AlertLevel.INFO: "Frequent yawning detected. Consider taking a break.",
                AlertLevel.WARNING: "Multiple yawns detected. Rest recommended."
            }
        }
        
        return messages.get(alert_type, {}).get(
            alert_level, 
            f"{alert_level.name}: {alert_type.value}"
        )
    
    def _dispatch_alert(self, alert):
        """
        Dispatch alert through appropriate channels.
        
        Args:
            alert: Alert dictionary with type, level, and message
        """
        # In a real system, this would:
        # - Play audio warnings
        # - Display visual alerts on dashboard
        # - Send haptic feedback through steering wheel
        # - Log to vehicle system
        
        # For now, just print to console
        level_symbol = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "CRITICAL": "🚨"
        }
        
        symbol = level_symbol.get(alert["level"], "•")
        print(f"\n{symbol} [{alert['level']}] {alert['type'].upper()}")
        print(f"   {alert['message']}")
    
    def get_active_alerts(self):
        """
        Get list of currently active alerts.
        
        Returns:
            list: Active alert types
        """
        return list(self.active_alerts)
    
    def get_alert_history(self, last_n=10):
        """
        Get recent alert history.
        
        Args:
            last_n: Number of recent alerts to return
            
        Returns:
            list: Recent alerts
        """
        return self.alert_history[-last_n:]
    
    def get_alert_stats(self):
        """
        Get statistics about alerts.
        
        Returns:
            dict: Alert statistics
        """
        stats = {
            "total_alerts": len(self.alert_history),
            "active_alerts": len(self.active_alerts),
            "by_type": {},
            "by_level": {}
        }
        
        for alert in self.alert_history:
            alert_type = alert["type"]
            alert_level = alert["level"]
            
            stats["by_type"][alert_type] = stats["by_type"].get(alert_type, 0) + 1
            stats["by_level"][alert_level] = stats["by_level"].get(alert_level, 0) + 1
        
        return stats
    
    def reset(self):
        """Reset the alert system state."""
        self.last_alert_time.clear()
        self.alert_history.clear()
        self.active_alerts.clear()
