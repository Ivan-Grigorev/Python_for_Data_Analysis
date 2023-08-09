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

    def total_births_count(self):
        total_births = self.names.pivot_table(
            values='birth',
            index='year',
            columns='sex',
            aggfunc='sum'
        )
        return total_births

    def data_visualisation(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(13, 10))

        # Plotting total births (ax1)
        total_data = self.total_births_count()

        # Rearrange data for plotting
        total_data = total_data.stack()
        total_data.name = 'births'
        total_data = total_data.reset_index()

        sns.barplot(
            y='births',
            x='year',
            hue='sex',
            data=total_data,
            ax=ax1,
            palette={'F': 'pink', 'M': 'blue'}
        )
        ax1.set_title('Total births by sex and year.')

        # Add exact birth number as plot label
        for container in ax1.containers:
            ax1.bar_label(
                container,
                [round(rect._height / 1000000, 2) for rect in container],  # Round values to 2 decimal places
            )

        # Set y-axis limits, ticks and tick labels
        ax1.set_ylim(0, 2500000)
        ax1.set_yticks(range(0, 3000000, 500000))
        ax1.set_yticklabels(range(0, 3000000, 500000))

        # ax2

        plt.suptitle(
            'Baby names in USA for the period from 1880 to 2010',
            fontsize=18,
            fontweight='bold'
        )
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.names


if __name__ == "__main__":
    try:
        # Get all data from datasets/babynames folder in one DataFrame
        # Create a list of DataFrames for each year
        pieces = [
            pd.read_csv(
                f"/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/babynames/yob{year}.txt",
                names=["name", "sex", "birth"],  # Add columns to DataFrame
            ).assign(year=year)  # Add the 'year' column to DataFrame
            for year in range(1880, 2011, 10)  # Loop over each 10 years from 1880 to 2011
        ]

        # Collect all data in one DataFrame
        names = pd.concat(pieces, ignore_index=True)

        babynames = BabyNames(
            names_df=names
        )
        # print(babynames.__repr__())
        babynames.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
