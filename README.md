# AppsFlyer MCP Server

A Model Context Protocol (MCP) server for integrating AppsFlyer analytics data with AI assistants.

## Features

- Fetch aggregate data reports from AppsFlyer Pull API
- Support for multiple report types: partners_report, partners_by_date_report, daily_report, geo_report, geo_by_date_report
- Secure API token authentication
- Type-safe input validation with Pydantic

## Installation

```bash
git clone https://github.com/ysntony/appsflyer-mcp
cd appsflyer-mcp
uv sync
```

## Configuration

Set up your AppsFlyer API credentials as environment variables:

```bash
export APPSFLYER_API_BASE_URL="https://hq1.appsflyer.com"
export APPSFLYER_TOKEN="your_api_token_here"
```

Or create a `.env` file:

```env
APPSFLYER_API_BASE_URL=https://hq1.appsflyer.com
APPSFLYER_TOKEN=your_api_token_here
```

## Usage

### Running the MCP Server

```bash
uv run python run_server.py
```

### MCP Configuration

Add to your MCP configuration file:

```json
{
  "mcpServers": {
    "appsflyer": {
      "command": "uv",
      "args": ["run", "python", "run_server.py"],
      "cwd": "/path/to/appsflyer-mcp",
      "env": {
        "APPSFLYER_API_BASE_URL": "https://hq1.appsflyer.com",
        "APPSFLYER_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## Available Tools

- `get_aggregate_data`: Fetch aggregate data reports from AppsFlyer Pull API
- `test_appsflyer_connection`: Test the connection to AppsFlyer API

## Report Types

- `partners_report`: Partner performance data
- `partners_by_date_report`: Daily partner performance data
- `daily_report`: Daily aggregate data (default)
- `geo_report`: Geographic performance data
- `geo_by_date_report`: Daily geographic performance data

## Development

```bash
uv sync --dev
pytest
```

## License

MIT License






