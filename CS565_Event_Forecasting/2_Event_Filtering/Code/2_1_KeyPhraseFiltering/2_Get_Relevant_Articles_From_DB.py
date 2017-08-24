# Get the relevant articles

import MySQLdb
import urllib2
import os
import shutil

save_path = '../../Data/Key_Phrase_Filtered_Articles'

if os.path.isdir(save_path):
   shutil.rmtree(save_path)
os.makedirs(save_path)


# Open database connection
db = MySQLdb.connect("127.0.0.1","root","admin","TESTDB")
# prepare a cursor object using cursor() method
cursor = db.cursor()
published_on=0
count=0
# Prepare SQL query to INSERT a record into the database.
sql = """SELECT * FROM News where (Source = 'hindustantimes' OR Source = 'indianexpress' OR Source = 'toi') AND (Title LIKE '%Protest%' OR Title LIKE '%Demons%' OR Title LIKE '%Rally%' OR Title LIKE '%Strike%' OR Title LIKE '%Dharna%' OR Title LIKE '%Bandh%'OR Title LIKE '%AANDOLAN%' OR Title LIKE '%Strike%' OR Title LIKE '%agitation%') """
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      idn = row[0]
      #link = row[1]
      published_on=row[2]
      title=row[3]
      #news_paper=row[4]
      article_text=row[5]
      taarikh = published_on%100
      mahina = (published_on%10000-taarikh)/100
      saal = (published_on-mahina-taarikh)/10000
      date = str(taarikh)+'-'+str(mahina)+'-'+str(saal)
      completeName = os.path.join(save_path,str(idn))   
      fo =open(completeName, 'w')
      fo.write(str(published_on)+ ' \n');
      fo.write(title+ ' \n');
      fo.write(str(date)+ ' \n');
      fo.write(article_text+' \n');
      fo.close()
      count=count+1
      print(" count = "+str(count))

except:
   print("Error: unable to fecth data")

# disconnect from server
db.close()
