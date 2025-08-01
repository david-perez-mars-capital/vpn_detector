#!/usr/bin/env python3
"""
Simple test script for VPN detector package.
"""

import sys
import os

# Add the package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vpn_detector import (
    VPNDetector,
    is_vpn_connected,
    get_vpn_interfaces,
    get_connected_vpn_interfaces,
    get_vpn_status_summary,
)


def test_vpn_detector():
    """Test the VPN detector functionality."""
    print("Testing VPN Detector Package")
    print("=" * 50)

    # Test class-based approach
    print("\n1. Testing VPNDetector class:")
    detector = VPNDetector()

    try:
        result = detector.is_vpn_connected()
        print(f"   VPN Status (class): {'Connected' if result else 'Not Connected'}")
        print("   ✓ VPNDetector class works correctly")
    except Exception as e:
        print(f"   ✗ Error with VPNDetector class: {e}")
        return False

    # Test convenience function
    print("\n2. Testing convenience function:")
    try:
        result = is_vpn_connected()
        print(f"   VPN Status (function): {'Connected' if result else 'Not Connected'}")
        print("   ✓ Convenience function works correctly")
    except Exception as e:
        print(f"   ✗ Error with convenience function: {e}")
        return False

    # Test multi-VPN functionality
    print("\n3. Testing multi-VPN functionality:")
    try:
        # Test get_vpn_interfaces
        vpn_interfaces = get_vpn_interfaces()
        print(f"   All VPN interfaces: {vpn_interfaces}")

        # Test get_connected_vpn_interfaces
        connected_vpns = get_connected_vpn_interfaces()
        print(f"   Connected VPNs: {connected_vpns}")

        # Test get_vpn_status_summary
        summary = get_vpn_status_summary()
        print(f"   VPN Summary:")
        print(f"     - Total VPNs found: {summary['total_count']}")
        print(f"     - Connected VPNs: {summary['connected_count']}")
        print(f"     - Any VPN connected: {summary['has_vpn_connected']}")
        if summary["connected_vpns"]:
            print(f"     - Connected VPN names: {', '.join(summary['connected_vpns'])}")

        print("   ✓ Multi-VPN functionality works correctly")
    except Exception as e:
        print(f"   ✗ Error with multi-VPN functionality: {e}")
        return False

    # Test network interfaces inspection
    print("\n4. Network interfaces inspection:")
    try:
        import psutil

        stats = psutil.net_if_stats()

        print("   Available network interfaces:")
        for interface, stat in stats.items():
            status = "UP" if stat.isup else "DOWN"
            vpn_indicator = " (VPN?)" if "vpn" in interface.lower() else ""
            print(f"     - {interface}: {status}{vpn_indicator}")

        print("   ✓ Network interface inspection works")
    except Exception as e:
        print(f"   ✗ Error inspecting network interfaces: {e}")
        return False

    print("\n" + "=" * 50)
    print("All tests completed successfully! ✓")
    return True


if __name__ == "__main__":
    success = test_vpn_detector()
    sys.exit(0 if success else 1)
