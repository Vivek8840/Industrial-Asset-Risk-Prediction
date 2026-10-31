
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ai4i2020.csv"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place ai4i2020.csv inside data/raw/."
        )

    df = pd.read_csv(DATA_PATH)

    print("\n--- DATASET SHAPE ---")
    print(df.shape)

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    print("\n--- FIRST FIVE ROWS ---")
    print(df.head())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())

    print("\n--- MACHINE FAILURE DISTRIBUTION ---")
    print(df["Machine failure"].value_counts())
    print(df["Machine failure"].value_counts(normalize=True) * 100)

    print("\n--- FAILURE-MODE COUNTS ---")
    failure_modes = ["TWF", "HDF", "PWF", "OSF", "RNF"]
    print(df[failure_modes].sum())

    print("\n--- NUMERIC SUMMARY ---")
    print(df.describe().T)


if __name__ == "__main__":
    main()
