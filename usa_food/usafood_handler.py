import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set pandas display output options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


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
            columns={'description': 'food', 'group': 'fgroup'},
            copy=False
        )
        nutrients = nutrients.rename(
            columns={'description': 'nutrient', 'group': 'nutgroup'},
            copy=False
        )

        # Merge two DataFrames
        nutrients_data = pd.merge(nutrients, info, on='id', how='outer')

        return nutrients_data

    def get_vitamins_amount(self):
        data = self.get_nutrients()

        # Create table with all nutrients amount
        nutr_amount = data.pivot_table(
            values='value',
            index='nutrient',
            columns='fgroup',
            aggfunc='sum',
            dropna=True,
            fill_value=0
        )

        # Filter rows by Vitamins nutrients
        vit_amount = nutr_amount[nutr_amount.index.str.contains('Vitamin')]

        return vit_amount

    def data_visualisation(self):
        # Create a figure with two subplots arranged vertically and set the overall figure size
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10))

        # Plotting the first plot showing median values by food elements (ax1)
        nutr_data = self.get_nutrients()

        # Get grouped average nutrient values
        ave_nutr_data = nutr_data.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)

        # Extract Zinc values for visualisation
        ave_nutr_zinc = ave_nutr_data['Zinc, Zn'].sort_values(ascending=False)

        # Create a bar plot for median zinc values by nutrient group
        sns.barplot(x=ave_nutr_zinc.values, y=ave_nutr_zinc.index, ax=ax1)
        ax1.set_title('Median zinc values by nutrient group')

        # Plotting the second plot showing the vitamins amount in nutrients (ax2)
        vit_data = self.get_vitamins_amount()

        # Rearrange data for plotting
        vit_data = vit_data.stack()
        vit_data.name = 'value'
        vit_data = vit_data.reset_index()
        # Convert the 'value' column to numeric
        vit_data['value'] = pd.to_numeric(vit_data['value'])

        # Create a bar plot for vitamins values in nutrients
        sns.barplot(
            x='value',
            y='fgroup',
            hue='nutrient',
            data=vit_data,
            ax=ax2
        )
        ax2.set_title('Vitamin values in nutrient group')

        plt.suptitle(
            "U.S. Department of Agriculture Food Database Analysis",
            fontsize=18,
            fontweight="bold",
        )
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
        # usafood.__repr__()
        usafood.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
