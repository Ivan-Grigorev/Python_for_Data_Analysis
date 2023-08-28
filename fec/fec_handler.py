import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set Pandas display output options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class FedElectComm:
    def __init__(self, dataset):
        self.data = dataset

    def __repr__(self):
        return self.data.head()


if __name__ == '__main__':
    try:
        fed_el_comm = FedElectComm(
            dataset=pd.read_csv(
                "/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/fec/fec_dataset.csv",
                low_memory=False
            )
        )
        print(fed_el_comm.__repr__())
    except FileNotFoundError as err:
        print(f'{err.strerror}: {err.filename}')
