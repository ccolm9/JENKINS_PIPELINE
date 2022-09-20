from utils.import_xlsx import Import
import pandas as pd
import os
import glob

if __name__ == "__main__":

    DATA_PATH = "data/"

    data_reader = Import()
    result = data_reader.ingest_feature_data(data_path=DATA_PATH)
    print(result.head())
