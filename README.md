# VPN Detector

A simple, lightweight Python package to detect active VPN connections by examining network interface statistics.

## Features

- **Simple API**: Single function call to check VPN status
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Lightweight**: Minimal dependencies (only `psutil`)
- **Fast**: Quick network interface scanning

## Installation

### From PyPI (recommended)

```bash
pip install git 
```

### From Source

```bash
git clone https://github.com/yourusername/vpn_detector.git
cd vpn_detector
pip install .
```

## Usage

### Basic Usage

```python
from vpn_detector import VPNDetector, is_vpn_connected

# Method 1: Using the class
detector = VPNDetector()

# Check if any VPN is connected
if detector.is_vpn_connected():
    print("VPN is connected")
else:
    print("No VPN connection detected")

# Method 2: Using convenience function
if is_vpn_connected():
    print("VPN is connected")
```

### Multi-VPN Support

```python
from vpn_detector import (
    VPNDetector, get_vpn_interfaces, get_connected_vpn_interfaces, 
    get_vpn_status_summary
)

detector = VPNDetector()

# Get all VPN interfaces and their status
vpn_interfaces = detector.get_vpn_interfaces()
print(f"All VPNs: {vpn_interfaces}")
# Output: {'OpenVPN Client': True, 'WireGuard Tunnel': False}

# Get only connected VPN interfaces
connected_vpns = detector.get_connected_vpn_interfaces()
print(f"Connected VPNs: {connected_vpns}")
# Output: ['OpenVPN Client']

# Get comprehensive status summary
summary = detector.get_vpn_status_summary()
print(f"VPN Summary: {summary['connected_count']}/{summary['total_count']} connected")
# Output: VPN Summary: 1/2 connected

# Using convenience functions
vpn_interfaces = get_vpn_interfaces()
connected_vpns = get_connected_vpn_interfaces()
summary = get_vpn_status_summary()
```

### Advanced Usage

```python
import time
from vpn_detector import VPNDetector

detector = VPNDetector()

def monitor_vpn_status(interval=5):
    """Monitor VPN status continuously with detailed info."""
    while True:
        summary = detector.get_vpn_status_summary()
        
        if summary['has_vpn_connected']:
            vpn_names = ', '.join(summary['connected_vpns'])
            print(f"VPN Status: {summary['connected_count']} Connected ({vpn_names})")
        else:
            print("VPN Status: Disconnected")
            
        time.sleep(interval)

# Monitor VPN status every 5 seconds
monitor_vpn_status()
```

## How It Works

The package works by:

1. Scanning all network interfaces using `psutil`
2. Looking for interfaces with "vpn" in their name (case-insensitive)
3. Checking if any such interfaces are currently active (up)
4. Returning `True` if an active VPN interface is found, `False` otherwise

## Requirements

- Python 3.7+
- psutil >= 5.0.0

## Limitations

- Detection is based on interface naming conventions
- May not detect all VPN types (especially those that don't include "vpn" in the interface name)
- Some VPN clients may use different naming schemes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 1.0.0
- Initial release
- Basic VPN detection functionality
- Cross-platform support
