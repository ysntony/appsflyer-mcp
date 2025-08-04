#!/usr/bin/env python3
"""
Standalone AppsFlyer MCP server script for Cursor.
This script directly runs the MCP server without module imports.
"""

import os
import sys
import asyncio
import httpx
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import FastMCP from official MCP package
from mcp.server.fastmcp import FastMCP

# Server configuration
AF_API_BASE_URL = os.getenv("APPSFLYER_API_BASE_URL", "https://hq1.appsflyer.com")
AF_TOKEN = os.getenv("APPSFLYER_TOKEN")

# Create MCP server
mcp = FastMCP("appsflyer")

# Define input model
class AggregateDataInput(BaseModel):
    app_id: str = Field(..., description="The ID of the AppsFlyer app.")
    from_date: date = Field(..., description="The start date of the data range (YYYY-MM-DD).")
    to_date: date = Field(..., description="The end date of the data range (YYYY-MM-DD).")
    report_type: Literal[
        "partners_report",
        "partners_by_date_report", 
        "daily_report",
        "geo_report",
        "geo_by_date_report"
    ] = Field("daily_report", description="The type of aggregate report to fetch.")

@mcp.tool()
async def get_aggregate_data(data: AggregateDataInput):
    """Fetches aggregate data reports from the AppsFlyer Pull API."""
    if not AF_API_BASE_URL or not AF_TOKEN:
        return "Error: AppsFlyer API credentials not configured."

    endpoint = f"{AF_API_BASE_URL}/api/agg-data/export/app/{data.app_id}/{data.report_type}/v5"
    
    params = {
        "from": data.from_date.isoformat(),
        "to": data.to_date.isoformat(),
    }
    
    headers = {
        "Authorization": f"Bearer {AF_TOKEN}",
        "Accept": "text/csv"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.text}"
    except httpx.RequestError as e:
        return f"A network error occurred: {e}"

@mcp.tool()
async def test_appsflyer_connection():
    """Test the connection to AppsFlyer API and return server status."""
    if not AF_API_BASE_URL or not AF_TOKEN:
        return "Error: AppsFlyer API credentials not configured."
    
    return f"AppsFlyer MCP server is running. API Base URL: {AF_API_BASE_URL}, Token configured: {'Yes' if AF_TOKEN else 'No'}"

def main():
    """Run the MCP server."""
    try:
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()