# Portfolio-Optimizer
Python application to determine the best quantity/mixture of stocks to purchase based off of a user-given list of desired stocks, and their total budget.

BeautifulSoup is used to scrape historical stock data of user-defined companies 

A pandas dataframe is then populated with the scraped data where each company is its own column

The PyPortfolioOpt library is used to calculate the expected return and covariance matrix.
Based on the user's budget, a list of allocated stocks are printed with the quantity of stock that should be bought
