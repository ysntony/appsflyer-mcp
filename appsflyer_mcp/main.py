#!/usr/bin/env python3
"""
CLI entry point for the AppsFlyer MCP server.
"""

import asyncio
import sys
from pathlib import Path

# Add the package to the Python path
package_dir = Path(__file__).parent
sys.path.insert(0, str(package_dir.parent))

from appsflyer_mcp.server import mcp


def cli():
    """Run the MCP server."""
    try:
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli() 