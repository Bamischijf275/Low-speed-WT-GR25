"""
Identical in functionality to infrared.py but with plotting code for report.
"""
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import uniform_filter1d

from measurements.loading import load_infrared_from_file
from measurements.plotting import save_plot, format_plot

# Distance in px from LE/TE in which transition will not be detected
# Necessary to prevent LE/TE to be detected as transition point
EDGE_CUTOFF = 5


def find_transition_point(image):
    # Average along span to get single chordwise line
    spanwise_average = np.average(image, axis=0)
    # Find pixel-by-pixel difference along chord
    chordwise_difference = np.diff(spanwise_average)
    # Moving average with window size 3
    unfiltered = chordwise_difference
    chordwise_difference = uniform_filter1d(chordwise_difference, size=3)

    # Crop image to wing without background
    x_leading_edge = chordwise_difference.argmax()
    x_trailing_edge = chordwise_difference.argmin()
    chordwise_difference = chordwise_difference[
        x_leading_edge + EDGE_CUTOFF : x_trailing_edge - 2 * EDGE_CUTOFF
    ]

    chord_length = x_trailing_edge - x_leading_edge

    # Find x/c of transition
    xc_transition = (chordwise_difference.argmin() + EDGE_CUTOFF) / chord_length

    # Convert to image coordinates for line in plot
    x_transition = int(x_leading_edge + xc_transition * chord_length)

    plt.figure(figsize=[12, 6])

    plt.axvspan(x_leading_edge, x_leading_edge + EDGE_CUTOFF, color="black", alpha=0.15, zorder=-2)
    plt.axvspan(
        x_leading_edge + EDGE_CUTOFF,
        x_trailing_edge - 2 * EDGE_CUTOFF,
        color="green",
        alpha=0.1,
        zorder=-2,
    )
    plt.axvspan(
        x_trailing_edge - 2 * EDGE_CUTOFF, x_trailing_edge, color="black", alpha=0.15, zorder=-2
    )

    plt.axvline(x_trailing_edge, color="black", linestyle=(0, (1, 10)), zorder=-1)
    plt.axvline(x_leading_edge, color="black", linestyle=(0, (1, 10)), zorder=-1)

    plt.text(x_leading_edge - 5, -0.22, "LE", ha="right")
    plt.text(x_trailing_edge + 5, -0.22, "TE")
    plt.text(x_transition, chordwise_difference.min() - 0.035, "Transition", ha="center")

    plt.plot(unfiltered, label="Unfiltered", zorder=1)
    plt.plot(
        np.arange(0, len(chordwise_difference)) + x_leading_edge + EDGE_CUTOFF,
        chordwise_difference,
        label="Moving average",
        zorder=2,
    )

    plt.scatter(
        x_transition, chordwise_difference.min(), marker="x", color="black", s=30, zorder=20
    )

    plt.legend()
    plt.xlabel("Pixel in chordwise direction [-]")
    plt.ylabel("Temperature [°C]")

    format_plot(zeroline=False)

    # plt.show()
    save_plot("processing_infrared_diff_along_chord")

    plt.figure(figsize=[12, 4.5])

    plt.plot(spanwise_average)

    plt.text(
        x_transition,
        spanwise_average[x_transition] - 0.18,
        "Transition",
        ha="center",
    )
    plt.scatter(
        x_transition,
        spanwise_average[x_transition],
        marker="x",
        color="black",
        s=30,
        zorder=20,
    )

    plt.xlabel("Pixel in chordwise direction [-]")
    plt.ylabel("Temperature [°C]")
    format_plot(zeroline=False)

    save_plot("processing_infrared_temp_along_chord")

    return xc_transition, x_transition, x_leading_edge, x_trailing_edge


def plot_infrared_image(folder):
    image, height = load_infrared_from_file(folder)

    find_transition_point(image)

    plt.imshow(image, cmap="plasma", interpolation="none")

    plt.axis("off")
    plt.gcf().tight_layout(pad=0.1, h_pad=0.4, w_pad=0.4)

    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("bottom", size="8%", pad=0.1)

    plt.colorbar(orientation="horizontal", cax=cax)

    # plt.show()
    save_plot(f"processing_infrared_averaged")


if __name__ == "__main__":
    plot_infrared_image("data/infrared/2dIR/5")
