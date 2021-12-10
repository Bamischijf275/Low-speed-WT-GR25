import pandas as pd


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
    return df


if __name__ == "__main__":
    df = load_pressures_from_file("2D/corr_test")
    print(df.head())
