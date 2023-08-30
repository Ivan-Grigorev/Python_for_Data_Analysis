import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set Pandas display output options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


class FedElectComm:
    def __init__(self, dataset):
        self.data = dataset

    def get_party_affiliation(self):
        # Get candidate's party affiliation
        # Define candidate's affiliation in dictionary
        parties_affiliation = {
            "Bachmann, Michelle": "Republican",
            "Cain, Herman": "Republican",
            "Gingrich, Newt": "Republican",
            "Huntsman, Jon": "Republican",
            "Johnson, Gary Earl": "Republican",
            "McCotter, Thadeus G": "Republican",
            "Obama, Barack": "Democrat",
            "Paul, Ron": "Republican",
            "Pawlenty, Timothy": "Republican",
            "Perry, Rick": "Republican",
            "Roemer, Charles E. 'Buddy' III": "Republican",
            "Romney, Mitt": "Republican",
            "Santorum, Rick": "Republican",
        }

        # Add to DataFrame column 'party' with candidate's affiliation
        self.data["party"] = self.data["cand_nm"].map(parties_affiliation)

        return self.data

    def get_donations_by_occupation(self):
        # Get handled data from get_party_affiliation function
        data = self.get_party_affiliation()

        # Dictionary for cleaning occupation values in the DataFrame
        occ_mapping = {
            "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
            "INFORMATION REQUESTED": "NOT PROVIDED",
            "INFORMATION REQUESTED (BEST EFFORTS)": "NOT PROVIDED",
            "C.E.O.": "CEO",
        }

        # Clean column in DataFrame with occupation data
        data["contbr_occupation"] = data["contbr_occupation"].map(
            lambda x: occ_mapping.get(x, x)
        )

        # Dictionary for cleaning employment type values in the DataFrame
        emp_mapping = {
            "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
            "INFORMATION REQUESTED": "NOT PROVIDED",
            "SELF": "SELF-EMPLOYED",
            "SELF EMPLOYED": "SELF-EMPLOYED",
        }

        # Clean column in DataFrame with employment type data
        data["contbr_employer"] = data["contbr_employer"].map(
            lambda x: emp_mapping.get(x, x)
        )

        # Create pivot table with all donations amount by occupation
        occupation_donations = data.pivot_table(
            values="contb_receipt_amt",
            index="contbr_occupation",
            columns="party",
            aggfunc="sum",
            dropna=True,
            fill_value=0,
        )

        # Filter all donations table by values increase 1 million USD
        highest_donations = occupation_donations[
            occupation_donations.sum(axis=1) > 1000000
        ]

        return highest_donations

    def get_donations_by_state(self):
        # United States of America codes
        usa_codes = [
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ]
        # Filter data by main candidates and states
        self.data = self.data.loc[(self.data['contbr_st'].isin(usa_codes)) &
                                   (self.data['cand_nm'].isin(['Obama, Barack', 'Romney, Mitt']))]

        # Calculate the total donations amount by state and candidate
        donations_by_st = self.data.pivot_table(
            values='contb_receipt_amt',
            index='contbr_st',
            columns='cand_nm',
            aggfunc='sum',
            dropna=True,
            fill_value=0
        )

        return donations_by_st

    def data_visualization(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))

        # Plotting first plot showing donations values (ax1)
        donations_data_by_occ = self.get_donations_by_occupation()
        # Divide donation amount to get millions numbers
        donations_data_by_occ = donations_data_by_occ / 1000000

        # Rearrange data for plotting
        donations_data_by_occ = donations_data_by_occ.stack()
        donations_data_by_occ.name = "value"
        donations_data_by_occ = donations_data_by_occ.reset_index()

        # Create seaborn bar plot
        sns.barplot(
            x="value",
            y="contbr_occupation",
            hue="party",
            data=donations_data_by_occ,
            ax=ax1,
        )

        # Add value as plot label
        for container in ax1.containers:
            ax1.bar_label(container, fmt="%.3f", fontsize=6, fontweight="bold")

        # Set ax1 title and labels options
        ax1.set_title("Amount of donations by parties for occupation types (Millions USD)")
        ax1.set_ylabel("Occupation type")
        ax1.set_xlabel(None)
        ax1.set_xticks(range(0, 31, 5))
        ax1.set_xticklabels(range(0, 31, 5))
        ax1.set_xlim(0, 30)

        # Plotting second plot showing donations per state for main candidates
        donations_data_by_st = self.get_donations_by_state()
        # Divide donation to get millions numbers
        donations_data_by_st = donations_data_by_st / 1000000

        sns.heatmap(
            data=donations_data_by_st,
            annot=True,
            cmap=False,
            ax=ax2
        )

        plt.suptitle(
            "The Federal Election Commission Database",
            fontsize=18,
            fontweight="bold")
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.data.info()


if __name__ == "__main__":
    try:
        fed_el_comm = FedElectComm(
            dataset=pd.read_csv(
                "/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/fec/fec_dataset.csv",
                low_memory=False,
            )
        )
        # print(fed_el_comm.__repr__())
        print(fed_el_comm.data_visualization())
    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
