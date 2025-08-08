#!/usr/bin/env python3
"""
Setup script for TempDataset Library.
This file provides backward compatibility for older pip versions.
The main configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
import os

# Read version from package
def get_version():
    """Extract version from package __init__.py."""
    version_file = os.path.join(os.path.dirname(__file__), 'tempdataset', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return "0.1.0"

# Read README for long description
def read_readme():
    """Read README.md for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A lightweight Python library for generating realistic temporary datasets for testing and development."

# Fallback setup for older pip versions
setup(
    name="tempdataset",
    version=get_version(),
    author="TempDataset Contributors",
    author_email="saqibshaikhdz@gmail.com",
    description="A lightweight Python library for generating realistic temporary datasets",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dot-css/TempDataset",
    packages=find_packages(exclude=["tests", "tests.*", ".benchmarks", ".benchmarks.*"]),
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "faker": ["faker>=18.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "memory-profiler>=0.60.0",
            "psutil>=5.9.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "memory-profiler>=0.60.0",
            "psutil>=5.9.0",
        ],
        "performance": [
            "memory-profiler>=0.60.0",
            "psutil>=5.9.0",
            "pytest-benchmark>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tempdataset=tempdataset.cli:main",
        ],
    },
    keywords=[
        "dataset", "testing", "development", "sample-data", "mock-data",
        "csv", "json", "sales-data", "temporary", "lightweight"
    ],
    include_package_data=True,
    package_data={
        "tempdataset": ["py.typed"],
    },
    project_urls={
        "Bug Tracker": "https://github.com/dot-css/TempDataset/issues",
        "Documentation": "https://tempdataset.readthedocs.io/",
        "Source Code": "https://github.com/dot-css/TempDataset",
    },
)