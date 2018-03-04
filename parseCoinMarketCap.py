import requests
from bs4 import BeautifulSoup
import os, urllib2, sys, re

def returnPageTitle(soupObj):
    title = soupObj.find('h1', attrs={'id': 'title'})
    # title is a class of type <class 'bs4.element.Tag'>
    # so convert it into text, and strip starting and trailing
    return title.text.strip()

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
#print(soup.prettify())

# print returnPageTitle(soup)
# print findAllCoinUrl(soup)
# print "Total Coins on CoinMarketCap.com : ", findTotalCoins(soup)
# findCoin(soup)

#pageTitle = soup.find('h1')


mostTrendingCoin = soup.find_all(class_='sortable text-right')
#print mostTrendingCoin