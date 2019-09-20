# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:06:04 2019
Manejo de portafolio de criptomonedas
@author: AAW
"""
import os
import json
from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

listingURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
sourceFile = 'portfolio.txt'
portfolioValue = 0.00

parameters = {
  'start':'1',
  'limit':'5000',
  'convert': 'USD' 
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '502ca910-c0d7-4d9a-84a5-6fe2bbff17f4',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(listingURL, params=parameters)
  data = json.loads(response.text)
  criptocurrencies = data['data']
  
# almaceno la información relevante en un diccionario
  criptoDic = {}
    
  for criptocurrency in criptocurrencies:
    name = criptocurrency['name']
    symbol = criptocurrency['symbol']
    quotes = criptocurrency['quote']
    price = float(quotes['USD']['price'])
    pc1h = quotes['USD']['percent_change_1h']
    pc24h = quotes['USD']['percent_change_24h']
    pc7d = quotes['USD']['percent_change_7d']
    
    #str_price = '{0:6.2f}'.format(price)
    
    criptoDic.update({symbol:[name, price, pc1h, pc24h, pc7d]})
  #print(criptoDic)  
  print()
  print('MY PORTFOLIO')
  print()
  table = PrettyTable(['Asset', 'symbol', 'Amount owned', 'Value', 'Price', '1h', '24h', '7d'])
      
# Se carga el archivo fuente de criptomonedas
  with open(sourceFile) as archivo:
        for line in archivo:
            ticker, amount = line.split()
            ticker = ticker.upper()
            amount = float(amount)
            ticker_name =  criptoDic[ticker][0]
            ticker_price = round(criptoDic[ticker][1],2)
            ticker_pc1h = round(criptoDic[ticker][2], 2)
            ticker_pc24h = round(criptoDic[ticker][3], 2)
            ticker_7d = round(criptoDic[ticker][4], 2)
            value = float(amount * ticker_price)
            portfolioValue += value
            
            if ticker_pc1h > 0:
                ticker_pc1h = Back.GREEN + str(ticker_pc1h) + '%' + Style.RESET_ALL
            else:
                ticker_pc1h = Back.RED + str(ticker_pc1h) + '%' + Style.RESET_ALL
                
            if ticker_pc24h > 0:
                ticker_pc24h = Back.GREEN + str(ticker_pc24h) + '%' + Style.RESET_ALL
            else:
                ticker_pc24h = Back.RED + str(ticker_pc24h) + '%' + Style.RESET_ALL
            
            if ticker_7d > 0:
                ticker_7d = Back.GREEN + str(ticker_7d) + '%' + Style.RESET_ALL
            else:
                ticker_7d = Back.RED + str(ticker_7d) + '%' + Style.RESET_ALL
            
            valueString= '{:,}'.format(round(value,2))
            portfolioValueString = '{:,}'.format(round(portfolioValue,2))
            #print(ticker_name, ticker, amount, valueString, portfolioValueString, ticker_pc1h,ticker_pc24h, ticker_7d)
            table.add_row([ticker_name,
                             ticker,
                             str(amount),
                             '$' + valueString,
                             '$' + str(ticker_price),
                             str(ticker_pc1h),
                             str(ticker_pc24h),
                             str(ticker_7d)])
  print(table)
  print('Portafolio Total: ' + Back.GREEN + 'US $' + portfolioValueString + Style.RESET_ALL)
    
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
