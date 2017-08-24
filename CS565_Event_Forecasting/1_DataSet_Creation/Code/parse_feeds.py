import os
import sys
import feedparser
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from nltk import clean_html
import urllib
import urllib2

save_path = '../Data/Parse_Feeds_Files'

   #Get the Handle to the feeds from the source
def get_feedparser_feed(FEED_URL):

    fp = feedparser.parse(FEED_URL)

    if fp and fp.entries and fp.entries[0]:
        print "Fetched %s entries from '%s'" % (len(fp.entries), fp.feed.title)
    else:
        print 'No entries parseed!'
        sys.exit()
    return fp
   #Store the file corrosponding to the handle passed
def get_blog_posts(fp):
    global feed_dict, blog_posts

    blog_posts = []
    for e in fp.entries:
        try:
            content = e.content[0]
        except AttributeError:
            content = e.summary_detail
   #Extracting all the reqired components of News Article
        url = e.links[0].href
        response = urllib2.urlopen(url)
        webContent = response.read()
        name=e.title+'.html'
	completeName = os.path.join(save_path,name)   
   #Writing those to file
        f = open(completeName, 'w')
        f.write(webContent)
        f.close
    return blog_posts
   #URL to the feeds of the source
FEED_URL = 'http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'
fp = get_feedparser_feed(FEED_URL)
blog_posts = get_blog_posts(fp)

