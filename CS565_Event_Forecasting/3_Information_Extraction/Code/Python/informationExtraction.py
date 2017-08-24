from itertools import islice
import os
from os import listdir
from os.path import isfile, join
import re
import shutil


#path = '/home/neha/Desktop/ISI_final/test'
relationPath = '../../Data/Relations'
article_path='../../../2_Event_Filtering/Data/LDA_Filtered_Articles'
taggedArticlePath='../../Data/Tagged_Protest_Articles'
extracted_info_path = '../../Data/Extracted_information'
fileList=[]
window_size=7







# Create the output folder if not exists
if os.path.isdir(extracted_info_path):
   shutil.rmtree(extracted_info_path)
os.makedirs(extracted_info_path)
########################################################################################################

#article_path='/home/neha/Desktop/info/article'

#get the published date of each article
articleList=[]
titleDict={}
published_date={}
for article in os.listdir(article_path):
  articleList.append(article)

for article in articleList:
  with open(os.path.join(article_path,article), 'rU') as fp:
    for i, line in enumerate(fp):
      if i == 2:
        published_date[article]=line[:len(line)-2]
      if i == 1:
        titleDict[article]=line




###################################################################################################
def get_count(word_count_tuple):
  """Returns the count from a dict word/count tuple  -- used for custom sort."""
  return word_count_tuple[1]



##########################################################################################################

def getRelID(relation):
  relID=relation.split('(')
  relID=int(relID[0])
  return relID
############################################################################################################
def window(seq, n):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

if __name__=="__main__":
  for filename in os.listdir(relationPath):
    fileList.append(filename)
  keywordList=['protest','protesting','protested','demonstartion','agitation','dharna','bandh','rally','rallies','gherao','activist','march towards','on strike']
  tagList=['/PERSON','/LOCATION','/DATE','/ORGANIZTION','/person','/location','/date','/organization']
##############################################################################
#iterate over all the files
  for filename in fileList:
    print(filename)
    print(titleDict[filename])

################################################################################################
#read file
    with open(os.path.join(relationPath,filename), 'rU') as f:
      dictPerson={}
      dictLocation={}
      dictOrganization={}
      dictDate={}
      relevanceDict={}
##################################################################################################
#parse the title
      with open(os.path.join(taggedArticlePath,filename), 'rU') as fp:
        i=0
        for i, line in enumerate(fp):
          if i==2:
            #print line+'\n'
            wordList=line.split(' ')
            k=-1
            for item in wordList:
              k=k+1
              if (k<len(wordList)) and ('/LOCATION' in wordList[k] or '/location' in wordList[k]):
                if (k+1<len(wordList)) and ('/LOCATION' in wordList[k+1] or '/location' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-9]
                  second=wordList[k+1]
                  second=second[:-9]
                  location=first+" "+second
                  k=k+1
                else:
                  location=wordList[k]
                  location=location[:-9]
                if location not in dictLocation:
                  dictLocation[location.lower()]=1

              if (k<len(wordList)) and ('/PERSON' in wordList[k] or '/person' in wordList[k]):
                if (k+1<len(wordList)) and ('/person' in wordList[k+1] or '/person' in wordList[k+1]):
                  if (k+2<len(wordList)) and ('/person' in wordList[k+2] or '/person' in wordList[k+2]):
                    first=wordList[k]
                    first=first[:-7]
                    second=wordList[k+1]
                    second=second[:-7]
                    third=wordList[k+2]
                    third=third[:-7]
                    person=first+" "+second+" "+third
                    k=k+2
                  else:
                    first=wordList[k]
                    first=first[:-7]
                    second=wordList[k+1]
                    second=second[:-7]
                    person=first+" "+second
                    k=k+1

                else:
                  person=wordList[k]
                  person=person[:-7]
                if person not in dictPerson:
                  dictPerson[person.lower()]=1


              if (k<len(wordList)) and ('/DATE' in wordList[k] or '/date' in wordList[k]):
                if (k+1<len(wordList)) and ('/DATE' in wordList[k+1] or '/date' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-5]
                  second=wordList[k+1]
                  second=second[:-5]
                  date=first+" "+second
                  k=k+1
                else:
                  date=wordList[k]
                  date=date[:-5]
                if date not in dictDate:
                  dictDate[date.lower()]=1

              if (k<len(wordList)) and ('/ORGANIZATION' in wordList[k] or '/oraganization' in wordList[k]):
                if (k+1<len(wordList)) and ('/ORGANIZATION' in wordList[k+1] or '/organization' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-13]
                  second=wordList[k+1]
                  second=second[:-13]
                  organization=first+" "+second
                  k=k+1
                else:
                  organization=wordList[k]
                  organization=organization[:-13]
                if organization not in dictOrganization:
                  dictOrganization[organization.lower()]=1


##################################################################################################
      content = f.readlines()
      # you may also want to remove whitespace characters like `\n` at the end of each line
      content = [x.strip() for x in content] 
    #prevWindowProcessedFlag=[0,0,0,0,0]



##################################################################################################
#iterarte over window
    for w in window(content,window_size):
      #check for key phrase in each window  and then check for the tags in each realtion extract info and mark relevant and processed
     # currWindowProcessedFlag=[0,0,0,0,0]
      stringWindow=str(w)
      if any(keyword in stringWindow for keyword in keywordList):




####################################################################################################
#iterate over all the relation of the window
        i=-1
        relevanceFlag=0
        for relation in w:
          person=""
          location=""
          date=""
          purpose=""
          organization=""
          flag=-1
          relevanceFlag=0
          i=i+1
          stringRel=str(relation)
          #relID=getRelID(stringRel)
          stringRel=stringRel[:-1]
          stringRel=re.sub(r'.*\(', '', stringRel)
          #print stringRel
         #set the flags and write relevence info into corresponding file
          if any(tag in stringRel for tag in tagList):
            #set relevance flag of this relation
            if any(keyword in stringRel for keyword in keywordList):
              relevanceFlag=1
              #print 'found relevant'
            #if not processed already process this time
            #if prevWindowProcessedFlag[i] == 0:
               #extract info
               #extractInfo(stringRel)
###########################################################################################################

            words=stringRel.split('#')
            string=words[0]+" "+words[1]+" "+words[2]
            wordList=string.split(' ')
            
            k=-1
            for item in wordList:
              k=k+1
              if (k<len(wordList)) and ('/LOCATION' in wordList[k] or '/location' in wordList[k]):
                if (k+1<len(wordList)) and ('/LOCATION' in wordList[k+1] or '/location' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-9]
                  second=wordList[k+1]
                  second=second[:-9]
                  location=first+" "+second
                  k=k+1
                else:
                  location=wordList[k]
                  location=location[:-9]
                if location not in dictLocation:
                  dictLocation[location.lower()]=1

              if (k<len(wordList)) and ('/PERSON' in wordList[k] or '/person' in wordList[k]):
                if (k+1<len(wordList)) and ('/person' in wordList[k+1] or '/person' in wordList[k+1]):
                  if (k+2<len(wordList)) and ('/person' in wordList[k+2] or '/person' in wordList[k+2]):
                    first=wordList[k]
                    first=first[:-7]
                    second=wordList[k+1]
                    second=second[:-7]
                    third=wordList[k+2]
                    third=third[:-7]
                    person=first+" "+second+" "+third
                    k=k+2
                  else:
                    first=wordList[k]
                    first=first[:-7]
                    second=wordList[k+1]
                    second=second[:-7]
                    person=first+" "+second
                    k=k+1

                else:
                  person=wordList[k]
                  person=person[:-7]
                if person not in dictPerson:
                  dictPerson[person.lower()]=1


              if (k<len(wordList)) and ('/DATE' in wordList[k] or '/date' in wordList[k]):
                if (k+1<len(wordList)) and ('/DATE' in wordList[k+1] or '/date' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-5]
                  second=wordList[k+1]
                  second=second[:-5]
                  date=first+" "+second
                  k=k+1
                else:
                  date=wordList[k]
                  date=date[:-5]
                if date not in dictDate:
                  dictDate[date.lower()]=1

              if (k<len(wordList)) and ('/ORGANIZATION' in wordList[k] or '/oraganization' in wordList[k]):
                if (k+1<len(wordList)) and ('/ORGANIZATION' in wordList[k+1] or '/organization' in wordList[k+1]):
                  first=wordList[k]
                  first=first[:-13]
                  second=wordList[k+1]
                  second=second[:-13]
                  organization=first+" "+second
                  k=k+1
                else:
                  organization=wordList[k]
                  organization=organization[:-13]
                if organization not in dictOrganization:
                  dictOrganization[organization.lower()]=1


###########################################################################################################
               #mark process flag in currWindowProcessedFlag
          #currWindowProcessedFlag[i]=1
          #write into file relevance info
        
        #relevanceDict[relID]=relevanceFlag
      #prevWindowProcessedFlag=currWindowProcessedFlag[:]
    #print dictPerson
    #print dictLocation
    #print dictOrganization
    #print dictDate

    completeName = os.path.join(extracted_info_path, filename)
    file1 = open(completeName, "w")
#write published date and title
    file1.write(published_date[filename])
    file1.write('\n'+titleDict[filename])
#write person
    if any(dictPerson):
      items = sorted(dictPerson.items(), key=get_count, reverse=True)
      firstWordFlag=1
      for item in items[:5]:
        if firstWordFlag == 1:
          file1.write(item[0])
          firstWordFlag=0
        else:
          file1.write(', '+item[0])
    else:
      file1.write('None')                     # '\n' not required as title string end with \n
#write date
    if any(dictDate):
      file1.write('\n')
      firstWordFlag=1
      for word,freq in dictDate.items():
        if firstWordFlag == 1:
          file1.write(word)
          firstWordFlag=0
        else:
          file1.write(', '+word)
    else:
      file1.write('\n'+published_date[filename])

#write organization
    if any(dictOrganization):
      file1.write('\n')
      items=[]
      items = sorted(dictOrganization.items(), key=get_count, reverse=True)
      firstWordFlag=1
      for item in items[:5]:
        if firstWordFlag == 1:
          file1.write(item[0])
          firstWordFlag=0
        else:
          file1.write(', '+item[0])
    else:
      file1.write('\nNone')
#write location
    if any(dictLocation):
      file1.write('\n')
      firstWordFlag=1
      for word,freq in dictLocation.items():
        if firstWordFlag == 1:
          file1.write(word)
          firstWordFlag=0
        else:
          file1.write(', '+word)
    else:
      file1.write('\nNone')
  file1.close()
