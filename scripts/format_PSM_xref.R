suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(janitor))
suppressPackageStartupMessages(library("argparse"))

# create parser object
parser <- ArgumentParser()
# specify our desired options
# by default ArgumentParser will add an help option

parser$add_argument("-p", "--peptides", dest="peptides",
                    help="Proteome discoverer file containing peptide spectral matches to database (file format = .txt)")
parser$add_argument("-o", "--outfile", action="store",
                    dest="outfile", help="Output filename for formatted .csv", 
                    default="outfile.csv")

args <- parser$parse_args()

peptides <- read_delim(args$peptides, 
                       delim = "\t", 
                       col_names = TRUE) %>%
  clean_names() %>%
  filter(contaminant == FALSE) %>%
  select(protein_accessions, annotated_sequence)

print("Input file...")
print(peptides)

peptides$annotated_sequence <- peptides$annotated_sequence %>%
  str_remove_all(., pattern = "\\[...\\]") %>% # remove ambiguous terminal amino acids
  str_remove_all(., pattern = "\\[..\\]") %>% # remove ambiguous terminal amino acids
  str_remove_all(., pattern = "\\[|\\.|\\]") %>% # remove extra characters
  toupper() # convert detected PTMs to uppercase

print("Output file...")
print(peptides)

outfile = args$outfile

if(str_sub(outfile, -3, -1) != "csv"){
  outfile = paste0(outfile, ".csv")
}

write_csv(peptides, outfile)

sprintf("Formatted outfile saved to: %s", outfile)




