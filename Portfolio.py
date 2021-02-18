import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

#Create dictionary for stocks and their prices for the past 20 days
stockDictionary = {"AAPL":[],"FB":[],"TSLA":[],"NFLX":[],"GOOG":[],"AMZN":[],"CAKE":[]}

#List of ticker symbols
tickers = ['AAPL','FB','TSLA','NFLX','GOOG','AMZN','CAKE']

#Web scrape closing price data for each stock and populate dictionary with the data
for i in range(len(tickers)):
    html = "https://www.marketwatch.com/investing/stock/"+tickers[i]+"/download-data?siteid=mktw&date=01162020&x=11&y=8"
    r = requests.get(html)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    table = soup.find('table', {'class':'table table--overflow align--center'})

    rows = table.find_all('tr')

    for row in rows:
        data = row.find_all('td')
        if (len(data) > 0):
            cell = data[4]
            cellStr = cell.text
            cellStr = cellStr[1::]
            cellStr = cellStr.replace(',','')
            value = float(cellStr)
            
            stockDictionary[tickers[i]].append(value)

#Create a pandas dataframe with the dictionary data
df = pd.DataFrame(stockDictionary)

assets = df.columns

#Mean historical return for each company
mu = expected_returns.mean_historical_return(df)

#Risk models sample covariance matrix
S = risk_models.sample_cov(df)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)

ef.portfolio_performance(verbose=True)

#User defined budget
pf_val = 2500
latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = pf_val)
allocation, leftover = da.lp_portfolio()
print('Stock Allocation: ', allocation)
print('Funds Remaining: ${:.2f}'.format(leftover))
