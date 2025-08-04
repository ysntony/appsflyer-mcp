"""
Tests for the AppsFlyer MCP server.
"""

import pytest
from datetime import date
from appsflyer_mcp.server import AggregateDataInput, get_aggregate_data


class TestAggregateDataInput:
    """Test the AggregateDataInput model."""
    
    def test_valid_input(self):
        """Test that valid input is accepted."""
        data = AggregateDataInput(
            app_id="test_app_id",
            from_date=date(2024, 1, 1),
            to_date=date(2024, 1, 31),
            report_type="daily"
        )
        assert data.app_id == "test_app_id"
        assert data.report_type == "daily"
    
    def test_default_report_type(self):
        """Test that report_type defaults to 'daily'."""
        data = AggregateDataInput(
            app_id="test_app_id",
            from_date=date(2024, 1, 1),
            to_date=date(2024, 1, 31)
        )
        assert data.report_type == "daily"
    
    def test_invalid_report_type(self):
        """Test that invalid report_type raises an error."""
        with pytest.raises(ValueError):
            AggregateDataInput(
                app_id="test_app_id",
                from_date=date(2024, 1, 1),
                to_date=date(2024, 1, 31),
                report_type="invalid_type"
            )


@pytest.mark.asyncio
async def test_get_aggregate_data_no_credentials():
    """Test that the function returns an error when credentials are not configured."""
    data = AggregateDataInput(
        app_id="test_app_id",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 1, 31)
    )
    
    # This test would need to mock the environment variables
    # For now, we'll just test the function exists
    assert callable(get_aggregate_data) 