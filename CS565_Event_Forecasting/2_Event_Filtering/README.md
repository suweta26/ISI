############################# README FOR EVENT DETECTTION ##############################################


PART 1: KEY PHRASE FILTERING

	1. Description: Applying word2vec to learn words similar to 'protest', 'demonstration' and then finding only those articles which are protest relevant.

	2. This part has two scripts:
		a. 1_Find_Similar_Wrods_Word2Vec.py : to find words similar to 'protest;
		b. 2_Get_Relevant_Articles_From_DB : to retrieve all protest realted files.
		
		All the input files required for these two scripts to run are stored in '../../../1_DataSet_Creation/Data/All_Articles'.

	3. Follow below procedure to run the script 1_Find_Similar_Wrods_Word2Vec.py.
		Step 1: Store all collected articles in one folder and given the same path in script as:
			input_file_path = '../../../1_DataSet_Creation/Data/All_Articles'
		Step 2: Open the terminal and go to same path where code is saved in your system and run below command:
			python3 1_Find_Similar_Wrods_Word2Vec.py
	4. Output of script will be saved in output folder('../Data/Output_Files') where filename is 'all_word2vec.model'

	5. Follow below procedure to run the script '2_Get_Relevant_Articles_From_DB'.
		Step 1: Store all collected articles in one folder and given the same path in script as:
			input_file_path = '../../../1_DataSet_Creation/Data/All_Articles'
		Step 2: Open the terminal and go to same path where code is saved in your system and run below command:
			python3 2_Get_Relevant_Articles_From_DB
	

END OF PART 1

PART 2: LDA IMPLEMENTATION

	1. Description: Applying LDA to refine the data after key phrase learning. LDA will results in final set of relevant(protest related) 	         articles.

	2. This part has two scripts:
		a. LDA.py
		b. Cluster_Documents.py
		
		All the input files required for these two scripts to run are stored in '../Data folder'. 
	NOTE: To run these scripts install 'gensim' which is python3 library.

	3. Script LDA.py has implementation in below order;
		-> Process all articles returned by Key Phrasing.
		-> Remove stopwords and filter high frequency data
		-> Create term document matrix
		-> Create TF-IDF matrix
		-> Implement LDA functionality and find all topics
		-> Calculate probability of document for each topic and save as dictionary

	4. Follow below procedure to run the script.
		-> Step 1: Store all the articles filtered from Key Phrase Learning in folder names '../Data/Key_Pharse_Filtered_Articles'. 
		-> Step 2: Store the stop words file in input folder. (path- '../Data')
		-> Step 3: Open the terminal and go to same path where code is saved in your system and run below command:
				python3 LDA.py
		NOTE: We have used gensim which is standard library in python3, we have developed the code by following python3 standard.

	5. Output of script will be saved in output folder('../Data/Output_Files') where-
		-> Filename 'topic.txt' have all the topics retrued by LDA.
		-> Filename 'key_fiiles_as_dict.csv' stores the mapping of the input files.
		-> Filename 'key_doc_topic.dict' is a dictonary and have document and topic probability mapping.

	6. Script Cluster_Documents.py has implementation as below:
		-> Input to this script is: All Key Phrase Filtered Articles files and 'key_fiiles_as_dict.csv' file from above step.
		-> For given topic number (found in above step) and cutoff, this script will give all the relevant articles

	7. Run script Cluster_Documents.py with below command
		python3 Cluster_Documents.py
	
	8. All outpfiles for script 'Cluster_Documents.py' will be saved in '"../../Data/LDA_Filtered_Articles' folder.

 
END OF PART 2


ANALYSIS & EVLUATION

	1. Analyis folder contains all the artefacts of our analyis
		-> LDA_Log.txt: Contains trace of LDA training and test
		-> Topic_Cutoff.txt: Topics that we chose with their respective cutoff.
		-> Topic_Word_Mixture_TopicNumber.txt: Contains topic word mixture.

	2. We have created a test data set using random sampling of 200 documents and done manual tagging for relevance.
		-> Performace measures used were Precision, Recall and F-Measure
		-> Go to Evaluation folder.
		-> TestDataSet holds the files sampled from corpus
		-> Tagging.csv has entries <filename,Relevence_Flag>
		-> Retreived results are stored at 2_Event_Filtering/Data/LDA_Filtered_Articles
		-> Run scripts $python3 Evaluation.py
		
		Result:

		
			 
#############################END OF README FILE###############################################



