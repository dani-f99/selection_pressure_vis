import numpy as np
import pandas as pd
import json
import os


# Reading information from json file. Used to extract the parameters from the config.json.
def read_json(path:str = "config.json") -> dict:
    """
    path : str -> path of the json file
    """

    with open('config.json') as config:
        config_f = json.load(config)

    return config_f


# Returning list of all the csv files in a folder with their complete path
def list_datasets(path:str = f"{read_json()["output_folder"]}\\r_data") -> list:
    """   
    path : str -> path of the folder
    """

    raw_list = os.listdir(path)
    csv_files = [i for i in raw_list if i.split(".")[1] == "csv"]
    
    print(f"{len(csv_files)} datasets found in {path}r_data:")
    for i in csv_files:
        print(i)
    
    return [f"{path}r_data\\{i}" for i in csv_files]
