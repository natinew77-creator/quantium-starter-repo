"""
Task 5: Unit Tests for Quantium Soul Foods Dashboard

This module contains unit tests for both the data processing script
and the Dash application.
"""

import pytest
import pandas as pd
import os
import sys
from dash.testing.application_runners import import_app

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_processor import load_and_process_data


class TestDataProcessor:
    """Unit tests for the data processing functionality."""
    
    def test_load_and_process_data_returns_dataframe(self):
        """Test that load_and_process_data returns a pandas DataFrame."""
        df = load_and_process_data()
        assert isinstance(df, pd.DataFrame)
    
    def test_data_has_required_columns(self):
        """Test that the processed data has Sales, Date, and Region columns."""
        df = load_and_process_data()
        required_columns = ['Sales', 'Date', 'Region']
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_data_not_empty(self):
        """Test that the processed data is not empty."""
        df = load_and_process_data()
        assert len(df) > 0, "Processed data should not be empty"
    
    def test_sales_values_are_numeric(self):
        """Test that Sales values are numeric and positive."""
        df = load_and_process_data()
        assert df['Sales'].dtype in ['float64', 'int64'], "Sales should be numeric"
        assert (df['Sales'] > 0).all(), "All sales values should be positive"
    
    def test_region_values_are_valid(self):
        """Test that Region values are valid (north, south, east, west)."""
        df = load_and_process_data()
        valid_regions = {'north', 'south', 'east', 'west'}
        actual_regions = set(df['Region'].str.lower().unique())
        assert actual_regions.issubset(valid_regions), f"Invalid regions found: {actual_regions - valid_regions}"
    
    def test_date_column_is_string(self):
        """Test that the Date column contains properly formatted dates."""
        df = load_and_process_data()
        # Check that dates can be parsed
        try:
            pd.to_datetime(df['Date'])
        except Exception as e:
            pytest.fail(f"Date column contains invalid dates: {e}")
    
    def test_output_file_exists(self):
        """Test that the output CSV file exists after processing."""
        from data_processor import save_processed_data
        df = load_and_process_data()
        output_path = 'data/formatted_sales_data.csv'
        save_processed_data(df, output_path)
        assert os.path.exists(output_path), f"Output file should exist at {output_path}"


class TestDashApp:
    """Unit tests for the Dash application."""
    
    def test_app_header_h1_exists(self, dash_duo):
        """Test that the app has a header with the correct title."""
        app = import_app('app')
        dash_duo.start_server(app)
        
        # Wait for the app to load
        dash_duo.wait_for_element('h1', timeout=10)
        
        # Check that the header contains the expected text
        header = dash_duo.find_element('h1')
        assert "Soul Foods" in header.text or "Pink Morsel" in header.text
    
    def test_region_radio_exists(self, dash_duo):
        """Test that the region radio button component exists."""
        app = import_app('app')
        dash_duo.start_server(app)
        
        # Wait for the radio buttons to appear
        dash_duo.wait_for_element('#region-radio', timeout=10)
        
        # Check that it exists
        radio = dash_duo.find_element('#region-radio')
        assert radio is not None
    
    def test_chart_exists(self, dash_duo):
        """Test that the sales chart exists."""
        app = import_app('app')
        dash_duo.start_server(app)
        
        # Wait for the chart to appear
        dash_duo.wait_for_element('#sales-chart', timeout=10)
        
        # Check that it exists
        chart = dash_duo.find_element('#sales-chart')
        assert chart is not None
    
    def test_summary_stats_exists(self, dash_duo):
        """Test that the summary statistics section exists."""
        app = import_app('app')
        dash_duo.start_server(app)
        
        # Wait for the summary stats to appear
        dash_duo.wait_for_element('#summary-stats', timeout=10)
        
        # Check that it exists
        stats = dash_duo.find_element('#summary-stats')
        assert stats is not None


# Pytest fixture configuration for Dash testing
@pytest.fixture
def dash_duo(dash_duo):
    """Fixture for Dash application testing."""
    return dash_duo


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
