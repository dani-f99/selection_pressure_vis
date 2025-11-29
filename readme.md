--------------------------------------------------------------------------------
                              SYSTEM IMMUNOLOGY LAB
                                Haifa University
                                 Daniel Fridman
                                      2025
[cite_start]-------------------------------------------------------------------------------- [cite: 1]

# PROJECT: Clonal Selection Pressure Analysis

## 1. OVERVIEW
This program processes sequencing data of clones in order to analyze selection
[cite_start]pressure metrics[cite: 1].

## 2. PREREQUISITES
[cite_start]Please ensure the following modules are installed before running the pipeline[cite: 4]:

### Required R Modules:
- shazam
- alakazam
- [cite_start]jsonlite [cite: 4]

### Required Python Modules:
- Pandas
- NumPy
- Matplotlib
- [cite_start]Seaborn [cite: 4]

## 3. CONFIGURATION (config.json)
[cite_start]Before running the analysis, configure the `config.json` file as follows[cite: 4, 5]:

a. input_folder
   - Name of the input folder.
   - [cite_start]Recommended to leave as default; the script will create this at first run[cite: 5, 6].

b. output_folder
   - Name of the output folder.
   - [cite_start]Recommended to leave as default; the script will create this at first run[cite: 6, 7].

c. metadata_list
   - List of metadata used to group the sequence data before the selection
     [cite_start]pressure analysis[cite: 7].

d. seq_dataset
   - [cite_start]Name of the dataset containing the sequences (example: "seqs.csv")[cite: 8].

e. time_point
   - [cite_start]Options: "all" or "sep"[cite: 8].
   - Use "all" for all timepoints at once.
   - [cite_start]Use "sep" to split the data for each timepoint separately[cite: 9].

## 4. USAGE GUIDE
1. [cite_start]Configure the `config.json` file as needed (see section above)[cite: 4].
2. [cite_start]Run the `selection_pressure.R` script (preferably on a server)[cite: 2, 4].
3. [cite_start]Run the `selection_visualization.ipynb` for graphic visualization of the results[cite: 3, 5].

## 5. DIRECTORY STRUCTURE
The program uses the following folder structure:

- [cite_start]input/           : Input files[cite: 11].
- [cite_start]output/          : Result output and tables to be used in the LPA program[cite: 10, 11].
  - [cite_start]output/r_figures : Generated figures[cite: 11].
  - [cite_start]output/r_data    : Generated data files[cite: 11].