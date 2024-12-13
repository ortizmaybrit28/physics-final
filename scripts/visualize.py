import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D

# Paths
RESULTS_PATH = "../output/energy_results.csv"
PLOTS_DIR = "../output/plots/"

def exponential_fit(x, a, b):
    """Exponential model: y = a * exp(b * x)"""
    return a * np.exp(b * x)

def plot_energy_distribution():
    """
    Generate and save multiple plots of energy distribution components.
    """
    # Load results
    try:
        data = pd.read_csv(RESULTS_PATH)
        print(f"Loaded energy results with {len(data)} rows.")
    except FileNotFoundError:
        print(f"Error: File {RESULTS_PATH} not found.")
        return
    except Exception as e:
        print(f"Error loading results: {e}")
        return

    # Ensure output directory exists
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # 1. Energy Components vs Magnitude (Scatter Plot with Exponential Fit Line)
    plt.figure(figsize=(10, 6))
    plt.scatter(data['mag'], data['ER'], label='Radiated Energy (ER)', alpha=0.7, c='blue')
    plt.scatter(data['mag'], data['EG'], label='Fracture Energy (EG)', alpha=0.7, c='green')
    plt.scatter(data['mag'], data['EH'], label='Thermal Energy (EH)', alpha=0.7, c='red')

    # Exponential fit for each energy component (ER, EG, EH)
    for energy_col, color, label in [('ER', 'blue', 'Radiated Energy (ER)'),
                                      ('EG', 'green', 'Fracture Energy (EG)'),
                                      ('EH', 'red', 'Thermal Energy (EH)')]:
        x = data['mag'].values
        y = data[energy_col].values

        # Fit exponential model: y = a * exp(b * x)
        try:
            popt, _ = curve_fit(exponential_fit, x, y, p0=(1, 0.1))  # p0 is the initial guess for a and b
            y_pred = exponential_fit(x, *popt)  # Predict y values using the fitted parameters
            plt.plot(x, y_pred, label=f'{label} Exponential Fit', color=color, linestyle='--')
        except RuntimeError as e:
            print(f"Error fitting {label}: {e}")
    
    plt.xlabel('Magnitude')
    plt.ylabel('Energy (J)')
    plt.title('Energy Components vs Magnitude with Exponential Fit')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "energy_vs_magnitude_with_exp_fit.png"))
    print("Plot saved: energy_vs_magnitude_with_exp_fit.png")

    # 2. Energy Components vs Depth (Scatter Plot)
    plt.figure(figsize=(10, 6))
    plt.scatter(data['depth'], data['ER'], label='Radiated Energy (ER)', alpha=0.7, c='blue')
    plt.scatter(data['depth'], data['EG'], label='Fracture Energy (EG)', alpha=0.7, c='green')
    plt.scatter(data['depth'], data['EH'], label='Thermal Energy (EH)', alpha=0.7, c='red')
    plt.xlabel('Depth (km)')
    plt.ylabel('Energy (J)')
    plt.title('Energy Components vs Depth')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "energy_vs_depth.png"))
    print("Plot saved: energy_vs_depth.png")

    # 3. Time Series Plot (if 'time' column is in a recognizable datetime format)
    if 'time' in data.columns:
        try:
            data['time'] = pd.to_datetime(data['time'])
            plt.figure(figsize=(10, 6))
            plt.plot(data['time'], data['ER'], label='Radiated Energy (ER)', alpha=0.7, c='blue')
            plt.plot(data['time'], data['EG'], label='Fracture Energy (EG)', alpha=0.7, c='green')
            plt.plot(data['time'], data['EH'], label='Thermal Energy (EH)', alpha=0.7, c='red')
            plt.xlabel('Time')
            plt.ylabel('Energy (J)')
            plt.title('Energy Components Over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(PLOTS_DIR, "energy_vs_time.png"))
            print("Plot saved: energy_vs_time.png")
        except Exception as e:
            print(f"Error with time series plot: {e}")

    # 4. 3D Plot of Energy Components vs Magnitude and Depth
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['mag'], data['depth'], data['ER'], label='Radiated Energy (ER)', c='blue')
    ax.scatter(data['mag'], data['depth'], data['EG'], label='Fracture Energy (EG)', c='green')
    ax.scatter(data['mag'], data['depth'], data['EH'], label='Thermal Energy (EH)', c='red')
    ax.set_xlabel('Magnitude')
    ax.set_ylabel('Depth (km)')
    ax.set_zlabel('Energy (J)')
    ax.set_title('3D Plot of Energy Components')
    ax.legend()
    plt.savefig(os.path.join(PLOTS_DIR, "energy_3d_plot.png"))
    print("Plot saved: energy_3d_plot.png")

if __name__ == "__main__":
    plot_energy_distribution()

