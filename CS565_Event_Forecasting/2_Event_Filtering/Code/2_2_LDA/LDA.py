import os
import nltk
import gensim
import re
import csv
import pickle
from os.path import isfile, join
from gensim import corpora, models, similarities
from gensim.models import  ldamodel
from nltk.stem import WordNetLemmatizer
from collections import Counter
import logging
import shutil
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
wordnet_lemmatizer = WordNetLemmatizer()
path=os.getcwd()
regex=(r'\([\w\.\s,]+\)')
regex2= (r'\((\d+),\s([\d\.]+)\)')

Output='../../Data/Output_Files'
if os.path.isdir(Output):
	shutil.rmtree(Output)
os.makedirs(Output)

#Function to read all input files, get path where files are kept, and parse stopwords file. Initailly all file name are stored in list
def read_all_files():
	stop_words_list=[]
	fileList=[]
	path_file = ("../../Data/Key_Phrase_Filtered_Articles")
	stop_file=open("../../Data/stopwords.txt",'r')
	stopwords=stop_file.read()
	stop_words_list=set(stopwords.split())
	for filename in os.listdir(path_file):
		fileList.append(filename)
	return path_file,stop_words_list,fileList
	
#Function to clear corpus by tokeniztion, removing stop words and lemmatization. Read whole corpus in a list and store each document data in a list as well, then read each document one by one. For each word of document first lemmatizing it and then checking for stop word. Store all data in list. There is one dictonary as well which is indexing documents. This dictonary is saved as files_as_dict.csv file. Also freq of each word is counted in this function only by using "Counter"

def filtered_corpus(path_file,stop_words_list,fileList):
	high_freq_data=[]
	doc_dict={}
	freq={}
	data_in_list=[]
	temp=[]
	alldata=[]
	i=0
	for filename in fileList:
		doc_dict[i]=filename
		i=i+1
		with open(os.path.join(path_file,filename), "r", encoding="ascii",errors="ignore") as f:
			filedata=f.read()
			compressed_data=[]
			for word in filedata.lower().split():
				if word not in stop_words_list:
					lemm_word=wordnet_lemmatizer.lemmatize(word)
					compressed_data.append(lemm_word)
					data_in_list.append(lemm_word)
			alldata.append(compressed_data)
	c = Counter(data_in_list)
	freq=dict(c)
	high_freq_data = [[data for data in docs if freq[data] > 1] for docs in alldata]
	write = csv.writer(open("../../Data/Output_Files/key_fiiles_as_dict.csv", "w",newline=''))
	for keys, values in doc_dict.items():
		write.writerow([keys, values])
	return  high_freq_data

#Function to first create term-document matrix and then TD-IDF matrix. Term-document matrix is created for high frequency data only. Words which appeared once have been removed. Using doc2bow to convert dictionary into bag of words. Each word is assigned with one id. So term document matrix will have only integer values where 1st tuple will indicate the word and 2nd tuple occurenc of word in a specific document.

def term_document_matrix():
	term_doc=[]
	word_id_mapping=corpora.Dictionary(high_freq_data)
	for words in high_freq_data:
		term_doc.append(word_id_mapping.doc2bow(words))
	return term_doc, word_id_mapping

def create_TFIDF_matrix(term_doc):
	tf_idf_model= models.TfidfModel(term_doc)
	tf_idf_matrix = tf_idf_model[term_doc]
	return tf_idf_matrix

#Function to implement LDA. Applying LDA in TF-IDF matrix and not on term-doc matrix. Each created topic will have most probable words in document. Storing data in form of string for future use. 

def find_topics(term_doc, word_id_mapping,tf_idf_matrix):
	t_num=150
	w_num=50
	ldamodel = gensim.models.ldamodel.LdaModel(tf_idf_matrix, num_topics=t_num, id2word = word_id_mapping, passes=20, iterations=50)
        #ldamodel.save('lda.model')
	topic=ldamodel.print_topics(num_topics=t_num, num_words=w_num)
	parse_doc=""
	lda_doc=ldamodel[tf_idf_matrix]
	for doc in lda_doc:
		data=str(doc)
		parse_doc=parse_doc+"\n"+data
	matrix_data=parse_doc.split('\n')
	write = csv.writer(open("../../Data/Output_Files/topics.txt", "w",newline=''))
	for keys in topic:
		write.writerow([keys])
	return topic,matrix_data

#Function to find probability of each word in document. Those document having high probability will be picked.

def doc_data_with_prob(matrix_data):
	dictionary={}
	dict_num=0
	for tuples in matrix_data:
	    tuples=re.findall(regex,tuples)
	    temp={}
	    for data in tuples:
	        data=re.search(regex2,data)
	        temp[data.group(1)]=data.group(2)
	    dictionary[dict_num]=temp
	    dict_num=dict_num+1
	write = csv.writer(open("../../Data/Output_Files/key_doc_topic.dict", "w",newline=''))
	pickle.dump(dictionary, open("../../Data/Output_Files/doc_topic.pickle", "wb"))
	for keys,values in dictionary.items():
		write.writerow([keys,values])

if __name__ == "__main__":
	print("Reading all the input files")
	path_file,stop_words_list,fileList=read_all_files()
	print("\n\t\t\tStep 1 Completed: Data processing Done\nFiltering corpus")
	high_freq_data=filtered_corpus(path_file,stop_words_list,fileList)
	print("\n\t\t\tStep 2 Completed: Corpus filtered i.e. Stored Data with high frequency\n Term Document matrix creation is in process")

	term_doc,word_id_mapping=term_document_matrix()

	print("\n\t\t\tStep 3 Completed: Created term document matrix Successfully\n Calcultaing TF-IDF matrix")

	tf_idf_matrix=create_TFIDF_matrix(term_doc)

	print("\n\t\t\tStep 4 Completed: TF-IDF matrix created successfully\nImplementing LDA functionality")

	final_topics,matrix_data=find_topics(term_doc,word_id_mapping,tf_idf_matrix)
	print("\n\t\t\tStep 5 Completed: LDA has been implemented successfully and all the tpocis are stored in file 'topics.txt'\nFinding probability of topic in documents")

	doc_data_with_prob(matrix_data)

	print("\n\t\t\tStep 6 Completed: Data is stored in file named 'key_doc_topic'")
	print("\n LDA Process finished")
















