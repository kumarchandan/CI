#

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.request import Request
from sqlite3 import dbapi2
from re import compile

# create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

# Crawl and Index
class crawler:
    
    #Initialize the crawler with the name of database
    def __init__(self, dbname):
        try:
            self.con = dbapi2.connect(dbname)
            print(self.con, 'Database connected successfully!')
        except Exception as e:
            print("error __init__: database connection error ", e)
        
    #
    def __del__(self):
        self.con.close()
    #
    def dbCommit(self):
        self.con.commit()
    #
    # Get an entry id and adding it if it's not present
    def getEntryId(self, table, field, value, createNew=True):
        try:
            cur = self.con.execute("select rowid from {} where {}=?".format(table, field), (value,))    # sql parameters can't be set using ?, use .format()
            res = cur.fetchone()
            if res == None:
                cur = self.con.execute("insert into {} ({}) values(?)".format(table, field), (value,))
                print(value, ' inserted')
                return cur.lastrowid
            else:
                return cur[0]

        except Exception as e:
            print('getEntryId: db error ', e)

    # Index an individual page
    def addToIndex(self, url, soup):

        if self.isIndexed(url):
            return
        print('Indexing', url)
        # Get the individual words
        text = self.getTextOnly(soup)
        words = self.separateWords(text)
        # Get the URL id
        urlid = self.getEntryId('urllist', 'url', url)
        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords:
                continue
            wordId = self.getEntryId('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) values(?, ?, ?)", (urlid, wordId, i))
    
    # Extract the text from an HTML page(no tags)
    def getTextOnly(self, soup):            # BeautifulSoup API
        data = soup.string
        if data == None:
            contents = soup.contents
            resultText = ''
            for text in contents:
                subtext = self.getTextOnly(text)
                resultText += subtext + '\n'
            return resultText
        else:
            return data.strip()

    # Separate the words by any non-whitespace character
    def separateWords(self, text):
        splitter = compile('\\W*')
        splittedText = splitter.split(text)
        sepWords = [s.lower() for s in splittedText if s != '']
        return sepWords

    # Return true if this url is already indexed
    def isIndexed(self, url):
        try:
            curUrl = self.con.execute("select rowid from urllist where url = ?", (url,)).fetchone()
            if curUrl != None:
                # Check if it has actually been crawled
                v = self.con.execute("select * from wordlocation where urlid=?", (curUrl[0],)).fetchone()
                if v != None:
                    return True
        except Exception as e:
            print('isIndexed: Accessing the table has some issue.', e)
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
        try:
            # Tables
            self.con.execute('create table if not exists urllist(url)')
            self.con.execute('create table if not exists wordlist(word)')
            self.con.execute('create table if not exists wordlocation(urlid, wordid, location)')
            self.con.execute('create table if not exists link(fromid integer, toid integer)')
            self.con.execute('create table if not exists linkwords(wordid, linkid)')
            # Indices
            self.con.execute('create index if not exists wordidx on wordlist(word)')
            self.con.execute('create index if not exists urlidx on urllist(url)')
            self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
            self.con.execute('create index if not exists urltoidx on link(toid)')
            self.con.execute('create index if not exists urlfromidx on link(fromid)')
            self.dbCommit()
        except:
            print('Table already exists')

    # Calculate pagerank for pages
    def calculatePageRank(self, iterations=20):
        # clearout the current pagerank tables
        self.con.execute("drop table if exists pagerank")
        self.con.execute("create table pagerank(urlid primary key, score)")

        # Initialize every url with pagerank 1
        self.con.execute("insert into pagerank select rowid, 1.0 from urllist")
        self.dbCommit()

        for i in range(iterations):
            print("iteration : ", i)
            for(urlid,) in self.con.execute("select rowid from urllist"):
                pr = 0.15

                # loop through all the pages that link to this one
                for (linker,) in self.con.execute("select distinct fromid from link where toid=?", (urlid,)):
                    # get the pagerank of the linker
                    linkerPR = self.con.execute("select score from pagerank where urlid=?", (linker,)).fetchone()[0]
                    # get the total number of links from the linker
                    linkerCount = self.con.execute("select count(*) from link where fromid=?", (linker,)).fetchone()[0]
                    pr += 0.85 * (linkerPR / linkerCount)
                    self.con.execute("update pagerank set score=? where urlid=?", (pr, urlid))
        self.dbCommit()


# Search
class searcher:
    def __init__(self, dbname):
        self.con = dbapi2.connect(dbname)

    def __del__(self):
        self.con.close()
    #
    def dbCommit(self):
        self.con.commit()
    
    def getMatchRows(self, queryString):
        # Strings to build the query
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # split the words by spaces
        words = queryString.split(' ')
        tablenumber = 0

        for word in words:
            try:
                # Get the wordid
                wordrow = self.con.execute("select rowid from wordlist where word=?", (word,)).fetchone()
            except Exception as e:
                print('Error: getMatchRows : selection from db failed: ', e)

            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w{}.urlid = w{}.urlid and '.format(tablenumber - 1, tablenumber)
                fieldlist += ',w{}.location'.format(tablenumber)
                tablelist += 'wordlocation w{}'.format(tablenumber)
                clauselist += 'w{}.wordid = {}'.format(tablenumber, wordid)
                tablenumber += 1

        # Create the query from the seperate parts
        fullquery = "select {} from {} where {}".format(fieldlist, tablelist, clauselist)
        try:
            cur = self.con.execute(fullquery)
        except Exception as e:
            print('Error: getMatchRows : full query failed: ', e)
        rows = [row for row in cur]
        return rows, wordids
    
    def getScoredList(self, rows, wordids):
        totalScores = dict([(row[0], 0) for row in rows])

        # Scoring function
        weights = [(1.0, self.locationScore(rows)), (1.0, self.frequencyScore(rows)), (1.0, self.pageRankScore(rows)), (1.0, self.linkTextScore(rows, wordids))]

        for(weight, scores) in weights:
            for url in totalScores:
                totalScores[url] += weight * scores[url]
        return totalScores

    def getURLName(self, id):
        try:
            cur = self.con.execute("select url from urllist where rowid = {}".format(id))
            return cur.fetchone()[0]
        except Exception as e:
            print('Error: getURLName : cannot get urllist data', e)
        return None

    def query(self, q):
        rows, wordids = self.getMatchRows(q)
        scores = self.getScoredList(rows, wordids)
        rankedScores = sorted([(score, url) for (url, score) in scores.items()], reverse=1)

        for(score, urlid) in rankedScores[0:10]:
            print('{}, {}'.format(score, self.getURLName(urlid)))

    def normalizeScores(self, scores, smallIsBetter=0):
        vSmall = 0.00001    # avoid division by zero error
        if smallIsBetter:
            minScore = min(scores.values())
            return dict([(u, float(minScore) / max(vSmall, l)) for (u, l) in scores.items()])
        else:
            maxScore = max(scores.values())
            if maxScore == 0:
                maxScore = vSmall
            return dict([(u, float(c) / maxScore) for (u, c) in scores.items()])
    
    # Word frequencey
    def frequencyScore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalizeScores(counts)

    # Word location on the page
    def locationScore(self, rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc
        return self.normalizeScores(locations, smallIsBetter=1)

    # Queried words' distance from each other
    # distance score
    def distanceScore(self, rows):
        # If there is only one word, everyone wins!
        if len(rows[0]) <= 2:
            return dict([(row[0], 1.0) for row in rows])
        
        # Initialize the dictionary with larger values
        minDistance = dict([(row[0], 1000000) for row in rows])

        for row in rows:
            dist = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])
            if dist < minDistance[row[0]]:
                minDistance[row[0]] = dist 
        return self.normalizeScores(minDistance, smallIsBetter=1)

    # inbound link score
    def inboundLinkScore(self, rows):
        uniqueURLs = set([row[0] for row in rows])
        inboundCount = dict([(url, self.con.execute("select count(*) from link where toid={}".format(url)).fetchone()[0]) for url in uniqueURLs])
        return self.normalizeScores(inboundCount)

    # pagerank score
    def pageRankScore(self, rows):
        pageranks = dict([(row[0], (self.con.execute("select score from pagerank where urlid = ?", (row[0],)).fetchone()[0])) for row in rows])
        
        maxRank = max(pageranks.values())
        normalizeScores = dict([(u, float(1) / maxRank) for (u, l) in pageranks.items()])
        return normalizeScores

    # link text score
    def linkTextScore(self, rows, wordids):
        linkScores = dict([row[0], 0] for row in rows)
        for wordid in wordids:
            cur = self.con.execute("select link.fromid, link.toid from linkwords, link where wordid=? and linkwords.linkid=link.rowid", (wordid,))
            for(fromid, toid) in cur:
                if toid in linkScores:
                    pr = self.con.execute("select score from pagerank where urlid=?", (fromid, )).fetchone()[0]
                    linkScores[toid] += pr
        maxScore = max(linkScores.values())
        normalizedScores = dict([(u, float(l) / maxScore) for (u, l) in linkScores.items()])
        return normalizedScores
