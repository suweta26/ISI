# Program to get the articles from Key Phrase filetered articles based on LDA topic and cutoff

import pickle
import csv
import shutil
import os

# Read doc data with probability
docs = pickle.load( open( "../../Data/Output_Files/doc_topic.pickle", "rb" ) )

# Location of Key phrase filtered files
input_files = ("../../Data/Key_Phrase_Filtered_Articles")
output_files = ("../../Data/LDA_Filtered_Articles")

# Read the mapping of file id nad file name
with open('../../Data/Output_Files/key_fiiles_as_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    file_id_name_dict = {rows[0]:rows[1] for rows in reader}


# LDA topic id # One of the topic used. 
topicnumber='88'
higher_cutoff= .06
lower_cutoff = .01



# Create the output folder if not exists
if os.path.isdir(output_files):
   shutil.rmtree(output_files)
os.makedirs(output_files)


# Files list
fileList=[]

# Check all docs
for i in docs.keys():
    doc=docs[i]
   # Check cutoff for given topic number
    if topicnumber in doc.keys():
        if (float(doc[topicnumber])> lower_cutoff) and (float(doc[topicnumber])< higher_cutoff):
            filename = file_id_name_dict[str(i)]
            fileList.append(filename)
            shutil.copy(os.path.join(input_files,filename), os.path.join(output_files, filename))

