import os
from multiprocessing import Pool

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import uniform_filter1d

from measurements.loading import load_infrared_from_file
from measurements.plotting import save_plot


def find_transition_point(image):
    # Average along span to get single chordwise line
    spanwise_average = np.average(image, axis=0)
    # Find pixel-by-pixel difference along chord
    chordwise_difference = np.diff(spanwise_average)
    # Moving average with window size 5
    chordwise_difference = uniform_filter1d(chordwise_difference, size=5)

    # Crop image to wing without background
    x_leading_edge = chordwise_difference.argmax()
    x_trailing_edge = chordwise_difference.argmin() + 1
    # Cut off 10 px on either end to ensure transition is maximum difference and not LE/TE
    chordwise_difference = chordwise_difference[x_leading_edge + 10 : x_trailing_edge - 10]

    # Add 10 px cutoff back to find x/c of transition
    xc_transition = (chordwise_difference.argmax() + 10) / (len(chordwise_difference) + 20)

    # Convert to image coordinates for line in plot
    x_transition = x_leading_edge + xc_transition * (len(chordwise_difference) + 20)

    return xc_transition, x_transition


def plot_infrared_image(folder, prefix, alpha):
    image = load_infrared_from_file(folder)

    xc_transition, x_transition = find_transition_point(image)

    plt.imshow(image, cmap="plasma", interpolation="none")

    # No clear transition beyond 10 deg
    if alpha[0] == "-" or float(alpha.split("-")[0]) <= 8.5:
        plt.axvline(x_transition, c="black", linestyle=(0, (1, 10)))
        plt.text(x_transition + 10, 20, f"x/c = {xc_transition:.2f}")

    plt.axis("off")
    plt.gcf().tight_layout(pad=0.1, h_pad=0.4, w_pad=0.4)

    save_plot(f"infrared_transition_{prefix}_{alpha}")


def plot_infrared_image_all_alphas(folder, prefix):
    p = Pool()

    folder = f"data/infrared/{folder}"
    for alpha in os.listdir(folder):
        full_path = os.path.join(folder, alpha)
        if os.path.isdir(full_path) and os.listdir(full_path):
            p.apply_async(plot_infrared_image, args=(full_path, prefix, alpha))

    p.close()
    p.join()


if __name__ == "__main__":
    plot_infrared_image_all_alphas("2dIR", "2D")
    # plot_infrared_image("data/infrared/2dIR/8", "2D", "5")
