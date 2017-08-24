import csv
import os

# Code to evaluate Event Filtering Model

LDA_ARTICLE_PATH = '../Data/LDA_Filtered_Articles'

# Read the meta data - Tagging information
with open('Tagging.csv', mode='r') as infile:
    reader = csv.reader(infile)
    tag_info_dict = {rows[0]:rows[1] for rows in reader}
	
file_list = []
# Build a list of files of test data set
with open('Tagging.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        file_list.append(rows[0])
		

# Build a dictionary for all the files
lda_file_dict ={}
for filename in os.listdir(LDA_ARTICLE_PATH):
    lda_file_dict[filename]='1'


TP = 0
FP = 0
TN = 0
FN = 0


for file in file_list:
    if ((tag_info_dict[file]=='1') and (file in lda_file_dict.keys())):
	    TP = TP + 1
	
    if ((tag_info_dict[file]=='1') and (file not in lda_file_dict.keys())):
	    FN = FN + 1
	
    if ((tag_info_dict[file]=='0') and (file in lda_file_dict.keys())):
	    FP = FP + 1
	
    if ((tag_info_dict[file]=='0') and (file not in lda_file_dict.keys())):
	    TN = TN + 1

precision = float(TP)/ (TP+FP)
recall = float(TP)/ (TP + FN)
fmeasure = (2*precision*recall)/(precision+recall)

print('TP is '+str(TP)+'\n')
print('FN is '+str(FN)+'\n')
print('FP is '+str(FP)+'\n')
print('TN is '+str(TN)+'\n')

print('Precision is '+str(precision)+'\n')
print('Recall is '+str(recall)+'\n')
print('F-Measure is '+str(fmeasure)+'\n')
