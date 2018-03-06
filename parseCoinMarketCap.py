import requests
from bs4 import BeautifulSoup
import os, urllib2, sys, re

# TODO : Scrapy - already installed. Seems more powerful than BeautifulSoup. Check how can this be used.
# TODO : how to change column's order (highest or lowest first) and read one specific table entry.

class cryptoCoin(object):
    def __init__(self):
        self.coins          = []
        self.coinSymbol     = []
        self.coinPrice      = []
        self.coinMarketCap  = []
        self.coinChange24h  = []
        self.coinURL        = []

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


    ''' Returns URLs for all the listed crypto-coins '''
    def findAllCoinUrl(self, soupObj):
        coinFullUrl = []
        urlRegex = r"<a href=\"([/a-z]+)"

        coinList = soupObj.find_all(class_='no-wrap currency-name')
        for coin in coinList:
            coinUrl = coin.find_all('a')
            for line in coinUrl:
                if re.search(urlRegex, str(line)):
                    match = re.search(urlRegex, str(line))
                    coinFullUrl.append(baseUrl + match.group(1))
        return coinFullUrl

    ''' Finds a user requested crypto-currency name'''
    def findCoin(self, soupObj, coinName):
        print "Looking for " , coinName , " ... .. ."
        # TODO : handle how to search / print only the user requested coin
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
        coin_data = [ coinRows[i].find_all('td', class_="no-wrap currency-name") for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                aaa = eachCoin.find_all('a', class_="currency-name-container")
                currencyNameContainerAll = [aaa[i].getText() for i in range(len(aaa))]
                for eachCoinName in currencyNameContainerAll:
                    self.coins.append(eachCoinName)

        '''Finds the symbol for each crypto-currency'''
        coin_data = [ coinRows[i].find('a') for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            self.coinSymbol.append(eachCoin_data.get_text().strip())

        '''Finds current price of each crypto-currency'''
        coin_data = [ coinRows[i].find_all('a', class_="price") for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                self.coinPrice.append(eachCoin.get_text().strip())

        '''Finds market cap for each crypto-currency'''
        coin_data = [ coinRows[i].find_all('td', class_="no-wrap market-cap text-right") for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            for eachCoin in eachCoin_data:
                # strip() is added to remove '\n' from front and back of [u'\n$194,725,221,493\n']
                self.coinMarketCap.append(eachCoin.get_text().strip())

        '''Finds % change in last 24hours for each crypto-currency'''
        # TODO This only works for +ve percentage change. Skips a -ve entry . this is not good. If this is the case, then will have to handle +ve and -ve % change currencies separately. i.e. 2 different data structures for each type. Bad design!
        coin_data = [ coinRows[i].find_all('td', class_="no-wrap percent-change positive_change text-right") for i in range(len(coinRows)) ]
        for eachCoin_data in coin_data:
            # print "% change : " , eachCoin_data
            for eachCoin in eachCoin_data:
                self.coinChange24h.append(eachCoin.get_text().strip())

        '''Finds URL for each crypto-currency's webpage'''
        coin_data = [coinRows[i].find('a') for i in range(len(coinRows))]
        for eachCoin_data in coin_data:
            # eachCoin_data.attrs['href'] returns subURL i.e. /currencies/bitcoin/
                # So adding baseUrl with it.
            self.coinURL.append(baseUrl + eachCoin_data.attrs['href'])

        print self.coins
        print self.coinSymbol
        print self.coinPrice
        print self.coinMarketCap
        print self.coinChange24h
        print self.coinURL
        # TODO : A better way of returning coin data. Think of some data structure.

        ''' End of getCoinData function'''

baseUrl = "https://coinmarketcap.com"
page = requests.get(baseUrl)
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

myCoin = cryptoCoin()
# print(myCoin.returnPageTitle(soup))
# print(myCoin.returnTableHeading(soup))
# print(myCoin.findAllCoinUrl(soup))
# print "Total Coins on CoinMarketCap.com : ", myCoin.findTotalCoins(soup)
# myCoin.findCoin(soup,"Bitcoin")
# myCoin.getCoinData(soup)

'''
NOTES :
    Good resources :
    https://beautiful-soup-4.readthedocs.io/en/latest/
    http://savvastjortjoglou.com/nba-draft-part01-scraping.html
'''