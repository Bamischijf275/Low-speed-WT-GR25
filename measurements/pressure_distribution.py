import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from measurements.loading import (
    load_pressures_from_file,
    load_pressures_from_file_simulated,
    load_pressures_from_xfoil,
)
from measurements.plotting import format_plot, save_plot

N_STATIONS_MEASURED = 24
N_STATIONS_XFLR = 12
N_STATIONS_XFOIL = 71


def plot_pressure_distribution(alpha, df, name, source):
    plt.figure(figsize=[12, 6])

    if source == "xflr":
        x_stations, cp = _select_data(alpha, df, source)
        plt.plot(x_stations, cp, label="Both surfaces", marker="D")
    else:
        x_stations, cp_upper, cp_lower = _select_data(alpha, df, source)
        plt.plot(x_stations, cp_upper, label="Upper surface", marker="D")
        plt.plot(x_stations, cp_lower, label="Lower surface", marker="D")

    plt.xlabel("x/c")
    plt.ylabel("$C_p$")
    plt.legend()

    if source == "xfoil" and alpha >= 10:
        # XFoil pressure distributions go wild above 10 deg
        plt.ylim([-8.5 * 1.05, 2.8 * 1.05])
    else:
        plt.ylim([-5.35 * 1.05, 2.8 * 1.05])
    plt.gca().invert_yaxis()

    format_plot()
    save_plot(f"pressure_dist_{name}")


def plot_pressure_distribution_superposition(file, alphas, prefix):
    df, _ = load_pressures_from_file(file)

    # Round to the next 0.5
    df["Alpha"] = (df["Alpha"] * 2).round() / 2

    plt.figure(figsize=[12, 6])

    # colors = sb.color_palette("crest_r", n_colors=int(1 * len(alphas)))
    colors = sb.color_palette()

    for i, alpha in enumerate(alphas):
        x_stations, cp_upper, cp_lower = _select_data(alpha, df, source="measurements")
        plt.plot(
            x_stations, cp_upper, label=r"$\alpha$ " + f"= {alpha:.1f}°", marker="D", c=colors[i]
        )
        plt.plot(x_stations, cp_lower, marker="D", c=colors[i])

    plt.xlabel("x/c")
    plt.ylabel("$C_p$")
    plt.legend()

    plt.ylim([-5.35 * 1.05, 2.8 * 1.05])
    plt.gca().invert_yaxis()

    format_plot()
    save_plot(f"pressure_dist_superposition_{prefix}")


def plot_pressure_distribution_superposition_2d_3d(file_2d, file_3d, alpha):
    df_2d, _ = load_pressures_from_file(file_2d)
    df_3d, _ = load_pressures_from_file(file_3d)

    # Round to the next 0.5
    df_2d["Alpha"] = (df_2d["Alpha"] * 2).round() / 2
    df_3d["Alpha"] = (df_3d["Alpha"] * 2).round() / 2

    plt.figure(figsize=[12, 6])

    colors = sb.color_palette()

    # Plot 2D pressure distribution
    x_stations, cp_upper, cp_lower = _select_data(alpha, df_2d, source="measurements")
    plt.plot(x_stations, cp_upper, label="2D", marker="D", c=colors[0])
    plt.plot(x_stations, cp_lower, marker="D", c=colors[0])

    # Plot 3D pressure distribution
    x_stations, cp_upper, cp_lower = _select_data(alpha, df_3d, source="measurements")
    plt.plot(x_stations, cp_upper, label="3D", marker="D", c=colors[1])
    plt.plot(x_stations, cp_lower, marker="D", c=colors[1])

    plt.xlabel("x/c")
    plt.ylabel("$C_p$")
    plt.legend()

    plt.ylim([-5.35 * 1.05, 2.8 * 1.05])
    plt.gca().invert_yaxis()

    format_plot()
    save_plot(f"pressure_dist_superposition_2d_3d_{alpha}")


def _select_data(alpha, df, source):
    row = df[df["Alpha"] == alpha]
    if len(row) == 0:
        raise "Invalid angle of attack"

    if source == "measurements":
        col_names_upper = [f"Cpu_{i:03d}" for i in range(1, N_STATIONS_MEASURED + 1)]
        col_names_lower = [f"Cpl_{i:03d}" for i in range(1, N_STATIONS_MEASURED)]
        x_stations = np.linspace(0, 1, N_STATIONS_MEASURED)

        cp_upper = row[col_names_upper].iloc[0, ::-1]
        cp_lower = row[col_names_lower].iloc[0]
        cp_lower[f"Cpl_{N_STATIONS_MEASURED:03d}"] = cp_upper["Cpu_001"]

        return x_stations, cp_upper, cp_lower
    elif source == "xfoil":
        col_names_upper = [f"Cpu_{i:03d}" for i in range(1, N_STATIONS_XFOIL + 1)]
        col_names_lower = [f"Cpl_{i:03d}" for i in range(2, N_STATIONS_XFOIL + 1)]
        x_stations = np.linspace(0, 1, N_STATIONS_XFOIL)

        cp_upper = row[col_names_upper].iloc[0]
        cp_lower = row[col_names_lower].iloc[0]
        cp_lower["Cpl_001"] = cp_upper["Cpu_001"]
        cp_lower = cp_lower.sort_index()

        return x_stations, cp_upper, cp_lower
    elif source == "xflr":
        col_names = [f"Cp_{i:03d}" for i in range(1, N_STATIONS_XFLR + 1)]
        x_stations = np.linspace(0, 1, N_STATIONS_XFLR)

        cp = row[col_names].iloc[0]
        return x_stations, cp


def plot_pressure_distribution_all_alphas(file, prefix):
    df, _ = load_pressures_from_file(file)

    for alpha in df["Alpha"]:
        plot_pressure_distribution(alpha, df, f"{prefix}_{alpha:.1f}", source="measurements")


def plot_pressure_distribution_all_alphas_xfoil():
    df = load_pressures_from_xfoil()

    for alpha in df["Alpha"]:
        plot_pressure_distribution(alpha, df, f"2D_xfoil_141_visc_{alpha:.1f}", source="xfoil")


def plot_pressure_distribution_all_alphas_xflr(folder, prefix):
    df, _ = load_pressures_from_file_simulated(folder)

    for alpha in df["Alpha"]:
        plot_pressure_distribution(alpha, df, f"{prefix}_{alpha:.1f}", source="xflr")


if __name__ == "__main__":
    # plot_pressure_distribution_all_alphas("2D/corr_test", "2D")
    # plot_pressure_distribution_all_alphas("3D/corr_test", "3D")

    plot_pressure_distribution_superposition("2D/corr_test", [0, 5, 10, 14], "2D")
    plot_pressure_distribution_superposition("3D/corr_test", [0, 5, 10, 14], "3D")
    plot_pressure_distribution_superposition_2d_3d("2D/corr_test", "3D/corr_test", 14)

    # plot_pressure_distribution_all_alphas_xflr("3D/OP_points_no_tip/VLM", "3D_VLM_no_tip")
    # plot_pressure_distribution_all_alphas_xflr("3D/OP_points_tip/VLM", "3D_VLM_tip")

    # plot_pressure_distribution_all_alphas_xfoil()
