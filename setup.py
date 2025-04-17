from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Package data directories
package_data_dirs = ['data']

# Find all package data files
package_data_files = []
for data_dir in package_data_dirs:
    for root, dirs, files in os.walk(os.path.join('cashflow_tracker', data_dir)):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, 'cashflow_tracker')
            package_data_files.append(rel_path)

setup(
    name="cashflow_tracker",
    version="0.1.0",
    author="Michael Foldyna",
    author_email="michael.foldyna@outlook.com",
    description="A comprehensive cashflow tracking and visualization system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micfold/cashflow_tracker",
    project_urls={
        "Bug Tracker": "https://github.com/micfold/cashflow_tracker/issues",
        "Documentation": "https://github.com/micfold/cashflow_tracker/docs",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={
        "cashflow_tracker": package_data_files,
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "cashflow-tracker=cashflow_tracker.cli:main",
        ],
    },
)