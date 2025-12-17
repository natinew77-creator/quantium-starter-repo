"""
Task 5: Unit Tests for Quantium Soul Foods Dashboard

This module contains unit tests for both the data processing script
and the Dash application.

The three required tests for the Dash app verify:
1. The header is present
2. The visualisation is present
3. The region picker is present
"""

import pytest
import pandas as pd
import os
import sys

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


# ============================================================================
# Task 5: Dash Application Tests
# These tests verify the three required elements are present in the app layout:
# 1. The header is present
# 2. The visualisation is present
# 3. The region picker is present
# ============================================================================

from dash import html, dcc
from app import app


def find_component_by_id(layout, component_id):
    """
    Recursively search for a component with the given ID in the layout.
    Returns True if found, False otherwise.
    """
    if hasattr(layout, 'id') and layout.id == component_id:
        return True
    
    if hasattr(layout, 'children'):
        children = layout.children
        if children is None:
            return False
        if isinstance(children, (list, tuple)):
            for child in children:
                if find_component_by_id(child, component_id):
                    return True
        else:
            return find_component_by_id(children, component_id)
    
    return False


def find_component_by_type(layout, component_type):
    """
    Recursively search for a component of the given type in the layout.
    Returns True if found, False otherwise.
    """
    if isinstance(layout, component_type):
        return True
    
    if hasattr(layout, 'children'):
        children = layout.children
        if children is None:
            return False
        if isinstance(children, (list, tuple)):
            for child in children:
                if find_component_by_type(child, component_type):
                    return True
        else:
            return find_component_by_type(children, component_type)
    
    return False


class TestDashApp:
    """
    Unit tests for the Dash application layout.
    These tests verify the three required components are present.
    """
    
    def test_header_exists(self):
        """
        Test 1: Verify the header is present.
        The app should have an H1 header element.
        """
        layout = app.layout
        assert find_component_by_type(layout, html.H1), "Header (H1) should be present in the app layout"
    
    def test_visualization_exists(self):
        """
        Test 2: Verify the visualisation (chart) is present.
        The app should have a Graph component with id 'sales-chart'.
        """
        layout = app.layout
        assert find_component_by_id(layout, 'sales-chart'), "Visualization (Graph with id='sales-chart') should be present"
    
    def test_region_picker_exists(self):
        """
        Test 3: Verify the region picker (radio buttons) is present.
        The app should have a RadioItems component with id 'region-radio'.
        """
        layout = app.layout
        assert find_component_by_id(layout, 'region-radio'), "Region picker (RadioItems with id='region-radio') should be present"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
