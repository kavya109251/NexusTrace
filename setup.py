from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nexustrace",
    version="1.0.0",
    author="NexusTrace Development Team",
    author_email="dev@nexustrace.com",
    description="Advanced Memory Forensics Analysis Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexustrace/nexustrace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Topic :: Security",
        "Topic :: System :: Forensics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core web framework
        "Flask",
        "Werkzeug",
        
        # Database
        "sqlite3",  # Usually built-in with Python
        
        # Security
        "bcrypt",
        "cryptography",
        
        # File handling
        "pathlib2",
        "magic",
        
        # Data processing
        "pandas",
        "numpy",
        
        # JSON/XML processing
        "lxml",
        "xmltodict",
        
        # Forensic analysis
        "volatility3",
        "yara-python",
        
        # Network analysis
        "requests",
        "urllib3",
        
        # Time/Date handling
        "python-dateutil",
        
        # System utilities
        "psutil",
        "hashlib",  # Usually built-in
        
        # Async support
        "asyncio",  # Usually built-in with Python 3.7+
        
        # Logging
        "coloredlogs",
        
        # Configuration
        "configparser",
        
        # Export formats
        "openpyxl",
        "reportlab",
        
        # Development utilities
        "pathlib",
        "uuid",  # Usually built-in
        "typing-extensions",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "pre-commit",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
        "performance": [
            "cython",
            "numba",
        ],
    },
    entry_points={
        "console_scripts": [
            "nexustrace=web.app:main",
            "nexustrace-cli=cli.main:main",
            "nexustrace-setup=scripts.setup_db:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nexustrace": [
            "web/templates/*.html",
            "web/static/css/*.css",
            "web/static/js/*.js",
            "config/*.json",
            "yara_rules/*.yar",
            "yara_rules/**/*.yar",
        ],
    },
    zip_safe=False,
    keywords="forensics, memory-analysis, incident-response, malware-analysis, volatility, yara",
    project_urls={
        "Bug Reports": "https://github.com/nexustrace/nexustrace/issues",
        "Documentation": "https://nexustrace.readthedocs.io/",
        "Source": "https://github.com/nexustrace/nexustrace",
    },
)
