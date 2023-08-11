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

    def data_visualisation(self):
        # Create a figure with two subplots arranged vertically and set the overall figure size
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10))

        # Plotting the first plot showing median values by food elements (ax1)
        nutr_data = self.get_nutrients()
        
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.db


if __name__ == "__main__":
    try:
        usafood = UsaFood(
            db=json.load(
                open(
                    "/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/usa_food/usafood_db.json"
                )
            )
        )
        # usafood.__repr__()
        usafood.get_nutrients()
        # usafood.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
