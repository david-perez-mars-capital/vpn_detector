"""
VPN Detector - A simple Python package to detect active VPN connections.
"""

from .detector import VPNDetector

__version__ = "1.0.0"

# Create a convenience function for backward compatibility
_detector = VPNDetector()
is_vpn_connected = _detector.is_vpn_connected

# Export additional convenience functions for multi-VPN scenarios
get_vpn_interfaces = _detector.get_vpn_interfaces
get_connected_vpn_interfaces = _detector.get_connected_vpn_interfaces
get_vpn_status_summary = _detector.get_vpn_status_summary

__all__ = [
    "VPNDetector", 
    "is_vpn_connected",
    "get_vpn_interfaces",
    "get_connected_vpn_interfaces", 
    "get_vpn_status_summary"
]