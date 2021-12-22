import glob
import os

import numpy as np
import pandas as pd
from PIL import Image


def load_pressures_from_file(filename):
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

    # Ignore hysteresis part
    idx_alpha_max = df["Alpha"].idxmax() + 1
    hysteresis = df.iloc[idx_alpha_max - 1 :]
    df_clean = df.iloc[:idx_alpha_max]

    return df_clean, hysteresis, df  # return hysteresis seperately


def load_pressures_from_file_simulated(folder, strip=1):
    def parse_number(lines, lineno):
        return float(lines[lineno - 1].split("=")[1].strip().split(" ")[0].strip())

    if not (os.path.exists(folder) and os.path.isdir(folder)):
        raise FileNotFoundError(f'"folder" is not an existing folder')

    data = []
    for file in glob.glob(f"{folder}/*.txt"):
        with open(file) as f:
            lines = f.readlines()

        run_data = {
            "Alpha": parse_number(lines, 6),
            "Cl": parse_number(lines, 10),
            "Cd": parse_number(lines, 12),
            "Cm": parse_number(lines, 14),
        }

        # Only VLM gives pressure distribution data
        if "VLM" in folder:
            cp_data_start = cp_data_end = None
            for i, line in enumerate(lines):
                if line.strip() == f"Strip {strip}":
                    cp_data_start = i + 1
                if line.strip() == f"Strip {strip+1}":
                    cp_data_end = i

            # Strip is last one in file
            if not cp_data_end:
                cp_data_end = len(lines)

            if not (cp_data_start and cp_data_end):
                raise Exception(f"Invalid strip {strip}")

            cp_data = np.genfromtxt(lines[cp_data_start:cp_data_end])[:, -1]
            run_data.update({f"Cp_{i:03d}": cp for i, cp in enumerate(cp_data)})

        data.append(run_data)

    df = pd.DataFrame(data)
    df = df.sort_values(by=["Alpha"], ignore_index=True)

    return df, pd.DataFrame()


def load_infrared_from_file(folder):
    individual_data = []
    for file in glob.glob(f"{folder}/*.csv"):
        # Remove last column which is NaN
        individual_data.append(np.delete(np.genfromtxt(file, delimiter=";"), -1, axis=1))

    # Average all images in the folder
    averaged_data = np.average(individual_data, axis=0)

    # Normalize to [0, 1] as required by Pillow
    min_temp = averaged_data.min()
    max_temp = averaged_data.max()
    range_temp = max_temp - min_temp
    averaged_data = (averaged_data - min_temp) / range_temp

    image = Image.fromarray(np.uint8(averaged_data * 255))
    # Rotate so LE and TE are vertical
    image = image.rotate(-1.2, resample=Image.BICUBIC)
    # Crop for clear image of wing without wall and lower tuft
    image = image.crop((50, 30, image.width - 80, image.height - 130))
    # Flip so flow comes from left
    image = image.transpose(method=Image.FLIP_LEFT_RIGHT)

    # Scale up to real temperature range
    processed_image = np.array(image)
    processed_image = processed_image / 255 * range_temp + min_temp

    return processed_image, image.height


def load_pressures_from_xfoil():
    df_all = None
    for file in glob.glob(f"data/xfoil/Pressure distributions/pressure_141_visc_*"):
        df = pd.read_csv(file, delimiter=r"\s+", skiprows=1, header=None, index_col=False)

        # Set proper column names
        col_names_upper = [f"Cpu_{i:03d}" for i in range(71, 0, -1)]
        col_names_lower = [f"Cpl_{i:03d}" for i in range(2, 72)]

        df.iloc[:, 0] = col_names_upper + col_names_lower

        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])

        # Convert strings to float
        df = df.apply(pd.to_numeric)

        df["Alpha"] = float(file.split("_")[-1].replace(",", "."))

        if df_all is None:
            df_all = df
        else:
            df_all = pd.concat([df_all, df])

    df_all = df_all.sort_values(by=["Alpha"], ignore_index=True)

    return df_all


def load_polars_from_xfoil(filename):
    df = pd.read_csv(f"data/xfoil/Polars/{filename}", delimiter=r"\s+", header=5, index_col=False)

    # Select only needed columns
    df = df.iloc[1:, [0, 1, 2, 4]]

    # Convert strings to float
    df = df.apply(pd.to_numeric)

    # Rename to common names
    df = df.rename({"alpha": "Alpha", "CL": "Cl", "CD": "Cd", "CM": "Cm"}, axis=1)

    return df, pd.DataFrame()


if __name__ == "__main__":
    # df = load_pressures_from_file("2D/corr_test")[0]
    df = load_polars_from_xfoil("141viscnew")[0]
    # df = load_pressures_from_file_simulated("3D/OP_points_no_tip/VLM")[0]
    print(df.head())
    print(df.info())
