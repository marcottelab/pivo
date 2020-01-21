import csv
import argparse
import pandas as pd
from Bio import SeqIO

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Takes a FASTA file and get protein lengths")
    parser.add_argument("-f", "--input_fasta", action="store", required=True,
                                        help="Filename of .fasta input")
    parser.add_argument("-o", "--out", action="store", required=False, dest="out",
                                    help="Name for outfile (optional)")
    args = parser.parse_args()


if args.out == None:
	writefile = args.input_fasta.replace('.fasta','_lengths')
else:
	writefile = args.out

fasta = args.input_fasta

len_list = []
index = 0
total_len = 0
longest_len = 0

for record in SeqIO.parse(open(fasta,"r"), "fasta"):
	
	prot_id = record.id
	#prot_seq = str(record.seq.upper())
	prot_len = len(record.seq)
	len_list.append([prot_id, prot_len])
	
	index += 1
	total_len += prot_len

	if prot_len > longest_len:
		longest_len = prot_len
		longest_id = prot_id

avg_len = total_len/index
print("average protein length = {} aa".format(avg_len))
print("{} is the longest entry with {} aa".format(longest_id, longest_len))

len_df = pd.DataFrame(len_list)
len_df.columns=['ProteinID','ProteinLength']
sorted_df = len_df.sort_values('ProteinLength', ascending=False)
print(sorted_df)
sorted_df.to_csv(writefile+'.csv', index=False)


#########################################################
# without pandas
#########################################################

#with open("{}_lengths.txt".format(writefile),"w") as f:
#	f.write("{}\t{}\n".format("ProteinID","ProteinLength"))
#	
#	for record in SeqIO.parse(open(fasta,"r"), "fasta"):
#		
#		prot_id = record.id
#		#prot_seq = str(record.seq.upper())
#		prot_len = len(record.seq)
#		#len_list.append([prot_id, prot_len])
#		
#		index += 1
#		total_len += prot_len
#
#		if prot_len > longest_len:
#			longest_len = prot_len
#			longest_id = prot_id
#
#        # write the ID(s) and lengths to the open csv 
#		f.write("{}\t{}\n".format(prot_id,prot_len))