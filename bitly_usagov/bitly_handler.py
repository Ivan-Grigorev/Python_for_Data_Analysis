import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set NumPy print precision to 4 decimal.
np.set_printoptions(precision=4)

# Set default figure size for matplotlib plots.
plt.rc("figure", figsize=(13, 8))

# Set maximum number of rows to display in pandas DataFrame.
pd.set_option("display.max_rows", 100)


class BitlyUsaGov:
    def __init__(self, path):
        # Get data from file.
        self.records = [json.loads(line) for line in open(path)]
        # Get all time zones from data.
        self.time_zones = [rec["tz"] for rec in self.records if "tz" in rec]

    def time_zone_count(self):
        # Count time zones in dateset.
        df = pd.DataFrame(self.records)

        # Clean data.
        clean_tz = df["tz"].dropna()
        clean_tz = clean_tz[clean_tz != ""]
        tz_counts = clean_tz.value_counts()

        return tz_counts.head(10)

    def users_browser_count(self):
        df = pd.DataFrame(self.records)

        # Remove rows with an empty 'tz' column values.
        df = df[df["tz"] != ""]

        # Get 'Windows' browser users.
        cframe = df[df.a.notnull()]
        cframe = cframe.copy()
        cframe["os"] = np.where(
            cframe["a"].str.contains("Windows"), "Windows", "Not Windows"
        )

        # Group DataFrame by time zones.
        by_tz_os = cframe.groupby(["tz", "os"])

        # Create table.
        agg_counts = by_tz_os.size().unstack().fillna(0)

        # Compute 'total' column.
        agg_counts["total"] = agg_counts.sum(axis=1)

        # Get 10 largest amount using nlargest() and keep as DataFrame.
        count_subset = agg_counts.nlargest(10, "total")

        # Rearrange data for plotting.
        count_subset = count_subset.stack()
        count_subset.name = "total"
        count_subset = count_subset.reset_index()
        # Remove from table 'total' rows.
        count_subset = count_subset[count_subset["os"] != "total"]

        # Calculate normalized total within each time zone.
        results = count_subset.groupby("tz").apply(
            lambda x: x.assign(normed_total=x.total / x.total.sum())
        )
        return count_subset, results

    def data_visualisation(self):
        # Create a single figure with three subplots stacked vertically.
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

        # Plotting the first bar plot on the first subplot (ax1).
        t_z_c = self.time_zone_count()
        sns.barplot(y=t_z_c.index, x=t_z_c.values, ax=ax1)
        ax1.set_title("First ten time zones from dataset 1.usa.gov")

        # Plotting the second bar plot on the second subplot (ax2).
        c_s, res = self.users_browser_count()
        sns.barplot(x="total", y="tz", hue="os", data=c_s, ax=ax2)
        ax2.set_title("First ten time zones highlighting Windows and other users")

        # Plotting the third bar plot on the third subplot (ax3).
        sns.barplot(x="normed_total", y="tz", hue="os", data=res, ax=ax3)
        ax3.set_title("Percentage of Windows and other users in first ten time zones")

        plt.suptitle("usa.gov data from Bitly", fontsize=18, fontweight="bold")
        plt.tight_layout()
        # Save figure to a file
        # plt.savefig("bitly_visualisation.png", dpi=300, bbox_inches="tight")
        plt.show()

    def __repr__(self):
        return self.records


if __name__ == "__main__":
    try:
        usagov = BitlyUsaGov(
            # Path to dataset file.
            path="/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/bitly/example.txt"
        )
        usagov.time_zone_count()
        usagov.users_browser_count()
        usagov.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
