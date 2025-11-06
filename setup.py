#!/usr/bin/env python3
"""
AIGo Programming Language - Setup Script

This setup.py provides backward compatibility with older Python packaging tools.
For modern installations, prefer using pyproject.toml.
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "AIGo Programming Language - AI-native language for high-performance computing"

# Core package information
setup(
    name="aigo-lang",
    version="1.0.0-beta",
    author="AIGo Development Team",
    author_email="dev@aigo.dev",
    description="AI-native programming language for high-performance computing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lekesiz/aigo",
    project_urls={
        "Bug Tracker": "https://github.com/lekesiz/aigo/issues",
        "Documentation": "https://github.com/lekesiz/aigo/wiki",
        "Source Code": "https://github.com/lekesiz/aigo",
    },

    # Package discovery
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},

    # Python version requirement
    python_requires=">=3.9",

    # Core dependencies (minimal)
    install_requires=[
        # No core dependencies - uses Python standard library
    ],

    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
            "bandit>=1.7.0",
            "safety>=2.3.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xdist>=3.0.0",
            "pytest-benchmark>=4.0.0",
        ],
        "perf": [
            "psutil>=5.9.0",
            "memory-profiler>=0.60.0",
        ],
    },

    # Entry points for CLI commands
    entry_points={
        "console_scripts": [
            "aigo=aigo.cli:main",
            "aigo-repl=aigo.cli:repl",
            "aigo-run=aigo.interpreter:run_from_cli",
        ],
    },

    # Package data
    package_data={
        "aigo": ["py.typed", "*.pyi"],
    },

    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],

    # License
    license="MIT",

    # Keywords
    keywords="aigo programming-language ai compiler interpreter",

    # Include additional files
    include_package_data=True,

    # Zip safe
    zip_safe=False,
)
