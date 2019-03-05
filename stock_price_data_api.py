import requests
import quandl
import pandas as pd
from bs4 import BeautifulSoup

#get the names of companies from polish stock exchange
url = 'https://www.bankier.pl/gielda/notowania/akcje?index=WIG'
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')

# Find the second table on the page
t = soup.find_all('table')[0]
df = pd.read_html(str(t))[0]

names_of_company = df["Walor AD"].values

names_of_company = list(names_of_company)

results = pd.DataFrame()
###############################################################################
#get data about Price, Volume, High, Low, Close and Open prices of stocks

for names in names_of_company:
    quandl.ApiConfig.api_key = 'api_key'
    x = quandl.get('WSE/%s' %names, start_date='2019-01-17', 
    end_date='2019-01-24',
    paginate=True)
    x['company'] = names
    results = results.append(x)

results = results.reset_index(drop=False)
pd.DataFrame.to_csv(results, 'WIG.csv')

#download data for WIG stock index
quandl.ApiConfig.api_key = 'api_key'
wig = quandl.get("WSE/WIG")
wig = pd.DataFrame(wig)

pd.DataFrame.to_csv(wig, 'WIG.csv')