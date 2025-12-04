#################
# Modules imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import regex
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
np.random.seed(42)
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


############################################################
# Plotting the selection bias according to the input dataset
def plot_selection(dataset_path:str,
                   save_fig:bool = True,
                   grouped_by:list = None,
                   metadata_split:str = None,
                   rename_xaxis:str = None,
                   xjitter:bool=False):
    """
    dataset : str -> Path of the source dataset (output of the 'selection_pressure.R' script).
    save_fig : bool -> to save the figure? if True the figure will be saved into 'output/py_figures' folder.
    grouped_by : list -> Found in the config.json, according to which metadata to order the plot.
    metadata_split : str - > Name of the metadata we grouped the data by, in this case antibody target (ab_target).
    rename_xaxis : str -> String to rename x-axis in the plot (xlabel).
    jitter : bool -> If True the x-axis values will be jittered for clearer visualization.
    """

    # Importing the dataset
    dataset = pd.read_csv(dataset_path, index_col=0)

    # Importing the metadata list, if single value than it will be the only object in the list
    try: 
        metadata_list = read_json()["metadata_list"].split(",")
        grouped_by2 = metadata_list[1]

    except:
        metadata_list = [read_json()["metadata_list"]]
        grouped_by2 = metadata_list[0]

    metadata_list = [i for i in metadata_list if i in dataset.columns]
    dataset[metadata_list] = dataset[metadata_list].astype("str")
    dataset = dataset.sort_values(metadata_list)

    #if user defined grouped by column by the grouped by argument
    if grouped_by is not None:
        metadata_list = grouped_by
        grouped_by2 = metadata_list[0]

    
    # Defining label if subject are united
    x_label = metadata_list[0]
    if "subject_id" in metadata_list:
        try:
            x_label = "subject_id"
            dataset.subject_id = dataset.subject_id.apply(lambda X : f"Subject {X.split("_")[-1]}")
        except:
            print("Dataset was not grouped by 'subject_id', attempting to use the second grouped by value.")

    unique_x = dataset[x_label].unique()
    number_x = len(unique_x)
    

    # Defining Borders of the baseline points
    dataset.baseline_ci_upper = (dataset.baseline_sigma.abs() - dataset.baseline_ci_upper.abs()).abs()
    dataset.baseline_ci_lower = (dataset.baseline_sigma.abs() - dataset.baseline_ci_lower.abs()).abs()

    # Calcualting the required y axis limit for the plot (highest order + 10%)
    max = pd.concat([dataset.baseline_sigma.abs() + dataset.baseline_ci_lower.abs(),
                     dataset.baseline_sigma.abs() + dataset.baseline_ci_upper.abs()]).max().round(1)
    y_limit_border = round((max + max*0.1), 1)

    if y_limit_border < 1.5:
        y_limit_border = 1

    # Getting unique values for region and subjects
    regions = dataset.region.unique()
    target_unique = dataset[grouped_by2].unique()

    # Creating figure object
    fig = plt.figure(figsize = (7, 10))
    gs = fig.add_gridspec(len(regions)-1, hspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    colors = list(mcolors.TABLEAU_COLORS)

    # Itirating over the different conditions and plotting the results
    for region in range(1, len(regions[1:])+1):     
        for target, cl in zip(target_unique, range(0, len(colors))):
            ax_index = region - 1
              
            # Getting dataset for specific region in specific ab_target (this case).
            cond_region = (dataset.region == regions[region])
            cond_target = (dataset[grouped_by2] == target)
            
            if type(metadata_list) != list:
                metadata_list = [metadata_list]

            temp_dataset = dataset.loc[(cond_region & cond_target), metadata_list + list(dataset.columns[-4:])]

            if __name__ == "__main__":
                print(region, regions[region], target, cl, x_label)
                print(f"X-axis: {temp_dataset[x_label].values} ")
                print(f"Y-axis: {temp_dataset["baseline_sigma"].values} ")

            if xjitter is True:
                len_x = temp_dataset[x_label].values.shape[0]
                og_val = cl
                x_input = jitter(len_x, og_val)

            else:
                x_input = temp_dataset[x_label]

            # Plottig each sub-dataset
            axs[ax_index].errorbar(x= x_input,
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
            
            # Resetting x-labels if jitter is applied
            if xjitter is True:
                # Setting initial x-axis labels
                xaxis_ph = np.arange(-1, number_x)
                axs[ax_index].set_xticks(xaxis_ph)

                # Creating the x-labels
                tlist = unique_x
                tdict = {i:j for i,j in zip(range(0,len(tlist)),tlist)}
                final_list = [""] + [tdict[i] if i in tdict else "" for i in xaxis_ph[1:]]
        
                # Setting the updated x-lbals
                axs[ax_index].set_xticklabels(final_list)

            # Region label
            axs[ax_index].text(y=0, x=number_x +0.1, s=regions[region], size=15, rotation=-90)

            # Modifing the plot parameters
            axs[ax_index].axhline(y=0, ls="--", color="grey")
            y_ticks_array = get_symticks(y_limit_border)
            axs[ax_index].set_yticks(np.linspace(-y_limit_border, y_limit_border, 7).round(1))
            ####axs[ax_index].set_ylim(-y_limit_border, y_limit_border)

            # Defining limits of x-axis bases on number of columns
            axs[ax_index].set_xlim( -1 , number_x)
            axs[ax_index].tick_params(axis="y", labelsize=10)

            # Making the first and last major ticks inivisible      
            y_ticks = axs[ax_index].yaxis.get_major_ticks()
            y_ticks[0].set_visible(False) ## set first x tick label invisible
            y_ticks[-1].set_visible(False) ## set last x tick label invisible
    
    if isinstance(rename_xaxis, str):
        x_label = rename_xaxis

    axs[-1].set_xlabel(x_label, fontsize=12)

    # Setting title legend
    if metadata_split is None:
        leg_title = grouped_by2
    else:
        leg_title = metadata_split
    
    # Figure parameters
    fig.supylabel("Selection Pressure Bias (Σ)", size=12)
    ax_h, ax_l = axs[0].get_legend_handles_labels()
    fig.legend(ax_h, 
               target_unique, 
               ncols=2, 
               loc="upper center", 
               bbox_to_anchor=(0.55,1.05), 
               fontsize=10, 
               title=leg_title,
               title_fontsize=12)
    
    plt.tight_layout()

    # Saving the figure
    if save_fig:
        output_path = "output\\py_figures"

        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
            print(f"{output_path} folder was created.")
        
        regex_pattern = r"\\r_data\\([\w\[\]\-]+).csv"
        name = regex.findall(regex_pattern, dataset_path)[0]

        plt.savefig(f"{output_path}\\{name}.png",  bbox_inches='tight')
        print(f"Plot saves as {name}")

    plt.show()

    return dataset


###########################################################
# Calculating the number of clones per defined sub-datasets
class nclones_report():
    
    # Loading the class with the input dataframe used in the selection bias analysis
    def __init__(self, 
                 dataset_name :str):
        """
        dataset_input : str -> Name of the sequences dataset including the '.csv' .
        """
        self.reports_path = "output\\py_reports"
        
        self.dataset_name = dataset_name
        self.csv_path = f"{read_json()["input_folder"]}\\{self.dataset_name}"
        self.dataset = pd.read_csv(self.csv_path, index_col=0)

    # Counting the number of unique clones per sub-dataset
    def groupby_count(self,
                      groupby_list :list,
                      save_reports :bool = True):
        """
        groupby_list : list -> list-like object which contains the columns names in order to group by.
        """
        
        dataset_gp =  self.dataset.groupby(groupby_list)
        self.gp_result = dataset_gp.agg({"clone_id":"nunique",}).reset_index()
        self.gp_result["seq_count"] = dataset_gp.size().reset_index()[0]
        self.gp_result.columns =  groupby_list + ["unique_clones","seq_count"]

        if save_reports:
            if os.path.exists(self.reports_path) is False:
                os.mkdir(self.reports_path)
                print(f"Report folder was created at {self.reports_path}")
        
            self.gp_result.to_csv(f"{self.reports_path}\\{self.dataset_name.split(".")[0]}_nclones.csv")

        return self.gp_result
    
    # Returning the sum of clones (all sub-datasets combined)
    def get_sum_clones(self):
        return self.gp_result.unique_clones.sum()