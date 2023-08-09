import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set pandas display output options
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


class BabyNames:
    def __init__(self, names_df):
        self.names = names_df

    def __repr__(self):
        return self.names


if __name__ == "__main__":
    try:
        # Create a list of DataFrames for each year
        pieces = [
            pd.read_csv(
                f"/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/babynames/yob{year}.txt",
                names=["name", "sex", "birth"],  # Add columns to DataFrame
            ).assign(year=year)  # Add the 'year' column to DataFrame
            for year in range(1880, 2011)  # Loop over the years from 1880 to 2011
        ]

        # Collect all data in one DataFrame
        names = pd.concat(pieces, ignore_index=True)

        babynames = BabyNames(names_df=names)
        print(babynames.__repr__())

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
