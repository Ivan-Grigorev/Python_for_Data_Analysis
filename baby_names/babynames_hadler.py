import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Set pandas display output options
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


class BabyNames:
    def __init__(self, names_df):
        self.names = names_df

    def total_births_count(self):
        # Count total births
        total_births = self.names.pivot_table(
            values="birth",
            index="year",
            columns="sex",
            aggfunc="sum"
        )
        return total_births

    def names_popularity_count(self):
        # Filter DataFrame by Gender (Male) and Popularity (minimum one name per day in year)
        popular_boys_names = self.names.loc[(self.names["sex"] == "M") &
                                            (self.names["birth"] >= 365)]

        # Filter DataFrame by Gender (Female) and Popularity (minimum one name per day in year)
        popular_girls_names = self.names.loc[(self.names["sex"] == "F") &
                                             (self.names["birth"] >= 365)]

        # Create a table of popular boys' names by each year
        count_boys_names = popular_boys_names.pivot_table(
            values="birth",
            index="name",
            columns="year",
            aggfunc="max",
            dropna=True,
            fill_value=0,
        )

        # Create a table of popular girls' names by each year
        count_girls_names = popular_girls_names.pivot_table(
            values="birth",
            index="name",
            columns="year",
            aggfunc="max",
            dropna=True,
            fill_value=0,
        )

        # Filter a tables of popular girls' and boys' names and get most popular
        count_boys_names = count_boys_names.loc[count_boys_names.idxmax()].drop_duplicates()
        count_girls_names = count_girls_names.loc[count_girls_names.idxmax()].drop_duplicates()

        return count_boys_names, count_girls_names

    def data_visualisation(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(13, 10))

        # Plotting total births (ax1)
        total_data = self.total_births_count()

        # Rearrange data for plotting
        total_data = total_data.stack()
        total_data.name = "births"
        total_data = total_data.reset_index()

        sns.barplot(
            y="births",
            x="year",
            hue="sex",
            data=total_data,
            ax=ax1,
            palette={"F": "pink", "M": "blue"},
        )
        ax1.set_title("Total births by sex and year.")

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

        # Plotting most popular names per each day (ax2, ax3)
        # Get the handled data from names_popularity_count()
        boys_names_data, girls_names_data = self.names_popularity_count()

        # Get the number of most popular boys and girls names by each day in year
        boys_names_data = boys_names_data / 365
        girls_names_data = girls_names_data / 365

        # Rearrange data for plotting
        boys_names_data = boys_names_data.stack()
        boys_names_data.name = "births"
        boys_names_data = boys_names_data.reset_index()

        girls_names_data = girls_names_data.stack()
        girls_names_data.name = "births"
        girls_names_data = girls_names_data.reset_index()

        # Define a dictionary to map names to colors
        names_color_mapping = {
            "boys": {
                "John": "blue",
                "Robert": "green",
                "James": "orange",
                "David": "red",
                "Michael": "brown",
                "Jacob": "cyan",
            },
            "girls": {
                "Mary": "pink",
                "Linda": "magenta",
                "Jennifer": "yellow",
                "Jessica": "purple",
                "Emily": "lightblue",
                "Isabella": "lavender",
            },
        }

        # Create a bar plot (ax2)
        sns.barplot(
            x="year",
            y="births",
            hue="name",
            data=boys_names_data,
            ax=ax2,
            palette=names_color_mapping["boys"].values(),
            width=0.9,
        )

        # Custom legend using dictionary (ax2)
        handles = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=color,
                markersize=10,
                label=name,
            )
            for name, color in names_color_mapping["boys"].items()
        ]
        ax2.legend(handles=handles, title="Names", loc="upper left")

        # Set title for ax2
        ax2.set_title("The number of most popular boys names given per day")

        # Add exact birth number as plot label (ax2)
        for container in ax2.containers:
            ax2.bar_label(container, fmt="%.0f", fontsize=7)

        # Set y-axis limits, ticks and tick labels (ax2)
        ax2.set_ylim(0, 250)
        ax2.set_yticks(range(0, 300, 50))
        ax2.set_yticklabels(range(0, 300, 50))

        # Create a bar plot (ax3)
        sns.barplot(
            x="year",
            y="births",
            hue="name",
            data=girls_names_data,
            ax=ax3,
            palette=names_color_mapping["girls"].values(),
            width=0.9,
        )

        # Custom legend using dictionary (ax3)
        handles = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=color,
                markersize=10,
                label=name,
            )
            for name, color in names_color_mapping["girls"].items()
        ]
        ax3.legend(handles=handles, title="Names", loc="upper left")

        # Set title for ax3
        ax3.set_title("The number of most popular girls names given per day")

        # Add exact birth number as plot label (ax3)
        for container in ax3.containers:
            ax3.bar_label(container, fmt="%.0f", fontsize=7)

        # Set y-axis limits, ticks and tick labels (ax3)
        ax3.set_ylim(0, 250)
        ax3.set_yticks(range(0, 300, 50))
        ax3.set_yticklabels(range(0, 300, 50))

        plt.suptitle(
            "Baby names in USA for the period from 1880 to 2010",
            fontsize=18,
            fontweight="bold",
        )
        plt.tight_layout()
        # Save the figure to a file
        # plt.savefig("babynames_usa.pdf", dpi=300, bbox_inches="tight")
        plt.show()

    def __repr__(self):
        return self.names


if __name__ == "__main__":
    try:
        # Get all data from datasets/babynames folder in one DataFrame
        # Create a list of DataFrames for each year
        pieces = [
            pd.read_csv(
                f"../datasets/babynames/yob{year}.txt",
                names=["name", "sex", "birth"],  # Add columns to DataFrame
            ).assign(year=year)  # Add the 'year' column to DataFrame
            for year in range(1880, 2011, 10)  # Loop over each 10 years from 1880 to 2011
        ]

        # Collect all data in one DataFrame
        names = pd.concat(pieces, ignore_index=True)

        babynames = BabyNames(names_df=names)
        # print(babynames.__repr__())
        babynames.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
