# Test all SearchRank files

import searchengine

pagelist = ['http://en.wikipedia.org/wiki/Cognitive_science']
crawler = searchengine.crawler('searchindex.db')
crawler.createIndexTables()
# crawler.crawl(pagelist)
