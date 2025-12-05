#################
# Modules imports
import numpy as np
import json
import os


##########################################################################################
# Reading information from json file. Used to extract the parameters from the config.json.
def read_json(path:str = "config.json") -> dict:
    """
    path : str -> path of the json file
    """

    with open('config.json') as config:
        config_f = json.load(config)

    return config_f


##########################################################################
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
    
    return [f"{path}\\{i}" for i in csv_files]


##################################################################################################
# Getting array of number based on given input, used to create y ticks based on the maximal number
def get_symticks(nval: float) -> np.array:
    """
    nval : float -> numerical value
    """
    abs_nval = abs(nval)
    abs_max = abs_nval
    pos_range = np.arange(-abs_nval, abs_max, 0.75)
    y_ticks = np.sort(np.concat((-pos_range[1:],pos_range)))

    return y_ticks


####################################################
# Return jittered array, can be used as x-axis input
def jitter(array_size : int,
           array_n : int) -> np.array:
    """
    array_size: int -> length of the 1 array to be jittered
    array_n : int -> value of the arary to be jittered
    """
    rng = np.random.default_rng(seed=42)


    if array_n == 0:
        random_multi = rng.uniform(low=-0.2, high=0.2, size=(1, array_size))

    else:
        random_multi = rng.uniform(low=0.8, high=1.2, size=(1, array_size)) 
        random_multi = random_multi * np.ones(array_size) * array_n
    
    return random_multi[0]