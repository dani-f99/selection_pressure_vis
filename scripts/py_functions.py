import numpy as np
import pandas as pd
import regex
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
    
    return [f"{path}\\{i}" for i in csv_files]

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# Plotting the selection bias according to the input dataset
def plot_selection(dataset_path:str,
                   save_fig:bool = True,
                   grouped_by:list = None,
                   metadata_split:str = None):
    """
    dataset : str -> Path of the source dataset (output of the 'selection_pressure.R' script).
    save_fig : bool -> to save the figure? if True the figure will be saved into 'output/py_figures' folder.
    grouped_by : list -> Found in the config.json, according to which metadata to order the plot.
    metadata_split : Name of the metadata we grouped the data by, in this case antibody target (ab_target).
    """

    # Getting the metadata column names from the config, if there was no user input.
    if grouped_by is None:
        try:
            metadata_list = read_json()["metadata_list"].split(",")
            grouped_by2 = metadata_list[1]

        except:
            metadata_list = read_json()["metadata_list"]
            grouped_by2 = metadata_list


    # Importing the dataset
    dataset = pd.read_csv(dataset_path, index_col=0)
    dataset.subject_id = dataset.subject_id.apply(lambda X : f"Subject {X.split("_")[-1]}")

    # Defining Borders of the baseline points
    dataset.baseline_ci_upper = (dataset.baseline_sigma - dataset.baseline_ci_upper).apply(abs)
    dataset.baseline_ci_lower = (dataset.baseline_sigma - dataset.baseline_ci_lower).apply(abs)

    # Getting unique values for region and subjects
    regions = dataset.region.unique()
    subjects = dataset.subject_id.unique()

    # Creating figure object
    fig = plt.figure(figsize = (1.5*len(subjects), 2.5*len(regions)))
    gs = fig.add_gridspec(len(regions)-1, hspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    colors = list(mcolors.TABLEAU_COLORS)

    # Itirating over the different conditions and plotting the results
    for region in range(1, len(regions[1:])+1):       
        for target, cl in zip(dataset[grouped_by2].unique(), range(0, len(colors))):
            ax_index = region - 1

            if __name__ == "__main__":
                print(region, regions[region], target, cl)

            # Getting dataset for specific region in specific ab_target (this case).
            cond_region = (dataset.region == regions[region])
            cond_target = (dataset[grouped_by2] == target)
            temp_dataset = dataset.loc[(cond_region & cond_target), metadata_list + list(dataset.columns[-4:])]

            # Plottig each sub-dataset
            axs[ax_index].errorbar(x=temp_dataset["subject_id"],
                                   y=temp_dataset["baseline_sigma"],
                                   yerr=temp_dataset[["baseline_ci_lower","baseline_ci_upper"]].T.values,
                                   linestyle="",
                                   marker= "o",
                                   color=colors[cl],
                                   markersize=10,
                                   markeredgecolor="black",
                                   alpha=0.75,
                                   ecolor="black",
                                   capsize=10,
                                   label=target)
            
            axs[ax_index].text(y=0.8,x=-0.15, s=regions[region], size=15)

            # Modifing the plot parameters
            axs[ax_index].axhline(y=0, ls="--", color="grey")
            axs[ax_index].set_ylim(-1,1) 
            axs[ax_index].tick_params(axis="y", labelsize=10)

            # Making the first and last major ticks inivisible      
            y_ticks = axs[ax_index].yaxis.get_major_ticks()
            y_ticks[0].label1.set_visible(False) ## set first x tick label invisible
            y_ticks[-1].label1.set_visible(False) ## set last x tick label invisible


    # Setting title legend
    if metadata_split is None:
        leg_title = grouped_by2
    else:
        leg_title = metadata_split
    
    # Figure parameters
    fig.supylabel("Selection Pressure Bias (Σ)", size=18)
    fig.supxlabel("Subject", size=18)
    ax_h, ax_l = axs[0].get_legend_handles_labels()
    fig.legend(ax_h, ["Spike Negative", "Spike Positive"], 
               ncols=2, 
               loc="upper center", 
               bbox_to_anchor=(0.55,1.05), 
               fontsize=13, 
               title=leg_title,
               title_fontsize=15)
    plt.tight_layout()

    # Saving the figure
    if save_fig:
        output_path = "output\\py_figures"

        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
            print(f"{output_path} folder was created.")
        
        regex_pattern = r"\\r_data\\([\w\[\]\-]+).csv"
        name = regex.findall(regex_pattern, dataset_path)[0]

        plt.savefig(f"{output_path}\\{name}.png")
        print(f"Plot saves as {name}")

    plt.show()

    return dataset
