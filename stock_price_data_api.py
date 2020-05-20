import requests
import quandl
import pandas as pd
from bs4 import BeautifulSoup

#get the names of companies from polish stock exchange
url = 'https://www.bankier.pl/gielda/notowania/akcje?index=WIG'
page = requests.get(url)

soup = BeautifulSoup(page.content,'html.parser')

# Find the second table on the page
t = soup.find_all('table')[0]
df = pd.read_html(str(t))[0]

names_of_company = df["Walor AD"].values

names_of_company = list(names_of_company)

results = pd.DataFrame()
###############################################################################
#get data about Price, Volume, High, Low, Close and Open prices of stocks

#remove NaN
for i in range(len(names_of_company)):
    names_of_company[i] = str(names_of_company[i])

names_of_company_without_nan = [x for x in names_of_company if x != 'nan']

for names in names_of_company_without_nan:
    quandl.ApiConfig.api_key = 'AZ964MpikzEYAyLGfJD2'
    try:
        x = quandl.get('WSE/%s' %names, start_date='2019-01-17',     end_date='2019-01-24',    paginate=True)
        x['company'] = names
        results = results.append(x)
    #Jeśli wywali się w tym 'try' to bierze następny w kolejce i leci dalej
    except:
        next

results = results.reset_index(drop=False)
pd.DataFrame.to_csv(results, 'WIG_COMPANY.csv')


#download data for WIG stock index
quandl.ApiConfig.api_key = 'AZ964MpikzEYAyLGfJD2'
wig20 = quandl.get("WSE/WIG20")
wig20 = pd.DataFrame(wig20)

pd.DataFrame.to_csv(wig20, 'WIG20.csv')

wig = quandl.get("WSE/WIG")
wig = pd.DataFrame(wig)

pd.DataFrame.to_csv(wig, 'WIG.csv')
