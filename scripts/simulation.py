import pandas as pd
import os

# Paths
PROCESSED_DATA_PATH = "../output/processed_data.csv"
OUTPUT_RESULTS_PATH = "../output/energy_results.csv"

def compute_energy_partition(data):
    """
    Compute energy components for each earthquake event:
    - W: Total released potential energy
    - ER: Radiated energy
    - EG: Fracture energy
    - EH: Thermal energy
    """
    results = []
    for _, row in data.iterrows():
        # Magnitude
        magnitude = row['mag']  # Total energy (approximation based on magnitude)
        W = 10 ** (1.5 * magnitude + 4.8)
    
        # Energy components (assumptions for this model)
        ER = 0.7 * W  # Radiated energy (70%)
        EG = 0.2 * W  # Fracture energy (20%)
        EH = 0.1 * W  # Thermal energy (10%)
        
        results.append({
            'time': row['time'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'depth': row['depth'],
            'mag': magnitude,
            'ER': ER,
            'EG': EG,
            'EH': EH
        })
    return pd.DataFrame(results)

def simulate_energy_partitioning():
    """
    Main function to compute and save energy partitioning results.
    """
    # Load processed data
    try:
        data = pd.read_csv(PROCESSED_DATA_PATH)
        print(f"Loaded processed data with {len(data)} rows.")
    except FileNotFoundError:
        print(f"Error: File {PROCESSED_DATA_PATH} not found.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return
       
    # Compute energy components
    energy_results = compute_energy_partition(data)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_RESULTS_PATH), exist_ok=True)
    
    # Save results
    try:
        energy_results.to_csv(OUTPUT_RESULTS_PATH, index=False)
        print(f"Energy partitioning results saved to {OUTPUT_RESULTS_PATH}")
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    simulate_energy_partitioning()

