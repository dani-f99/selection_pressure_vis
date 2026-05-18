#####################
## Importing packages
suppressPackageStartupMessages({
  library(alakazam)
  library(shazam)
  library(jsonlite)
})


###########################
# Setting working directory
setwd("C:/github/selection_pressure_vis")


#############################################
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

##############################
# Loading dataset of sequences
seqs <- read.csv("input/cleaned_seqs_all_seq.csv")
dataset_seqs <- data.frame(seqs)
dataset_seqs$sequence <- trimws(dataset_seqs$sequence)
dataset_seqs$germline <- trimws(dataset_seqs$germline)


##############################################
# Collapse clonal groups into single sequences
clones <- collapseClones(dataset_seqs, 
                         cloneColumn="clone_id", 
                         sequenceColumn="sequence", 
                         germlineColumn="germline", 
                         regionDefinition=Custom_V_By_Regions, 
                         method="thresholdedFreq", 
                         minimumFrequency=0.6,
                         includeAmbiguous=FALSE, 
                         breakTiesStochastic=FALSE, 
                         nproc=1)

# Replace 'N' and '-' with '.' in the germline and sequence column
clones$clonal_sequence <- gsub("N|-", ".", clones$clonal_sequence, ignore.case = TRUE)
clones$clonal_germline <- gsub("N|-", ".", clones$clonal_germline, ignore.case = TRUE)


# Calculate selection scores from scratch
baseline <- calcBaseline(clones, 
                         testStatistic="focused", 
                         regionDefinition=Custom_V_By_Regions, 
                         nproc=1)

