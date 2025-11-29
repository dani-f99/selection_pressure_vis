## Importing packages
library(alakazam)
library(shazam)
library(jsonlite)

# Reading the config file
config_info <- fromJSON("config.json", simplifyVector = FALSE)
input_folder <- config_info$input_folder
output_folder <- config_info$output_folder
metadata_list <- config_info$metadata_list

# Creating folders according the the congif.json
folders = c(input_folder, 
            output_folder, 
            paste0(output_folder,"/r_figures"), 
            paste0(output_folder,"/r_data"))

for (f in folders) {
                    if (!dir.exists(f)) {dir.create(f)}
                    print(paste0(f," folder was created."))
                    }

## Defining required custom S4 regions object

# 1. Define the length of each region in NUCLEOTIDES (based on IMGT standard)
# FWR1 (codon 1-26)   : 26 * 3 = 78 nt
# CDR1 (codon 27-38)  : 12 * 3 = 36 nt
# FWR2 (codon 39-55)  : 17 * 3 = 51 nt
# CDR2 (codon 56-65)  : 10 * 3 = 30 nt
# FWR3 (codon 66-104) : 39 * 3 = 117 nt
# Total Length        : 312 nt

# 2. Create the vector of region names repeated by their length
# Note: This creates a vector of length 312
region_labels <- c(
  rep("FWR1", 78),
  rep("CDR1", 36),
  rep("FWR2", 51),
  rep("CDR2", 30),
  rep("FWR3", 117)
                  )

# 3. Convert to factor (required by the S4 class)
boundary_factor <- factor(region_labels, levels = c("FWR1", 
                                                    "CDR1", 
                                                    "FWR2", 
                                                    "CDR2", 
                                                    "FWR3"
                                                    )
                          )

# 4. Create the S4 object
Custom_V_By_Regions <- createRegionDefinition(
                                              name = "Custom_V_Split",
                                              boundaries = boundary_factor,
                                              description = "IMGT V-segment split into constituent FWR and CDR regions",
                                              citation = "Custom definition based on IMGT numbering"
                                              )


# user input for dataset type
data_type_list <- list("motif", "all")
time_type_list <- list("tp", "tpall")
data_type <- "motif"
time_type <- "tp"

# Optional loop for user input if needed
while_loop = FALSE
if (while_loop == TRUE) {
while (!(data_type %in% data_type_list) | !(time_type %in% time_type_list)) 
        {
        if (!(data_type %in% data_type_list)) {
          data_type <- readline("What is the dataset, motif clones or all clones? (motif or all inputs only): ")
                                               }
        if (!(time_type %in% time_type_list)) {
          time_type <- readline("Calculate each time-point sepertly (tp) or all togahter (tpall?)? (motif or all inputs only): ")
                                               }
        }
}

current_time <- format(Sys.time(), "%Y-%m-%d_%H-%M-%S")     
run_name <-  paste0(data_type, "_", time_type, "_[",current_time,"]")
print(paste0(run_name, " Selected."))

# Defining import and output paths
input_path <- "datasets/"
output_path <- "output/"

## Importing our sequences
seqs <- read.csv(paste0(input_path, paste0("cl_seqs_",data_type,".csv")))
seqs_df <- data.frame(seqs)

# Modfing the naming scheme
colnames(seqs_df)[colnames(seqs_df) == 'sequence'] <- 'clonal_sequence'
colnames(seqs_df)[colnames(seqs_df) == 'germline'] <- 'clonal_germline'

# Custom function of the 
selection_analysis <- function(df_input) {
  
  # Creating baseline (expected and actual mutations)
  # Calculate selection scores from scratch
  baseline <- calcBaseline(df_input, 
                           testStatistic="focused", 
                           regionDefinition=Custom_V_By_Regions, 
                           nproc=1)
  
  # Grouping the data by subject id and ab_target
  grouped_2 <- groupBaseline(baseline, groupBy=c("subject_id","ab_target"))
  
  # Getting the statistical information about the baseline calculation
  #baseline_stats <- testBaseline(grouped_2, groupBy=c("subject_id","ab_target"))
  #write.csv(baseline_stats, paste0(output_path, run_name, "_baseline_stats.csv"))
  
  # Getting the mean and std.dev of the baseline calculation
  baseline_values <- summarizeBaseline(grouped_2, returnType="df")
  write.csv(baseline_values, paste0(output_path, run_name, "_baseline_values.csv"))
    
  # Plotting the baseline
  baseline_plot <- plotBaselineSummary(grouped_2, "subject_id", "ab_target")
  ggsave(paste0(output_path, run_name, "_baseline_plot.png"), plot = baseline_plot)
}

# CSV analysis by condition
if (time_type == "tpall") {
  selection_analysis(seqs_df)
  
} else if (time_type == "tp") {
  unique_time_points <- unique(seqs_df$time_point)
  
  for (tp in unique_time_points) {
    run_name <-  paste0(data_type, "_", time_type, tp, "_[",current_time,"]")
    temp_df <- seqs_df[seqs_df$time_point == tp,]
    selection_analysis(temp_df)
  }
}