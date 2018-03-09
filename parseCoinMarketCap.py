import requests
from bs4 import BeautifulSoup
import os, urllib2, sys, re

# TODO : Scrapy - already installed. Seems more powerful than BeautifulSoup. Check how can this be used.
# TODO : how to change column's order (highest or lowest first) and read one specific table entry.


'''user-defined exception class to print mismatch in lengths of rows searched and coin attributes'''
class lengthMismatchError(Exception):
    def __init__(self,totalRows, names,symbols,prices,marketCaps,posAndNegChanges,urls):
        self.totalRows              = totalRows
        self.namesLength            = names
        self.symbolsLength          = symbols
        self.pricesLength           = prices
        self.marketCapsLength       = marketCaps
        self.posAndNegChangesLength = posAndNegChanges
        self.urlsLength             = urls

    def __str__(self):
        print "Lengths of one or more coin attributes DO NOT match total no. of rows"
        # TODO : change the print statements
        print "totalRows =", self.totalRows
        print "\tnamesLength = ", self.namesLength
        print "\tsymbolsLength = ", self.symbolsLength
        print "\tpricesLength = ", self.pricesLength
        print "\tmarketCapsLength = ", self.marketCapsLength
        print "\tposAndNegChangesLength = ", self.posAndNegChangesLength
        print "\turlsLength = ", self.urlsLength


class cryptoCoin(object):

    def __init__(self,searchRows='all'):
        self.searchRows             = searchRows
        self.coins                  = []
        self.coinSymbol             = []
        self.coinPrice              = []
        self.coinMarketCap          = []
        self.coinPosAndNegChng24h   = []
        self.coinChange24h          = []
        self.coinNegChange24h       = []
        self.coinURL                = []
        # TODO : do we really need both positive and negative change variables ? Not efficient ?

    # TODO: Still this is a very bad way. How can individual functions call this one to get how many rows to search ? Then call this one eleswhere
    def searchRowBoundaries(self):
        if self.searchRows == 'all':
            return 1

    '''Returns the title of the homepage'''
    def returnPageTitle(self, soupObj):
        title = soupObj.find('h1', attrs={'id': 'title'})
        '''
        title is a class of type <class 'bs4.element.Tag'>
            so convert it into text, and strip starting and trailing
        '''
        return title.text.strip()


    ''' Returns column headings : Name | Market Cap | Price | Volume (24h) | Circulating Suppy | Change (24h) | Price Graph (24h) '''
    def returnTableHeading(self, soupObj):
        firstTwoRows = soupObj.find_all('tr', limit=2)
        columnHeaders = [th.getText() for th in firstTwoRows[0].findAll('th')]
        return columnHeaders


    ''' Returns total number of crypto-coins listed on the homepage '''
    def findTotalCoins(self, soupObj):
        total_coins = 0
        coinList = soupObj.find_all(class_='no-wrap currency-name')
        return len(coinList)

    ''' Finds the name of each crypto-currency '''
    def findAllCoinNames(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]

        coin_data = [ coinRows[i].find_all('td', class_="no-wrap currency-name") for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                aaa = eachCoin.find_all('a', class_="currency-name-container")
                currencyNameContainerAll = [aaa[i].getText() for i in range(len(aaa))]
                for eachCoinName in currencyNameContainerAll:
                    self.coins.append(eachCoinName)
        return self.coins


    '''Finds the symbol for each crypto-currency'''
    def findAllCoinSymbols(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find('a') for i in range(len(coinRows))]
        for eachCoin_data in coin_data:
            self.coinSymbol.append(eachCoin_data.get_text().strip())
        return self.coinSymbol


    '''Finds current price of each crypto-currency'''
    def findAllCoinPrices(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find_all('a', class_="price") for i in range(len(coinRows))]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                self.coinPrice.append(eachCoin.get_text().strip())
        return self.coinPrice

    '''Finds market cap for each crypto-currency'''
    def findAllCoinMarketCaps(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find_all('td', class_="no-wrap market-cap text-right") for i in range(len(coinRows))]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                # strip() is added to remove '\n' from front and back of [u'\n$194,725,221,493\n']
                self.coinMarketCap.append(eachCoin.get_text().strip())
        return self.coinMarketCap

    '''Finds both positve and negative % change in last 24hours for each crypto-currency'''
    def findAllPosAndNegChange24h(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]

        # Good example of finding table data for multiple classes
        coin_data = [coinRows[i].find_all('td', {"class": ["no-wrap percent-change positive_change text-right", "no-wrap percent-change negative_change text-right"]}) for i in
                     range(len(coinRows))]
        for eachCoin_data in coin_data:
            # print "% change : " , eachCoin_data
            for eachCoin in eachCoin_data:
                self.coinPosAndNegChng24h.append(eachCoin.get_text().strip())
        return self.coinPosAndNegChng24h

    '''Finds positve % change in last 24hours for each crypto-currency'''
    def findAllPositiveChange24h(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find_all('td', class_="no-wrap percent-change positive_change text-right") for i in
                     range(len(coinRows))]
        for eachCoin_data in coin_data:
            # print "% change : " , eachCoin_data
            for eachCoin in eachCoin_data:
                self.coinChange24h.append(eachCoin.get_text().strip())
        return self.coinChange24h


    '''Finds negative % change in last 24hours for each crypto-currency'''
    def findAllNegativeChange24h(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find_all('td', class_="no-wrap percent-change negative_change text-right") for i in
                     range(len(coinRows))]
        for eachCoin_data in coin_data:
            # print "% change : " , eachCoin_data
            for eachCoin in eachCoin_data:
                self.coinNegChange24h.append(eachCoin.get_text().strip())
        return self.coinNegChange24h

    '''Finds URL for each crypto-currency's webpage'''
    def findAllCoinUrls(self, soupObj):
        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]
        coin_data = [coinRows[i].find('a') for i in range(len(coinRows))]
        for eachCoin_data in coin_data:
            # eachCoin_data.attrs['href'] returns subURL i.e. /currencies/bitcoin/
            # So adding baseUrl with it.
            self.coinURL.append(baseUrl + eachCoin_data.attrs['href'])

        # Another method :
        # coinFullUrl = []
        # urlRegex = r"<a href=\"([/a-z]+)"
        #
        # coinList = soupObj.find_all(class_='no-wrap currency-name')
        # for coin in coinList:
        #     coinUrl = coin.find_all('a')
        #     for line in coinUrl:
        #         if re.search(urlRegex, str(line)):
        #             match = re.search(urlRegex, str(line))
        #             coinFullUrl.append(baseUrl + match.group(1))
        # return coinFullUrl

        return self.coinURL

    ''' Finds a user requested crypto-currency name'''
    def findCoin(self, soupObj, coinName):
        print "Looking for " , coinName , " ... .. ."
        # TODO : handle how to search / print only the user requested coin. Currently it is only finding the first row.
        coin = soupObj.find(class_='no-wrap currency-name')
        coinUrl = coin.find_all('a')
        print coinUrl

    '''For each row i.e. each crypto-currency, finds data and stores it in respective lists'''
    def getCoinData(self, soupObj):

        # Get 2nd to last row. First row has table headers
        coinRows = soupObj.findAll('tr')[1:]

        # for eachRow in coinRows:
        #     # Prints each row's full data
        #     print(eachRow.prettify())

        ''' Finds the name of each crypto-currency '''
        allNames = self.findAllCoinNames(soupObj)

        '''Finds the symbol for each crypto-currency'''
        allSymbols = self.findAllCoinSymbols(soupObj)

        '''Finds current price of each crypto-currency'''
        allPrices = self.findAllCoinPrices(soupObj)

        '''Finds market cap for each crypto-currency'''
        allMarketCaps = self.findAllCoinMarketCaps(soupObj)

        '''Finds % change (both positive and negative) in last 24hours for each crypto-currency'''
        allPosAndNegChange24h = self.findAllPosAndNegChange24h(soupObj)
        # # Use following to test error/lengthMismatchError exception condition
        # allPosAndNegChange24h = self.findAllNegativeChange24h(soupObj)

        '''Finds URL for each crypto-currency's webpage'''
        allUrls = self.findAllCoinUrls(soupObj)

        try:
            if any([    len(allNames)               != len(coinRows), \
                        len(allSymbols)             != len(coinRows), \
                        len(allPrices)              != len(coinRows), \
                        len(allMarketCaps)          != len(coinRows), \
                        len(allPosAndNegChange24h)  != len(coinRows), \
                        len(allUrls)                != len(coinRows) ]) :
                raise lengthMismatchError(len(coinRows),len(allNames),len(allSymbols),len(allPrices),len(allMarketCaps),len(allPosAndNegChange24h),len(allUrls) )
        except lengthMismatchError as errorObj:
            errorObj.__str__()
            return ["ERROR","ERROR","ERROR","ERROR","ERROR","ERROR"]
        else :
            # TODO : Is there a better way of returning ? Handle it accordingly in the above error condition as well
            # Returning a nested list - much better way of returning multiple attributes.
            return [allNames, allSymbols, allPrices, allMarketCaps, allPosAndNegChange24h, allUrls]


    '''Returns top 5 performing coins in terms of positive % change in last 24h'''
    def findTopFiveBestCoins(self,soupObj):
        allCoinsData = self.getCoinData(soupObj)
        # tempAllPosAndNegChange24h = allCoinsData[-2]
        # allCoinsData[-2] = [x for x in tempAllPosAndNegChange24h if x >= 0] + [x for x in tempAllPosAndNegChange24h if x < 0]
        # OR
        # trying to get top 5 coins
        tempAllCoinsSortedAsPerTopPosChange24h = sorted(allCoinsData[-2],reverse=True)
        print "tempAllCoinsSortedAsPerTopPosChange24h - " , tempAllCoinsSortedAsPerTopPosChange24h
        topFiveCoinIndices = [ allCoinsData[-2].index(x) for x in tempAllCoinsSortedAsPerTopPosChange24h[0:5] ]
        print "topFiveCoinIndices : " , topFiveCoinIndices
        print "best coin - ", allCoinsData[0][topFiveCoinIndices[0]]
        print [x for x in topFiveCoinIndices]
        print " -----  -- - - - - -- - -- - -- - -- ------ - - -- - - -- -- - ----- - -"

        topFiveCoinsNames       = [ allCoinsData[0][x] for x in topFiveCoinIndices ]
        topFiveCoinsSymbols     = [ allCoinsData[1][x] for x in topFiveCoinIndices ]
        topFiveCoinsPrices      = [ allCoinsData[2][x] for x in topFiveCoinIndices ]
        topFiveCoinsMarketCaps  = [ allCoinsData[3][x] for x in topFiveCoinIndices ]
        topFiveCoinsChange24h   = [ allCoinsData[4][x] for x in topFiveCoinIndices ]
        topFiveCoinsUrls        = [ allCoinsData[5][x] for x in topFiveCoinIndices ]

        return [ topFiveCoinsNames, topFiveCoinsSymbols, topFiveCoinsPrices, topFiveCoinsMarketCaps, topFiveCoinsChange24h, topFiveCoinsUrls ]

baseUrl = "https://coinmarketcap.com"
page = requests.get(baseUrl)
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

myCoin = cryptoCoin()
# print(myCoin.returnPageTitle(soup))
# print(myCoin.returnTableHeading(soup))
# print "Total Coins on CoinMarketCap.com : ", myCoin.findTotalCoins(soup)
print "##############################"

# myCoin.findCoin(soup,"Bitcoin")

print "##############################"
# print(myCoin.findAllCoinNames(soup))
# print(myCoin.findAllCoinSymbols(soup))
# print(myCoin.findAllCoinPrices(soup))
# print(myCoin.findAllCoinMarketCaps(soup))
print(myCoin.findAllPositiveChange24h(soup))
# print(myCoin.findAllNegativeChange24h(soup))
# print(myCoin.findAllPosAndNegChange24h(soup))
# # print(len(myCoin.findAllPosAndNegChange24h(soup)))
# print(myCoin.findAllCoinUrls(soup))

print "##############################"
# # returns data of all 100 coins listed in the table on the homepage.
# myCoinData = myCoin.getCoinData(soup)
# print(myCoinData[0])
# print(myCoinData[1])
# print(myCoinData[2])
# print(myCoinData[3])
# print(myCoinData[4])
# print(myCoinData[5])

print "##############################"
topFiveCoinsData = myCoin.findTopFiveBestCoins(soup)
print(topFiveCoinsData[0])
print(topFiveCoinsData[1])
print(topFiveCoinsData[2])
print(topFiveCoinsData[3])
print(topFiveCoinsData[4])
print(topFiveCoinsData[5])

'''
NOTES :
    Good resources :
    https://beautiful-soup-4.readthedocs.io/en/latest/
    http://savvastjortjoglou.com/nba-draft-part01-scraping.html
'''