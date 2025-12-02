## Importing packages
suppressPackageStartupMessages({
  library(alakazam)
  library(shazam)
  library(jsonlite)
})


# Reading the config file
config_info <- fromJSON("config.json", simplifyVector = FALSE)
input_folder <- config_info$input_folder
input_dataset <- config_info$dataset
output_folder <- config_info$output_folder
metadata_list <- unlist(strsplit(config_info$metadata_list, ","))
time_point <- config_info$time_point

if (length(metadata_list) == 1){
  meta_groupby <- metadata_list[1]
  meta_name <- meta_groupby

} else if (length(metadata_list) == 2) {
  meta_groupby <- metadata_list[1]
  meta_name <- paste(metadata_list, collapse = "-")
}


# Creating folders according the the congif.json
folders <- c(input_folder, 
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


# Defining output name
dataset_name <- strsplit(input_dataset, ".", fixed=TRUE)[[1]][1]
current_time <- format(Sys.time(), "%Y-%m-%d_%H-%M-%S")     
run_name <-  paste0(dataset_name,"-",meta_name , "-", time_point, "-[", current_time, "]")
print(paste0(run_name, " Selected."))

# Defining import and output paths
input_path <- paste0(input_folder,"/")
output_path <- paste0(output_folder,"/")

## Importing our sequences
seqs <- read.csv(paste0(input_path, input_dataset))
seqs_df <- data.frame(seqs)

# Modefing the naming scheme
colnames(seqs_df)[colnames(seqs_df) == 'sequence'] <- 'clonal_sequence'
colnames(seqs_df)[colnames(seqs_df) == 'germline'] <- 'clonal_germline'

# Custom function of the 
selection_analysis <- function(df_input) {
  
  # Creating baseline (expected and actual mutations)
  # Calculate selection scores from scratch
  print("Calculating Baseline")
  baseline <- calcBaseline(df_input, 
                           testStatistic="focused", 
                           regionDefinition=Custom_V_By_Regions, 
                           nproc=1)
  
  # Grouping the data by subject id and ab_target
  print("Grouping data")
  grouped_baseline <- groupBaseline(baseline, 
                                    groupBy=meta_groupby)
  
  # Getting the mean and std.dev of the baseline calculation
  print("Calculating baseline values for grouped data")
  baseline_values <- summarizeBaseline(grouped_baseline, 
                                       returnType="df")
  write.csv(baseline_values,
            paste0(output_folder, "/r_data/", run_name, "_baseline_values.csv"))
    
  # Plotting the baseline
  print("Ploting Figure")
  baseline_plot <- plotBaselineSummary(grouped_baseline, meta_groupby)
  ggsave(paste0(output_folder, "/r_figures/", run_name, "_baseline_plot.png"), 
         plot = baseline_plot)
}

# CSV analysis by condition
if (time_point == "all") {
  selection_analysis(seqs_df)
  
} else if (time_point == "sep") {
  unique_time_points <- unique(seqs_df$time_point)
  
  for (tp in unique_time_points) {
    run_name <- paste0(dataset_name,"-", meta_name , "-", time_point,"_", tp, "-[", current_time, "]")
    temp_df <- seqs_df[seqs_df$time_point == tp,]
    selection_analysis(temp_df)
  }
}