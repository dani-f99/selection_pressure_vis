--------------------------------------------------------------------------------
                              SYSTEM IMMUNOLOGY LAB
                                Haifa University
                                 Daniel Fridman
                                      2025
--------------------------------------------------------------------------------


# PROJECT: Clonal Selection Pressure Analysis

## 1. OVERVIEW
This program utilizes the shazam and alakazam packages from the Immcantation framework 
to analyze the selection pressure of B-cell sequences. The pipeline assumes sequences 
have already been preprocessed and assigned to clones; please refer to the Immcantation 
tutorial for preprocessing guidance. Once the selection pressure analysis is complete, 
default visualizations are generated. Users may also run the optional Python step for 
advanced visualization.

## 2. PREREQUISITES
Please ensure the following modules are installed:

### Required R Packages:
- shazam 
- alakazam 
- jsonlite 

### Required Python Modules:
- Pandas 
- NumPy 
- Matplotlib 
- Seaborn 

## 3. CONFIGURATION (config.json)
Before running the analysis, configure the `config.json` file as follows: 

a. input_folder
   - Name of the input folder. 
   - Recommended to leave as default; the script will create this at first run. 

b. output_folder
   - name of the output folder. 
   - Recommended to leave as default; the script will create this at first run. 

c. metadata_list
   - List of metadata that will group the sequences data before the selection
     pressure analysis. 

d. seq_dataset
   - Name of the dataset containing the sequences (example: "seqs.csv"). 

e. time_point
   - Options: "all" or "sep". 
   - "all": Analyze all timepoints at once. 
   - "sep": Split the data for each time-point separately. 

## 4. USAGE GUIDE
1. Configure the `config.json` file as needed (see section above). 
2. Run the `selection_pressure.R` script, preferably on a server. 
3. Run the `selection_visualization.ipynb` for better graphic visualization of
  the results. 

## 5. DIRECTORY STRUCTURE
The program uses the following folder structure: 

- input/  : Input folder. 
- output/ : Result output, tables to be used in the LPA program. 
           - output/r_figures : Generated figures. 
           - output/r_data    : Generated data files. 
		   
## 6. RESOUCES
- Immcantation Website: https://shazam.readthedocs.io/en/stable/vignettes/Baseline-Vignette/
- Immcantation GitHub: https://github.com/immcantation/shazam