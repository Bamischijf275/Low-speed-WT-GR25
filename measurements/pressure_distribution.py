import numpy as np
import matplotlib.pyplot as plt

from measurements.loading import load_pressures_from_file
from measurements.plotting import format_plot, save_plot

N_STATIONS = 24


def plot_pressure_distribution(alpha, df, name):
    col_names_upper = [f"Cpu_{i:03d}" for i in range(1, N_STATIONS + 1)]
    col_names_lower = [f"Cpl_{i:03d}" for i in range(1, N_STATIONS)]
    x_stations = np.linspace(0, 1, N_STATIONS)

    row = df[df["Alpha"] == alpha]
    if len(row) == 0:
        raise "Invalid angle of attack"

    cp_upper = row[col_names_upper].iloc[0, ::-1]
    cp_lower = row[col_names_lower].iloc[0]
    cp_lower[f"Cpl_{N_STATIONS:03d}"] = cp_upper[f"Cpu_001"]

    plt.figure(figsize=[12, 6])

    plt.plot(x_stations, cp_upper, label="Upper surface", marker="D")
    plt.plot(x_stations, cp_lower, label="Lower surface", marker="D")
    plt.xlabel("x/c")
    plt.ylabel("$C_p$")
    plt.legend()

    plt.ylim([-5.35 * 1.05, 1.04])
    plt.gca().invert_yaxis()

    format_plot()
    save_plot(f"pressure_dist_{name}")


def plot_pressure_distribution_all_alphas(file, prefix):
    df, trash = load_pressures_from_file(file)  # Don't need hysteresis, only df

    for alpha in df["Alpha"]:
        plot_pressure_distribution(alpha, df, f"{prefix}_{alpha:.1f}")


if __name__ == "__main__":
    plot_pressure_distribution_all_alphas("2D/corr_test", "2D")
    plot_pressure_distribution_all_alphas("3D/corr_test", "3D")
