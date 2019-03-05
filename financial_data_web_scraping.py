import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.bankier.pl/gielda/notowania/akcje?index=WIG'
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
# Find the second table on the page
t = soup.find_all('table')[0]

#Read the table into a Pandas DataFrame
df = pd.read_html(str(t))[0]

#get names of company 
names_of_company = df["Walor AD"].values
    
for name in names_of_company: 
    url2 = 'https://www.bankier.pl/gielda/notowania/akcje/{}/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/1'.format(name)
    
    page2 = requests.get(url2)

    soup = BeautifulSoup(page2.content,'lxml')
# Find the second table on the page
    try:
        t2 = soup.find_all('table')[0]
        df2 = pd.read_html(str(t2))[0]
        df2['company_name'] = name

        with open('financial_results12.csv', 'a') as f:
            df2.to_csv(f, header=False)
    except:
        pass