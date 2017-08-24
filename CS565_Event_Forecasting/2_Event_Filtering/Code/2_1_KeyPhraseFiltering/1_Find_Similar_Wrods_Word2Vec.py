# Program to file similar words to protest and demonstration in our corpus

import gensim, logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
input_file_path = '../../../1_DataSet_Creation/Data/All_Articles'

# Build Sentences from Corpus
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

				
sentences = MySentences(input_file_path) # a memory-friendly iterator

# Use word2Vec model
model = gensim.models.Word2Vec(sentences)

model.save('../../Data/Output_Files/all_word2vec.model')

#Get Most similar
print(model.most_similar('demonstration', topn=50))
