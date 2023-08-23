import json
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
import seaborn as sns


# Set Pandas display output options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# Define color thresholds and corresponding Seaborn heatmap colors
HEATMAP_COLORS = {
    (750.0,): "red",
    (500.0,): "purple",
    (200.0,): "pink",
    (50.0,): "orange",
    (10.0,): "yellow",
    (1.0,): "blue",
}


class UsaFood:
    def __init__(self, db):
        self.db = db

    def get_nutrients(self):
        # Create a DataFrame with specific columns for extraction
        info = pd.DataFrame(
            self.db, columns=["description", "group", "id", "manufacturer"]
        )

        # Collect all products nutrients
        nutrients = [
            pd.DataFrame(rec["nutrients"]).assign(id=rec["id"])
            for rec in self.db
        ]

        # Concat all objects
        nutrients = pd.concat(nutrients, ignore_index=True)
        nutrients = nutrients.drop_duplicates()

        # Rename columns with the same names
        info = info.rename(
            columns={"description": "food", "group": "fgroup"},
            copy=False
        )
        nutrients = nutrients.rename(
            columns={"description": "nutrient", "group": "nutgroup"},
            copy=False
        )

        # Merge two DataFrames
        nutrients_data = pd.merge(nutrients, info, on="id", how="outer")

        return nutrients_data

    def get_vitamins_amount(self):
        data = self.get_nutrients()

        # Create table with all nutrients amount
        nutr_amount = data.pivot_table(
            values="value",
            index="fgroup",
            columns="nutrient",
            aggfunc=lambda x: np.percentile(x, 50),
            dropna=True,
            fill_value=0,
        )

        # Filter columns by Vitamins
        vit_amount = nutr_amount.filter(like="Vitamin", axis=1)

        return vit_amount

    def data_visualisation(self):
        # Create a figure with two subplots arranged vertically and set the overall figure size
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 11))

        # Plotting the first plot showing median values by food elements (ax1)
        nutr_data = self.get_nutrients()

        # Get grouped average nutrient values
        ave_nutr_data = nutr_data.groupby(["nutrient", "fgroup"])["value"].quantile(0.5)

        # Extract Zinc values for visualisation
        ave_nutr_zinc = ave_nutr_data["Zinc, Zn"].sort_values(ascending=False)

        # Create a bar plot for median zinc values by nutrient group
        sns.barplot(x=ave_nutr_zinc.values, y=ave_nutr_zinc.index, ax=ax1)
        ax1.set_title("Median zinc values in Food groups (mg per 100g)")
        ax1.set_xlabel("")
        ax1.set_xticklabels([])
        ax1.set_ylabel("Food group")

        # Add value as plot label
        for container in ax1.containers:
            ax1.bar_label(container, fmt="%.3f")

        # Plotting the second plot showing the vitamins amount in nutrients (ax2)
        vit_data = self.get_vitamins_amount()

        # Create the custom ListedColormap using the colors from HEATMAP_COLORS dictionary
        custom_cmap = ListedColormap(
            [next((color for key, color in HEATMAP_COLORS.items() if x >= key), "lightgray")
                for x in np.linspace(0, 1000, 1000)]
        )

        # Create a heatmap
        sns.heatmap(
            vit_data,
            annot=True,
            cmap=custom_cmap,
            fmt=".3f",
            vmin=0.0,
            vmax=1000.0,
            xticklabels=[
                "A (IU)",
                "A (RAE)",
                "B-12",
                "B-12 (added)",
                "B-6",
                "C",
                "D",
                "D (D2 + D3)",
                "D2",
                "D3",
                "E",
                "E (added)",
                "K",
            ],
            annot_kws={"fontsize": 7},
            linewidths=0.5,
            cbar_kws={"ticks": np.arange(0, 1050, 50)},
            ax=ax2,
        )

        ax2.set_title("Median Vitamins values in Food Groups (mg per 100g)")
        ax2.set_xlabel("Vitamins")
        ax2.set_ylabel("Food group")

        plt.suptitle(
            "U.S. Department of Agriculture Food Database Analysis",
            fontsize=18,
            fontweight="bold",
        )
        # Save figure to a file
        # plt.savefig("usafood_visualisation.png", dpi=300, bbox_inches="tight")
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.db


if __name__ == "__main__":
    try:
        usafood = UsaFood(
            db=json.load(
                open("/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/usa_food/usafood_db.json")
            )
        )
        usafood.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
