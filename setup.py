#!/usr/bin/env python3
"""
Setup script for appsflyer-mcp.
"""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="appsflyer-mcp",
        version="0.1.0",
        packages=find_packages(),
        install_requires=[
            "httpx>=0.28.1",
            "mcp[cli]>=1.12.3",
            "python-dotenv>=1.1.1",
            "pydantic>=2.0.0",
        ],
        entry_points={
            "console_scripts": [
                "appsflyer-mcp=appsflyer_mcp.main:cli",
            ],
        },
        python_requires=">=3.10",
    ) 