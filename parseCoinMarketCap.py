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

baseUrl = "https://coinmarketcap.com"
page = requests.get(baseUrl)
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

# print returnPageTitle(soup)
# print returnTableHeading(soup)
# print findAllCoinUrl(soup)
# print "Total Coins on CoinMarketCap.com : ", findTotalCoins(soup)
# findCoin(soup)


'''
Trying to find first two rows of the page
    Great resource : http://savvastjortjoglou.com/nba-draft-part01-scraping.html
'''
allRows = soup.find_all('tr',limit=2)
# print allRows
''' This returns the 1st row of the table : Name | Market Cap | Price | Volume (24h) | Circulating Suppy | Change (24h) | Price Graph (24h) '''
#print allRows[0].findAll('th')
columnHeaders = [th.getText() for th in allRows[0].findAll('th')]
for heading in columnHeaders:
    print heading

