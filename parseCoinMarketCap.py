import requests
from bs4 import BeautifulSoup
import os, urllib2, sys, re

# TODO : Scrapy - already installed. Seems more powerful than BeautifulSoup. Check how can this be used.
# TODO : how to change column's order (highest or lowest first) and read one specific table entry.
#   good resource : http://savvastjortjoglou.com/nba-draft-part01-scraping.html

def returnPageTitle(soupObj):
    title = soupObj.find('h1', attrs={'id': 'title'})
    '''
    title is a class of type <class 'bs4.element.Tag'>
        so convert it into text, and strip starting and trailing
    '''
    return title.text.strip()


''' Returns column headings : Name | Market Cap | Price | Volume (24h) | Circulating Suppy | Change (24h) | Price Graph (24h) '''
def returnTableHeading(soupObj):
    firstTwoRows = soupObj.find_all('tr', limit=2)
    columnHeaders = [th.getText() for th in firstTwoRows[0].findAll('th')]
    return columnHeaders


def findTotalCoins(soupObj):
    total_coins = 0
    coinList = soupObj.find_all(class_='no-wrap currency-name')
    return len(coinList)


def findAllCoinUrl(soupObj):
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


def findCoin(soupObj):
    coin = soupObj.find(class_='no-wrap currency-name')
    coinUrl = coin.find_all('a')
    print coinUrl

def getCoinData(soupObj):
    coins           = []
    coinSymbol      = []
    coinPrice       = []
    coinMarketCap   = []
    coinChange24h   = []
    coinURL         = []

    # Get 2nd to last row. First row has table headers
    coinRows = soupObj.findAll('tr')[1:]

    for eachRow in coinRows:
        # Prints each row's full data
        print(eachRow.prettify())

    ''' Works fine '''
    ''' Finds the name of each crypto-currency '''
    coin_data = [ coinRows[i].find_all('td', class_="no-wrap currency-name") for i in range(len(coinRows)) ]
    for eachCoin_data in coin_data:
        for eachCoin in eachCoin_data:
            aaa = eachCoin.find_all('a', class_="currency-name-container")
            currencyNameContainerAll = [aaa[i].getText() for i in range(len(aaa))]
            for eachCoinName in currencyNameContainerAll:
                coins.append(eachCoinName)

    ''' Works fine '''
    '''Finds the symbol for each crypto-currency'''
    coin_data = [ coinRows[i].find('a') for i in range(len(coinRows)) ]
    for eachCoin_data in coin_data:
        coinSymbol.append(eachCoin_data.get_text().strip())

    ''' Works fine '''
    '''Find current price of each crypto-currency'''
    coin_data = [ coinRows[i].find_all('a', class_="price") for i in range(len(coinRows)) ]
    for eachCoin_data in coin_data:
        for eachCoin in eachCoin_data:
            coinPrice.append(eachCoin.get_text().strip())

    ''' Works fine '''
    '''Finds market cap for each crypto-currency'''
    coin_data = [ coinRows[i].find_all('td', class_="no-wrap market-cap text-right") for i in range(len(coinRows)) ]
    for eachCoin_data in coin_data:
        for eachCoin in eachCoin_data:
            # strip() is added to remove '\n' from front and back of [u'\n$194,725,221,493\n']
            coinMarketCap.append(eachCoin.get_text().strip())

    ''' Works fine '''
    '''Find % change in last 24hours for each crypto-currency'''
    # TODO This only works for +ve percentage change. Skips a -ve entry . this is not good. If this is the case, then will have to handle +ve and -ve % change currencies separately. i.e. 2 different data structures for each type. Bad design!
    coin_data = [ coinRows[i].find_all('td', class_="no-wrap percent-change positive_change text-right") for i in range(len(coinRows)) ]
    for eachCoin_data in coin_data:
        print "% change : " , eachCoin_data
        for eachCoin in eachCoin_data:
            coinChange24h.append(eachCoin.get_text().strip())

    ''' Works fine '''
    '''Find URL for each crypto-currency's webpage'''
    coin_data = [coinRows[i].find('a') for i in range(len(coinRows))]
    for eachCoin_data in coin_data:
        # eachCoin_data.attrs['href'] returns subURL i.e. /currencies/bitcoin/
            # So adding baseUrl with it.
        coinURL.append(baseUrl + eachCoin_data.attrs['href'])

    print coins
    print coinSymbol
    print coinPrice
    print coinMarketCap
    print coinChange24h
    print coinURL
    # TODO : A better way of returning coin data. Think of some data structure.
    ''' End of getCoinData function'''

baseUrl = "https://coinmarketcap.com"
page = requests.get(baseUrl)
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

# print returnPageTitle(soup)
# print returnTableHeading(soup)
# print findAllCoinUrl(soup)
# print "Total Coins on CoinMarketCap.com : ", findTotalCoins(soup)
# findCoin(soup)
# getCoinData(soup)


'''
NOTES :
    Good resources :
    https://beautiful-soup-4.readthedocs.io/en/latest/
    http://savvastjortjoglou.com/nba-draft-part01-scraping.html
'''