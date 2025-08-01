"""
Setup configuration for vpn_detector package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vpn-detector",
    version="0.0.1",
    author="David Perez",
    description="A simple Python package to detect active VPN connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david-perez-marscapital/vpn_detector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.0.0",
    ],
    keywords="vpn, network, detection, connection, monitoring",
    project_urls={
        "Bug Reports": "https://github.com/david-perez-marscapital/vpn_detector/issues",
        "Source": "https://github.com/david-perez-marscapital/vpn_detector",
    },
)