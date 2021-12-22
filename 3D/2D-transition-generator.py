import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

plots = True

def save_plot(name: str, type="pdf"):
    os.makedirs("plots", exist_ok=True)
    name = name.replace(".", "-")
    plt.savefig(
        f"plots/plot_{name}.{type}",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()


def plot_config():
    """
    Contains the configuration for the plots
    """
    line_thickness = 6
    line_color = "#000000"

    plt.ylim(0.0, 0.7)
    plt.xlim(-0.1, 0.3)
    plt.plot((0, 0), (0, 0.64), linewidth=line_thickness, color=line_color)
    plt.plot((0, 0.24), (0.64, 0.64), linewidth=line_thickness, color=line_color)
    plt.plot((0.24, 0.24), (0.64, 0), linewidth=line_thickness, color=line_color)
    plt.plot((0.24, 0), (0.0, 0.0), linewidth=line_thickness, color=line_color)
    plt.gca().invert_yaxis()
    plt.legend()


colors = [
    "#38f523",
    "#d29d00",
    "#f40909",
]

if plots:
    # Plots without tip, LLT
    plt.figure()
    k = 0
    xc = [0.6679, 0.0377, 0.0145]
    angles = [0, 7, 14]
    for i, j in enumerate(xc):
        plt.plot((0.24*j,0.24*j), (0,0.64), color=colors[k], label=f"AOA {angles[i]}")
        k += 1
        plot_config()
        save_plot(f"Transition lines 2D, AOA={angles[i]}")