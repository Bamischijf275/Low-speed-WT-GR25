from math import pi

import scipy.stats

from measurements.loading import load_pressures_from_file, load_pressures_from_file_simulated


def find_lift_curve_slope(df, alpha_start, alpha_end):
    df = df.loc[(alpha_start <= df["Alpha"]) & (df["Alpha"] <= alpha_end)]

    res = scipy.stats.linregress(df["Alpha"], df[_find_cl_col(df)])

    slope_deg = res.slope
    slope_rad = slope_deg * 180 / pi

    print(
        f"Cl_alpha ({alpha_start} <= alpha <= {alpha_end}) = {slope_rad:.4f} 1/rad = {slope_deg:.4f} 1/deg"
    )


def find_cl_max(df):
    print(f"Cl max = {df[_find_cl_col(df)].max()}")


def _find_cl_col(df):
    if "Cl" in df:
        return "Cl"
    elif "CL" in df:
        return "CL"
    else:
        raise Exception("Data does not contain lift coefficient")


if __name__ == "__main__":
    # 3D
    # df = load_pressures_from_file("balance/corr_test")[0]
    df = load_pressures_from_file_simulated("3D/OP_points_tip/VLM")[0]
    # df = load_pressures_from_file_simulated("3D/OP_points_tip/LLT")[0]
    find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    # 2D
    # df = load_pressures_from_file("2D/corr_test")[0]
    # find_lift_curve_slope(df, -2, 6)
    # find_lift_curve_slope(df, 6, 11.5)
    # find_cl_max(df)
