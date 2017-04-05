# Test all SearchRank files

# import searchengine

# Crawling
# pagelist = ['https://en.wikipedia.org/wiki/Deep_learning','http://en.wikipedia.org/wiki/Cognitive_science', 'https://en.wikipedia.org/wiki/Artificial_intelligence']
# crawler = searchengine.crawler('wikipedia.db')
# crawler.calculatePageRank()
# # crawler = searchengine.crawler('')
# crawler.createIndexTables()
# crawler.crawl(pagelist)

# Searching
# e = searchengine.searcher('wikipedia.db')
# e.query('functional programming')



# neural network test
import neuralnetwork as nn
mynet = nn.searchnet('nn.db')
# mynet.makeTables()

wWorld, wRiver, wBank = 101, 102, 103           # words
uWorldBank, uRiver, uEarth = 201, 202, 203      # urls

# mynet.generateHiddenNode([wWorld, wBank], [uWorldBank, uRiver, uEarth])
print('hidden word')
for c in mynet.con.execute('select * from hiddenword'):
    print(c)

print('hidden url')
for c in mynet.con.execute('select * from hiddenurl'):
    print(c)

print('hidden node')
for c in mynet.con.execute('select * from hiddennode'):
    print(c)
