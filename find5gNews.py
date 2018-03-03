class findNews(object):
    def __init__(self, newsType):
        self.newsType = newsType

    def printNewsType(self):
        print "News Type : ", self.newsType

myNews = findNews('5g')
myNews.printNewsType()