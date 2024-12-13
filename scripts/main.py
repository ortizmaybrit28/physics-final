import pandas as pd
import os
from scripts.load_data import load_earthquake_data
from scripts.energy_partitioning import calculate_radiated_energy, calculate_fracture_energy, calculate_thermal_energy
from scripts.visualization import plot_energy_distribution

# Step 1: Load the data
data_path = "data/all_month.csv"
df = load_earthquake_data(data_path)

# Step 2: Filter data (California earthquakes)
california_bbox = [32.5, 42.0, -125.0, -114.0]  # min_lat, max_lat, min_lon, max_lon
df_california = df[
    (df["latitude"] >= california_bbox[0]) & (df["latitude"] <= california_bbox[1]) &
    (df["longitude"] >= california_bbox[2]) & (df["longitude"] <= california_bbox[3]) &
    (df["magnitude"] >= 3.0)  # Only select earthquakes with magnitude 3.0 or higher
]

print(f"Filtered data: {len(df_california)} earthquakes found in California with magnitude 3.0+.")
print(df_california.head())

# Step 3: Compute energy partitioning
df_california['E_R'] = df_california.apply(lambda row: calculate_radiated_energy(row['magnitude'], row.get('stress_drop', None)), axis=1)
df_california['E_G'] = df_california.apply(lambda row: calculate_fracture_energy(row.get('fault_slip', None), row.get('material_elasticity', None)), axis=1)

# Calculate total released energy (ΔW)
df_california['total_energy'] = df_california['E_R'] + df_california['E_G']

# Calculate thermal energy (E_H)
df_california['E_H'] = df_california.apply(lambda row: calculate_thermal_energy(row['total_energy'], row['E_R'], row['E_G']), axis=1)

# Step 4: Save processed data
output_path = "output/processed_earthquake_data.csv"
df_california.to_csv(output_path, index=False)

# Step 5: Visualize energy distribution
plot_path = "output/energy_distribution.png"
plot_energy_distribution(df_california, save_path=plot_path)

print("Analysis complete. Results saved in 'output/' directory.")
