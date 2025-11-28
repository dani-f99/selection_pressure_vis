-----------------------------
------Daniel-Fridman---------
--- System-Immunology-Lab --- 
------Haifa-University ------
-----------2025--------------
-----------------------------
-----------------------------
--- General-Information -----
This program objective is to 
process sequencing data of clones in order to analyse selection pressure mterics.
1. in the first step, run the selection_pressure.R after filling the config.json file.
2. Run the sleection_visualization for better graphic visualization of the results.
-----------------------------
-----------------------------
-----------------------------
-----------------------------
--- Required-R-Modules -
1. shazam
2. alakazam
3. jsonlite
--- Required-Python-Modules -
1. Pandas
2. NumPy
3. Matplotlib
4. Seaborn
-----------------------------
-----------------------------
-----------------------------
-----------------------------
--- Guide ---
1. Configure the config.json as needed (see config.json section)
2. Run the selection_pressure.R script, preferebly on a server.
3. Run the selection_visualization.ipynb
-----------------------------
-----------------------------
-----------------------------
-----------------------------
--- config.json --------------
  a. input_folder -> Name of the input folder, recomended to leave as defualt. the script will create at first run.
  b. output_folder -> Name of the output folder, recomended to leave as defualt. the script will create at first run.
  c. metadata_list -> List of metadata that will group by the sequences data before the selection pressure analysis.
  d. seq_dataset -> name of the dataset containing the sequences (example: "seqs.csv").
  e. time_point -> "all" or "sep". "all" for all the timepoints at once and "sep" to split the data for each timepoint sepertly.
-----------------------------
-----------------------------
-----------------------------
-----------------------------
--- Subfolders --------------
1. output – result output, tables to be used in the LPA program.
2. output/r_figures -
3. output/r_data - 
4. input - 
-----------------------------
-----------------------------
-----------------------------
