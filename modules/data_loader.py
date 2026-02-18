import pandas as pd

def load_data(path="data/sample_esg_data.csv"):
    return pd.read_csv(path)
