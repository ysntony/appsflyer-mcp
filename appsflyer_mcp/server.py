import os
import httpx
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# The AppsFlyer API base URL and token from environment variables
AF_API_BASE_URL = os.getenv("APPSFLYER_API_BASE_URL")
AF_TOKEN = os.getenv("APPSFLYER_TOKEN")

# Import FastMCP from official MCP package
from mcp.server.fastmcp import FastMCP

# Create an instance of the MCP server
# The name here is what the LLM will see
mcp = FastMCP("appsflyer")

# Define the input parameters for your tool
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

# The actual function that will run when the tool is called
@mcp.tool()
async def get_aggregate_data(data: AggregateDataInput):
    """Fetches aggregate data reports from the AppsFlyer Pull API."""
    if not AF_API_BASE_URL or not AF_TOKEN:
        return "Error: AppsFlyer API credentials not configured."

    # The specific endpoint for the AGGREGATE PULL API
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
    import asyncio
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main() 