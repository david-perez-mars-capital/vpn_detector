"""
VPN detection functionality.

This module provides functions to detect active VPN connections by examining
network interface statistics.
"""

import psutil
from typing import Dict, List


class VPNDetector:
    """
    VPN Detector class for handling single and multiple VPN connections.
    """

    def get_vpn_interfaces(self) -> Dict[str, bool]:
        """
        Get all VPN interfaces and their connection status.

        Returns:
            Dict[str, bool]: Dictionary mapping VPN interface names to their status
                           (True if connected/up, False if disconnected/down).

        Example:
            >>> detector = VPNDetector()
            >>> vpn_interfaces = detector.get_vpn_interfaces()
            >>> print(vpn_interfaces)
            {'OpenVPN Client': True, 'WireGuard Tunnel': False}
        """
        vpn_interfaces = {}
        stats = psutil.net_if_stats()

        for interface_name, interface_stats in stats.items():
            if "vpn" in interface_name.lower():
                vpn_interfaces[interface_name] = interface_stats.isup

        return vpn_interfaces

    def get_connected_vpn_interfaces(self) -> List[str]:
        """
        Get a list of currently connected VPN interface names.

        Returns:
            List[str]: List of VPN interface names that are currently active/connected.
                      Empty list if no VPN connections are active.

        Example:
            >>> detector = VPNDetector()
            >>> connected_vpns = detector.get_connected_vpn_interfaces()
            >>> print(f"Connected VPNs: {connected_vpns}")
            Connected VPNs: ['OpenVPN Client', 'WireGuard Tunnel']
        """
        vpn_interfaces = self.get_vpn_interfaces()
        return [name for name, is_connected in vpn_interfaces.items() if is_connected]

    def is_vpn_connected(self) -> bool:
        """
        Check if any VPN connection is currently active.

        This function examines network interface statistics to determine if any
        interface with 'vpn' in its name is currently up and running.

        Returns:
            bool: True if at least one VPN connection is detected as active, False otherwise.

        Example:
            >>> from vpn_detector import is_vpn_connected
            >>> if is_vpn_connected():
            ...     print("VPN is connected")
            ... else:
            ...     print("No VPN connection detected")
        """
        return len(self.get_connected_vpn_interfaces()) > 0

    def get_vpn_status_summary(self) -> Dict[str, any]:
        """
        Get a comprehensive summary of VPN status.

        Returns:
            Dict[str, any]: Summary containing:
                - 'has_vpn_connected': bool - True if any VPN is connected
                - 'connected_count': int - Number of connected VPNs
                - 'total_count': int - Total number of VPN interfaces found
                - 'connected_vpns': List[str] - Names of connected VPN interfaces
                - 'all_vpns': Dict[str, bool] - All VPN interfaces and their status

        Example:
            >>> detector = VPNDetector()
            >>> summary = detector.get_vpn_status_summary()
            >>> print(f"Connected VPNs: {summary['connected_count']}/{summary['total_count']}")
        """
        all_vpns = self.get_vpn_interfaces()
        connected_vpns = self.get_connected_vpn_interfaces()

        return {
            "has_vpn_connected": len(connected_vpns) > 0,
            "connected_count": len(connected_vpns),
            "total_count": len(all_vpns),
            "connected_vpns": connected_vpns,
            "all_vpns": all_vpns,
        }
