--------------------------------------------------------------------------------
                              SYSTEM IMMUNOLOGY LAB
                                Haifa University
                                 Daniel Fridman
                                      2025
--------------------------------------------------------------------------------
[cite_start][cite: 1]

# PROJECT: Clonal Selection Pressure Analysis

## 1. OVERVIEW
This program's objective is to process sequencing data of clones in order to
[cite_start]analyze selection pressure metrics. [cite: 1]

## 2. PREREQUISITES
Please ensure the following modules are installed:

### Required R Modules:
- [cite_start]shazam [cite: 4]
- [cite_start]alakazam [cite: 4]
- [cite_start]jsonlite [cite: 4]

### Required Python Modules:
- [cite_start]Pandas [cite: 4]
- [cite_start]NumPy [cite: 4]
- [cite_start]Matplotlib [cite: 4]
- [cite_start]Seaborn [cite: 4]

## 3. CONFIGURATION (config.json)
[cite_start]Before running the analysis, configure the `config.json` file as follows: [cite: 5]

a. input_folder
   - [cite_start]Name of the input folder. [cite: 6]
   - [cite_start]Recommended to leave as default; the script will create this at first run. [cite: 6]

b. output_folder
   - [cite_start]Name of the output folder. [cite: 6]
   - [cite_start]Recommended to leave as default; the script will create this at first run. [cite: 7]

c. metadata_list
   - List of metadata that will group the sequences data before the selection
     [cite_start]pressure analysis. [cite: 7]

d. seq_dataset
   - [cite_start]Name of the dataset containing the sequences (example: "seqs.csv"). [cite: 8]

e. time_point
   - [cite_start]Options: "all" or "sep". [cite: 8]
   - [cite_start]"all": Analyze all timepoints at once. [cite: 9]
   - [cite_start]"sep": Split the data for each timepoint separately. [cite: 9]

## 4. USAGE GUIDE
1. [cite_start]Configure the `config.json` file as needed (see section above). [cite: 5]
2. [cite_start]Run the `selection_pressure.R` script, preferably on a server. [cite: 2, 5]
3. Run the `selection_visualization.ipynb` for better graphic visualization of
   [cite_start]the results. [cite: 3, 5]

## 5. DIRECTORY STRUCTURE
[cite_start]The program uses the following folder structure: [cite: 10]

- [cite_start]input/           : Input folder. [cite: 11]
- [cite_start]output/          : Result output, tables to be used in the LPA program. [cite: 10]
  - [cite_start]output/r_figures : Generated figures. [cite: 11]
  - [cite_start]output/r_data    : Generated data files. [cite: 11]