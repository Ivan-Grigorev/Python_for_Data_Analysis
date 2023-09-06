import geopandas as gpd
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
        self.data = self.data.loc[
            (self.data["contbr_st"].isin(usa_codes)) &
            (self.data["cand_nm"].isin(["Obama, Barack", "Romney, Mitt"]))
        ]

        # Calculate the total donations amount by state and candidate
        donations_by_st = self.data.pivot_table(
            values="contb_receipt_amt",
            index="contbr_st",
            columns="cand_nm",
            aggfunc="sum",
            dropna=True,
            fill_value=0,
        )

        # Filter donations by state to get states where Barack Obama donations exceeded Romney Mitt
        obama_states = donations_by_st[
            donations_by_st["Obama, Barack"] > donations_by_st["Romney, Mitt"]
        ].index.tolist()  # Get only states codes as list

        # Filter donations by state to get states where Romney Mitt donations exceeded Barack Obama
        mitt_states = donations_by_st[
            donations_by_st["Romney, Mitt"] > donations_by_st["Obama, Barack"]
        ].index.tolist()  # Get only states codes as list

        return donations_by_st, obama_states, mitt_states

    def data_visualization(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))

        # Plotting first plot shows donations values (ax1)
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
        ax1.set_title("Total donations by parties for different occupation types (Millions USD)")

        # Create custom legend handles with the correct colors
        ax1.legend(
            title="Parties",
            labels=["Democratic", "Republican"],
            handles=[
                plt.Line2D([0], [0], color=sns.color_palette("deep")[i], lw=5)
                for i in range(2)
            ],
        )
        ax1.set_ylabel("Occupation type")
        ax1.set_xlabel(None)
        ax1.set_xticks(range(0, 31, 5))
        ax1.set_xticklabels(range(0, 31, 5))
        ax1.set_xlim(0, 30)

        # Plotting second plot shows donations per state for main candidates (ax2)
        donations_data_by_st, obamas_states_data, romneys_states_data = self.get_donations_by_state()

        # Load USA boundaries data
        states_map_data = gpd.read_file(
            "/Users/a1/PythonProjects/Python_for_Data_Analysis/"
            "fec/geopandas_data/usa-states-census-2014.shp"
        )

        # Create a Geopandas USA map as ax2
        states_map = states_map_data.boundary.plot(linewidth=0.5, color="Black", ax=ax2)
        # Add USA codes to map
        states_map_data.apply(
            lambda x: ax2.annotate(
                text=x.STUSPS,
                xy=x.geometry.centroid.coords[0],
                ha="center",
                fontsize=7,
                color="white",
            ),
            axis=1,
        )

        # Plot the USA states with exact candidate colors
        obamas_states = states_map_data[states_map_data["STUSPS"].isin(obamas_states_data)]
        romneys_states = states_map_data[states_map_data["STUSPS"].isin(romneys_states_data)]
        obamas_states.plot(ax=states_map, color="#4C72B0")  # Obama's states in blue
        romneys_states.plot(ax=states_map, color="#DE844E")  # Romney's states in orange

        ax2.set_title("USA Map: States colored by candidate's top donations")
        # Remove axis labels and ticks from ax2
        ax2.axis("off")

        # Plotting third plot shows donations amount by state (ax3)
        # Divide donation to get millions numbers
        donations_data_by_st = donations_data_by_st / 1000000

        # Rearrange data for plotting
        donations_data_by_st = donations_data_by_st.stack()
        donations_data_by_st.name = "value"
        donations_data_by_st = donations_data_by_st.reset_index()

        # Create bar plot ax3
        sns.barplot(
            x="contbr_st",
            y="value",
            hue="cand_nm",
            data=donations_data_by_st,
            ax=ax3,
        )

        ax3.set_title("Candidate donations per State (Millions USD)")
        # Create custom legend handles with the correct colors
        ax3.legend(
            title="Candidates",
            labels=["Barack Obama", "Mitt Romney"],
            handles=[
                plt.Line2D([0], [0], color=sns.color_palette("deep")[i], lw=5)
                for i in range(2)
            ],
        )
        ax3.set_ylabel("Millions USD")
        ax3.set_ylim(0, 30)
        ax3.set_yticks(range(0, 31, 5))
        ax3.set_yticklabels(range(0, 31, 5))
        ax3.set_xlabel("USA")

        # Add donation amount as plot label
        for container in ax3.containers:
            ax3.bar_label(container, fmt="%.3f", fontsize=6, rotation=90, fontweight="bold")

        plt.suptitle("The Federal Election Commission Database", fontsize=18, fontweight="bold")
        plt.tight_layout()
        # Save figure to file
        # plt.savefig('fec_visualization.pdf', dpi=300, bbox_inches='tight')
        plt.show()

    def __repr__(self):
        return self.data


if __name__ == "__main__":
    try:
        fed_el_comm = FedElectComm(
            dataset=pd.read_csv(
                "/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/fec/fec_dataset.csv",
                low_memory=False,
            )
        )
        fed_el_comm.data_visualization()
    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
