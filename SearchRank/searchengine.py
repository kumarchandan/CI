#

class crawler:
    #Initialize the crawler with the name of database
    def __init__(self, dbname):
        #pass
    #
    def __del__(self):
        #pass
    #
    def dbCommit(self):
        #pass
    #
    #Auxiliary function for getting an entry id and adding
    # it if it's not present
    def getEntryId(self, table, field, value, createNew = True):
        return None
    
    # Index an individual page
    def addToIndex(self, url, soap):
        print 'Indexing %s' % url
    
    # Extract the text from an HTML page(no tags)
    def getTextOnly(self, soup):
        return None

    # Separate the words by any non-whitespace character
    def separate