import MySQLdb


#######################################################################
#                         Parameters and connectors
#######################################################################

count=0
#Create Connection to the server Database
db = MySQLdb.connect(host="172.16.117.24",    user="user_select_arti", passwd="user_select_arti",  db="News_articles_v1.2")
cur = db.cursor()
#Connection to Local Database
db_local = MySQLdb.connect("127.0.0.1","root","password","TESTDB")
cursor_local = db_local.cursor()
#Query to create table
sql_create_table = "CREATE TABLE News (id int NOT NULL,Link CHAR(200),published_on int,Title  BLOB,news_paper char(200),article_text BLOB )"	
cursor_local.execute(sql_create_table)
# get data from database where date > start_date (16 jan 2017 here)
start_date=20170116  # YYYYMMDD											
print "Getting data from SQL server...."
cur.execute("""SELECT *  from downloaded_1 WHERE `date`> %s  """,(start_date,))
coun = cur.fetchall()
db.commit()
print "Data Stats: \n Count of Articles after " + str(start_date)  + " = " + str(len(coun))
#Iterating Over the Fetched Data
for row in coun:
    id=row[0]
    link=row[2]
    published_on=row[3]
    date_in_integer=row[4]
    title=row[6]
    news_paper=row[7]
    article_text=row[8]
   #storing data to our local database
    sql_insert = "INSERT INTO News (id,Link,published_on,Title,news_paper,article_text)VALUES ('%d', '%s', '%d','%s','%s','%s' )" % (id,link,date_in_integer,title,news_paper,article_text)
    try:
   # Execute the SQL command
        cursor_local.execute(sql_insert)
   # Commit your changes in the database
        db_local.commit()
    except:
   # Rollback in case there is any error
        print 'Error Occured'
        db_local.rollback()
    count=count+1
    print "line no. %d copying", count;


print "Finished"
db.close()
db_local.close()


