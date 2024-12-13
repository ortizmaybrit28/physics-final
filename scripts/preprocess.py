import pandas as pd
import os

# Paths
DATA_PATH = "data/all_month.csv"
OUTPUT_PATH = "output/processed_data.csv"

def preprocess_data():
    """
    Preprocess the earthquake data from all_month.csv:
    - Load raw data
    - Filter relevant columns
    - Handle missing values
    - Save the processed data
    """
    # Load the raw data
    try:
        data = pd.read_csv(DATA_PATH)
        print(f"Loaded data with {len(data)} rows.")
    except FileNotFoundError:
        print(f"Error: File {DATA_PATH} not found.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Filter relevant columns
    columns_to_keep = ['time', 'latitude', 'longitude', 'depth', 'mag', 'place']
    data = data[columns_to_keep]
    
    # Handle missing values (drop rows with missing critical data)
    data = data.dropna(subset=['time', 'latitude', 'longitude', 'depth', 'mag'])

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Save the processed data
    try:
        data.to_csv(OUTPUT_PATH, index=False)
        print(f"Processed data saved to {OUTPUT_PATH}")
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    preprocess_data()

