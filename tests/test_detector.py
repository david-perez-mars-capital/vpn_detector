"""
Tests for VPN detector functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
from vpn_detector import (
    VPNDetector,
    is_vpn_connected,
    get_vpn_interfaces,
    get_connected_vpn_interfaces,
    get_vpn_status_summary,
)


class TestVPNDetector(unittest.TestCase):
    """Test cases for VPNDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = VPNDetector()

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_vpn_connected_with_vpn_interface(self, mock_net_if_stats):
        """Test VPN detection when VPN interface is present and up."""
        # Mock network interface stats with a VPN interface that is up
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "vpn0": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.is_vpn_connected()
        self.assertTrue(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_vpn_connected_with_vpn_interface_down(self, mock_net_if_stats):
        """Test VPN detection when VPN interface is present but down."""
        # Mock network interface stats with a VPN interface that is down
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "vpn0": MagicMock(isup=False),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.is_vpn_connected()
        self.assertFalse(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_vpn_not_connected_no_vpn_interface(self, mock_net_if_stats):
        """Test VPN detection when no VPN interface is present."""
        # Mock network interface stats without VPN interface
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "wlan0": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.is_vpn_connected()
        self.assertFalse(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_vpn_case_insensitive(self, mock_net_if_stats):
        """Test VPN detection is case insensitive."""
        # Mock network interface stats with uppercase VPN interface
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "VPN-Connection": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.is_vpn_connected()
        self.assertTrue(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_multiple_vpn_interfaces(self, mock_net_if_stats):
        """Test VPN detection with multiple VPN interfaces."""
        # Mock network interface stats with multiple VPN interfaces
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "vpn0": MagicMock(isup=False),
            "vpn1": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.is_vpn_connected()
        self.assertTrue(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_empty_interfaces(self, mock_net_if_stats):
        """Test VPN detection with no network interfaces."""
        mock_net_if_stats.return_value = {}

        result = self.detector.is_vpn_connected()
        self.assertFalse(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_get_vpn_interfaces(self, mock_net_if_stats):
        """Test getting all VPN interfaces with their status."""
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "OpenVPN Client": MagicMock(isup=True),
            "NordVPN Tunnel": MagicMock(isup=False),
            "vpn-corporate": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.get_vpn_interfaces()
        expected = {
            "OpenVPN Client": True,
            "NordVPN Tunnel": False,
            "vpn-corporate": True,
        }
        self.assertEqual(result, expected)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_get_connected_vpn_interfaces(self, mock_net_if_stats):
        """Test getting only connected VPN interfaces."""
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "OpenVPN Client": MagicMock(isup=True),
            "NordVPN Tunnel": MagicMock(isup=False),
            "vpn-corporate": MagicMock(isup=True),
            "vpn-personal": MagicMock(isup=False),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.get_connected_vpn_interfaces()
        expected = ["OpenVPN Client", "vpn-corporate"]
        self.assertEqual(sorted(result), sorted(expected))

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_get_vpn_status_summary(self, mock_net_if_stats):
        """Test getting comprehensive VPN status summary."""
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "OpenVPN Client": MagicMock(isup=True),
            "NordVPN Tunnel": MagicMock(isup=False),
            "vpn-corporate": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.get_vpn_status_summary()

        self.assertTrue(result["has_vpn_connected"])
        self.assertEqual(result["connected_count"], 2)
        self.assertEqual(result["total_count"], 3)
        self.assertEqual(
            sorted(result["connected_vpns"]),
            sorted(["OpenVPN Client", "vpn-corporate"]),
        )
        self.assertEqual(len(result["all_vpns"]), 3)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_no_vpn_interfaces_summary(self, mock_net_if_stats):
        """Test summary when no VPN interfaces exist."""
        mock_stats = {
            "eth0": MagicMock(isup=True),
            "wlan0": MagicMock(isup=True),
            "lo": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = self.detector.get_vpn_status_summary()

        self.assertFalse(result["has_vpn_connected"])
        self.assertEqual(result["connected_count"], 0)
        self.assertEqual(result["total_count"], 0)
        self.assertEqual(result["connected_vpns"], [])
        self.assertEqual(result["all_vpns"], {})


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for the convenience functions."""

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_convenience_function_vpn_connected(self, mock_net_if_stats):
        """Test convenience function when VPN is connected."""
        mock_stats = {"vpn0": MagicMock(isup=True)}
        mock_net_if_stats.return_value = mock_stats

        result = is_vpn_connected()
        self.assertTrue(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_convenience_function_vpn_not_connected(self, mock_net_if_stats):
        """Test convenience function when VPN is not connected."""
        mock_stats = {"eth0": MagicMock(isup=True)}
        mock_net_if_stats.return_value = mock_stats

        result = is_vpn_connected()
        self.assertFalse(result)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_convenience_get_vpn_interfaces(self, mock_net_if_stats):
        """Test convenience function for getting VPN interfaces."""
        mock_stats = {
            "OpenVPN Client": MagicMock(isup=True),
            "vpn-tunnel": MagicMock(isup=False),
            "eth0": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = get_vpn_interfaces()
        expected = {"OpenVPN Client": True, "vpn-tunnel": False}
        self.assertEqual(result, expected)

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_convenience_get_connected_vpn_interfaces(self, mock_net_if_stats):
        """Test convenience function for getting connected VPN interfaces."""
        mock_stats = {
            "OpenVPN Client": MagicMock(isup=True),
            "vpn-tunnel": MagicMock(isup=False),
            "NordVPN": MagicMock(isup=True),
            "eth0": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = get_connected_vpn_interfaces()
        expected = ["OpenVPN Client", "NordVPN"]
        self.assertEqual(sorted(result), sorted(expected))

    @patch("vpn_detector.detector.psutil.net_if_stats")
    def test_convenience_get_vpn_status_summary(self, mock_net_if_stats):
        """Test convenience function for getting VPN status summary."""
        mock_stats = {
            "OpenVPN Client": MagicMock(isup=True),
            "vpn-tunnel": MagicMock(isup=False),
            "eth0": MagicMock(isup=True),
        }
        mock_net_if_stats.return_value = mock_stats

        result = get_vpn_status_summary()

        self.assertTrue(result["has_vpn_connected"])
        self.assertEqual(result["connected_count"], 1)
        self.assertEqual(result["total_count"], 2)


if __name__ == "__main__":
    unittest.main()
