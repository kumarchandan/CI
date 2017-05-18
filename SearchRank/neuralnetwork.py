from math import tanh
from sqlite3 import dbapi2

class searchnet:
    #
    def __init__(self, dbname):
        self.con = dbapi2.connect(dbname)

    def __del__(self):
        self.con.close()
    
    # db tables to support neural network model - 
    def makeTables(self):
        try:
            self.con.execute("create table hiddennode(create_key)")
            self.con.execute("create table hiddenword(fromid, toid, strength)")
            self.con.execute("create table hiddenurl(fromid, toid, strength)")
            self.con.commit()
        except Exception as e:
            print('error while creating tables or table already exists', e)
        
    # getStrength - determines the current strength of the connection. since new connection are only created
    # when necessary this method has to return default value if there are no connections
    # for links from words to hiddenlayer, the default value is -0.2, so that, by default, extra words will have a
    # slightly negative effect on the activation level of a hidden node.
    def getStrength(self, fromid, toid, layer):
        if layer == 0:
            table = 'hiddenword'
        else:
            table = 'hiddenurl'
        
        res = self.con.execute("select strength from {} where fromid={} and toid={}".format(table, fromid, toid)).fetchone()
        if res is None:
            if layer == 0:
                return -0.2
            if layer == 1:
                return 0
        return res[0]

    # if connection already exists, update or create connection with new strength
    def setStrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = 'hiddenword'
        else:
            table = 'hiddenurl'
        
        res = self.con.execute("select rowid from {} where fromid = {} and toid = {}".format(table, fromid, toid)).fetchone()
        # 
        if res is None:
            self.con.execute("insert into {} (fromid, toid, strength) values({}, {}, {})".format(table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute("update {} set strength={} where rowid={}".format(table, strength, rowid))
    
    # create a new node in the hidden layer every time it is passed a combination of words that it has never seen before
    def generateHiddenNode(self, wordids, urls):
        # 
        if len(wordids) > 3:
            return None
        # check if we already created a node for this set of words
        createkey = '_'.join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute("select rowid from hiddennode where create_key='{}'".format(createkey)).fetchone()

        # if not, create it
        if res is None:
            cur = self.con.execute("insert into hiddennode(create_key) values('{}')".format(createkey))
            hiddenid = cur.lastrowid
            # put in some default weights
            for wordid in wordids:
                self.setStrength(wordid, hiddenid, 0, 1.0/len(wordids))
                for urlid in urls:
                    self.setStrength(hiddenid, urlid, 1, 0.1)
            self.con.commit()

    def getAllHiddenIds(self, wordids, urlids):
        l1 = {}
        for wordid in wordids:
            cur = self.con.execute("select toid from hiddenword where fromid={}".format(wordid))
            for urlid in urlids:
                cur = self.con.execute("select fromid from hiddenurl where toid={}".format(urlid))
                for row in cur:
                    l1[row[0]] = 1
            return l1.keys()
    
    # setup network
    def setupNetwork(self, wordids, urlids):
        # value lists
        self.wordids = wordids
        self.urlids = urlids
        self.hiddenids = self.getAllHiddenIds(wordids, urlids)

        # node outputs
        self.ai = [1.0] * len(self.wordids)
        self.ao = [1.0]*len(self.urlids)
        self.ah = [1.0] * len(self.hiddenids)

        # create weights matrix
        self.wi = [[self.getStrength(wordid, hiddenid, 0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo = [[self.getStrength(hiddenid, urlid, 1) for urlid in self.urlids] for hiddenid in self.hiddenids]

    # feedforward
    def feedforward(self):
        # the only inputs are the query words
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # hidden activations
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # output activations
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)
        return self.ao[:]
    
    # get result
    def getresult(self, wordids, urlids):
        self.setupNetwork(wordids, urlids)
        return self.feedforward()
