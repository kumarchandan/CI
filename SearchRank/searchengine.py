#

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.request import Request
from sqlite3 import dbapi2 as sqlite

# create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:
    #Initialize the crawler with the name of database
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
    #
    def __del__(self):
        self.con.close()
    #
    def dbCommit(self):
        self.con.commit()
    #
    #Auxiliary function for getting an entry id and adding it if it's not present
    def getEntryId(self, table, field, value, createNew=True):
        return None
    
    # Index an individual page
    def addToIndex(self, url, soap):
        print('Indexing', url)
    
    # Extract the text from an HTML page(no tags)
    def getTextOnly(self, soup):
        return None

    # Separate the words by any non-whitespace character
    def separateWords(self, text):
        return None

    # REturn true if this url is already indexed
    def isIndexed(self, url):
        return False
    
    # Add a link between two pages
    def addLinkRef(self, urlFrom, urlTo, linkText):
        pass
    
    # Starting with a list of pages, do a breadth first search to the given depth, indexing pages as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    req = Request(page)
                    response = urlopen(req)
                except:
                    print('Could not open', page)
                    continue
                the_page = response.read()
                soup = BeautifulSoup(the_page, 'html.parser')
                self.addToIndex(page, soup)

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]         # remove # location portion
                        if url[0:4] == 'http' and not self.isIndexed(url):
                            newpages.add(url)
                        linkText = self.getTextOnly(link)
                        self.addLinkRef(page, url, linkText)
                    
                self.dbCommit()
            pages = newpages

    # Create index tables
    def createIndexTables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbCommit()
