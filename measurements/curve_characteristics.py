from math import pi, sqrt

import pandas as pd
import scipy.stats

from measurements.loading import (
    load_pressures_from_file,
    load_pressures_from_file_simulated,
    load_polars_from_xfoil,
)


def find_lift_curve_slope(df, alpha_start, alpha_end):
    df = df.loc[(alpha_start <= df["Alpha"]) & (df["Alpha"] <= alpha_end)]

    res = scipy.stats.linregress(df["Alpha"], df[_find_cl_col(df)])

    slope_deg = res.slope
    slope_rad = slope_deg * 180 / pi

    print(
        f"Cl alpha ({alpha_start} <= alpha <= {alpha_end}) = {slope_rad:.4f} 1/rad = {slope_deg:.4f} 1/deg"
    )

    return slope_rad


def find_cl_max(df):
    cl_max = df[_find_cl_col(df)].max()
    alpha_cl_max = df.iloc[df[_find_cl_col(df)].argmax()]["Alpha"]
    print(f"Cl max = {cl_max:.4f} at alpha = {alpha_cl_max:.1f}°")


def _find_cl_col(df):
    if "Cl" in df:
        return "Cl"
    elif "CL" in df:
        return "CL"
    else:
        raise Exception("Data does not contain lift coefficient")


def helmbold_equation(Cl_alpha_rad, A=5.345):
    """Estimates the wing lift curve slope from the airfoil lift curve slope and aspect ratio"""
    CL_alpha_rad = Cl_alpha_rad * A / (Cl_alpha_rad / pi + sqrt((Cl_alpha_rad / pi) ** 2 + A ** 2))
    CL_alpha_deg = CL_alpha_rad * pi / 180

    print(f"CL_alpha = {CL_alpha_rad:.4f} 1/rad = {CL_alpha_deg:.4f} 1/deg")


if __name__ == "__main__":
    print("### MEASURED ###")
    print("--- 2D ---")
    df = load_pressures_from_file("2D/corr_test")[0]
    slope_2d = find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    print("--- 3D ---")
    df = load_pressures_from_file("balance/corr_test")[0]
    find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    print("--- HELMBOLD ---")
    helmbold_equation(slope_2d)

    print("\n### SIMULATED (VLM) ###")
    print("--- 2D (XFOIL) ---")
    x, y, _ = load_polars_from_xfoil("data/xfoil/Polars/141viscnew")
    df = pd.DataFrame({"Alpha": x, "Cl": y})
    slope_2d = find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    print("--- 3D ---")
    df = load_pressures_from_file_simulated("3D/OP_points_tip/VLM")[0]
    find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    print("--- HELMBOLD ---")
    helmbold_equation(slope_2d)

    print("\n### SIMULATED (LLT) ###")
    print("--- 3D ---")
    df = load_pressures_from_file_simulated("3D/OP_points_tip/LLT")[0]
    find_lift_curve_slope(df, -2, 6)
    find_lift_curve_slope(df, 6, 11.5)
    find_cl_max(df)

    print("--- HELMBOLD ---")
    helmbold_equation(slope_2d)
