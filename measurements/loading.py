import glob

import numpy as np
import pandas as pd
from PIL import Image


def load_pressures_from_file(filename, remove_hysteresis=False):
    # Need to separate loading of headers and data because there is a weird extra column at the end
    # Load column names
    header = (
        pd.read_csv(f"data/cp/{filename}.txt", sep="\t", nrows=1, header=None)
        .iloc[0]
        .values.tolist()
    )
    # Remove whitespace from column names
    header = list(map(lambda s: s.strip(), header))
    # Load actual data
    df = pd.read_csv(
        f"data/cp/{filename}.txt", sep="\t", skiprows=2, index_col=False, names=header
    ).iloc[:, 1:]

    if remove_hysteresis:
        # Ignore hysteresis part
        idx_alpha_max = df["Alpha"].idxmax() + 1
        df = df.iloc[:idx_alpha_max]

    return df


def load_infrared_from_file(folder):
    individual_data = []
    for file in glob.glob(f"{folder}/*.csv"):
        # Remove last column which is NaN
        individual_data.append(np.delete(np.genfromtxt(file, delimiter=";"), -1, axis=1))

    # Average all images in the folder
    averaged_data = np.average(individual_data, axis=0)

    # Normalize to [0, 1]
    min_temp = averaged_data.min()
    max_temp = averaged_data.max()
    averaged_data = (averaged_data - min_temp) / (max_temp - min_temp)

    image = Image.fromarray(np.uint8(averaged_data * 255))
    # Rotate so LE and TE are vertical
    image = image.rotate(-1.2, resample=Image.BICUBIC)
    # Crop for clear image of wing without wall and lower tuft
    image = image.crop((50, 30, image.width - 50, image.height - 130))
    # Flip so flow comes from left
    image = image.transpose(method=Image.FLIP_LEFT_RIGHT)

    return np.array(image), image.height


if __name__ == "__main__":
    df = load_pressures_from_file("2D/corr_test")
    print(df.head())
