from math import tanh
from sqlite3 import dbapi2

class searchnet:
    #
    def __init__(self, dbname):
        self.con = dbapi2.connect(dbname)

    def __del__(self):
        self.con.close()
    
    def makeTables(self):
        try:
            self.con.execute("create table hiddennode(create_key)")
            self.con.execute("create table hiddenword(fromid, toid, strength)")
            self.con.execute("create table hiddenurl(fromid, toid, strength)")
            self.con.commit()
        except Exception as e:
            print('error while creating tables or table already exists', e)
        
    # get strength
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
