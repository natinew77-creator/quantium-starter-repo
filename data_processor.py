"""
Task 2: Data Processing Script for Quantium Software Engineering Virtual Experience

This script processes the daily sales data files to:
1. Filter for "pink morsel" products only
2. Calculate sales (quantity * price)
3. Combine data from all CSV files into a single output file
"""

import pandas as pd
import os
import re

def load_and_process_data(data_dir='data'):
    """
    Load all CSV files from the data directory, filter for Pink Morsels,
    calculate sales, and return a combined DataFrame.
    """
    all_data = []
    
    # Find all daily_sales_data CSV files
    csv_files = sorted([f for f in os.listdir(data_dir) if f.startswith('daily_sales_data') and f.endswith('.csv')])
    
    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)
        print(f"Processing: {file_path}")
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter for pink morsel only (case insensitive)
        df = df[df['product'].str.lower() == 'pink morsel']
        
        # Clean the price column (remove $ and convert to float)
        df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
        
        # Calculate sales = quantity * price
        df['sales'] = df['quantity'] * df['price']
        
        # Keep only the required columns
        df = df[['sales', 'date', 'region']]
        
        all_data.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Rename columns to match expected output format
    combined_df.columns = ['Sales', 'Date', 'Region']
    
    return combined_df


def save_processed_data(df, output_path='data/formatted_sales_data.csv'):
    """
    Save the processed DataFrame to a CSV file.
    """
    df.to_csv(output_path, index=False)
    print(f"Saved processed data to: {output_path}")
    print(f"Total records: {len(df)}")


if __name__ == '__main__':
    # Process and save the data
    processed_data = load_and_process_data()
    save_processed_data(processed_data)
    
    # Display sample of the data
    print("\nSample of processed data:")
    print(processed_data.head(10))
