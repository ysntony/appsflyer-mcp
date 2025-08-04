"""
Main entry point for running appsflyer_mcp as a module.
This allows running: python -m appsflyer_mcp
"""

from .server import main

if __name__ == "__main__":
    main()