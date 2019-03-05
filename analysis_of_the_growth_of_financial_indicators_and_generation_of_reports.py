import pandas as pd
import psycopg2
import numpy as np
from itertools import cycle
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime
from matplotlib.backends.backend_pdf import PdfPages

#get connection with DataBase
conn = psycopg2.connect(dbname='Financial_Data', user='postgres', + \
                        host='localhost', password='yourpassword')

df = pd.read_sql_query("""SELECT * 
                   FROM public."Financial_Data"
                   """,con=conn)

df = data_from_last_quarters = df.groupby('Name').head(5) #tutaj biorę tylko 5Q
                                                             #
quarters = cycle(['01-04-18','01-01-18','01-10-17','01-07-17','01-04-17',])

df['quarters'] = [next(quarters) for quarter in range(len(df))]

#calculate financial data
net_revenues_from_sales  = (df.groupby('Name')['net_revenues_from_sales']
       .agg([('a','last'),('net_revenues_from_sales','first')])
       .pct_change(axis=1)['net_revenues_from_sales']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

net_revenues_from_sales = net_revenues_from_sales.nlargest(3,'net_revenues_from_sales')


nett_profit  = (df.groupby('Name')['nett_profit_loss']
       .agg([('a','last'),('nett_profit_loss','first')])
       .pct_change(axis=1)['nett_profit_loss']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

nett_profit_loss = nett_profit_loss.nlargest(5,'nett_profit_loss')

      
EBITDA  = (df.groupby('Name')['EBITDA']
       .agg([('a','last'),('EBITDA','first')])
       .pct_change(axis=1)['EBITDA']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

EBITDA = EBITDA.nlargest(5,'EBITDA')

earnings_per_share  = (df.groupby('Name')['earnings_per_share']
       .agg([('a','last'),('earnings_per_share','first')])
       .pct_change(axis=1)['earnings_per_share']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

earnings_per_share = earnings_per_share.nlargest(5,'earnings_per_share')

book_value_per_share  = (df.groupby('Name')['book_value_per_share']
       .agg([('a','last'),('book_value_per_share','first')])
       .pct_change(axis=1)['book_value_per_share']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

book_value_per_share = book_value_per_share.nlargest(5,'book_value_per_share')

operating_profit_loss  = (df.groupby('Name')['operating profit_loss']
       .agg([('a','last'),('operating profit_loss','first')])
       .pct_change(axis=1)['operating profit_loss']
       .mul(100).round(0)
       .reset_index()
       .replace([np.inf, -np.inf], np.nan))

operating_profit_loss = operating_profit_loss.nlargest(5,'operating_profit_loss')

####################################################################
#create one big dataframe for financial results 
big_df = pd.concat([net_revenues_from_sales, operating_profit_loss, nett_profit_loss, EBITDA, + \
                    earnings_per_share, book_value_per_share], axis=1)

cols=pd.Series(big_df.columns)
for dup in big_df.columns.get_duplicates(): cols[big_df.columns.get_loc(dup)] =[dup+'.'+str(d_idx) 
    if d_idx!=0 else dup 
        for d_idx in range(big_df.columns.get_loc(dup).sum())]

arr = np.array(big_df)
count = Counter(arr.reshape(arr.size))

company = sorted(count.items(), key=lambda x: x[1],reverse=True)[:6]
company.pop(0)
flat_list = [item for sublist in company for item in sublist]

companys_to_chart = flat_list[0::2]

#######################################################################
#create plots for 3 companys with the best financial results into PDF
company_1 = df[df['Name'] == companys_to_chart[0]]
company_2 = df[df['Name'] == companys_to_chart[1]]
company_3 = df[df['Name'] == companys_to_chart[2]]

x = company_1['quarters']
z = company_1['nett_profit_loss']
v = company_1['operating profit_loss']
b = company_1['EBITDA']

conn_2 = psycopg2.connect(dbname='Financial_Data', user='postgres', + \
                          host='localhost', password='yourpassword')

df = pd.read_sql_query("""SELECT * 
                       FROM public."Stock_prices"
                       """,con=conn_2)

name_of_company = companys_to_chart[0]

n_groups = 5
###############################################################################
with PdfPages('Companies with the largest increase of profit..pdf') as pdf:
    #first company
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
     
    rects1 = plt.bar(index, z, bar_width,
                     alpha=opacity,
                     color='b',
                     label='nett_profit')
     
    rects2 = plt.bar(index + bar_width, v, bar_width,
                     alpha=opacity,
                     color='g',
                     label='operating profit_loss')
    
    rects3 = plt.bar(index + bar_width + bar_width, b, bar_width,
                     alpha=opacity,
                     color='y',
                     label='EBITDA')
     
    plt.xlabel('quarters')
    plt.ylabel('PLN')
    plt.title(companys_to_chart[0])
    plt.xticks(index + bar_width, x)
    plt.legend()
    ax.grid(True)
    
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    company = df.loc[(df['NameOfCompany'] == name_of_company) & (df['Date'] > datetime.date(2016,10,2))]
    
    company[['Open', 'High','Low','Close']] = company[['Open', 'High','Low','Close']].astype('float')

    WIG = pd.read_sql_query("""SELECT * 
                       FROM public."WIG"
                       """,con=conn)
    WIG[['Open', 'High','Low','Close']] = WIG[['Open', 'High','Low','Close']].astype('float')
    
    x = company['Date']
    y = company['Close']
    
    x1 = WIG['Date']
    y1 = WIG['Close']
    
    fig, ax = plt.subplots()
    
    ax.plot(x,y,label='Price')
    ax.set_ylabel("PLN")
    ax.set_xlabel("Date")
    
    ax2 = ax.twinx()
    ax2.plot(x1,y1, 'y-', label='WIG')
    
    myFmt = DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(myFmt)
    
    fig.autofmt_xdate()
    
    plt.ylabel('Points',size=10)
    plt.title(name_of_company)
    ax.grid(True)
    
    fig.legend(bbox_to_anchor=(0.85, 0.35))
    
    pdf.savefig()
    plt.close()
    ###########################################################################
    #second companyt
    x_1 = company_2['quarters']
    z_1 = company_2['nett_profit_loss']
    v_1 = company_2['operating profit_loss']
    b_1 = company_2['EBITDA']
    
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
     
    rects1 = plt.bar(index, z_1, bar_width,
                     alpha=opacity,
                     color='b',
                     label='nett_profit_loss')
     
    rects2 = plt.bar(index + bar_width, v_1, bar_width,
                     alpha=opacity,
                     color='g',
                     label='operating_profit_loss')
    
    rects3 = plt.bar(index + bar_width + bar_width, b_1, bar_width,
                     alpha=opacity,
                     color='y',
                     label='EBITDA')
     
    plt.xlabel('quarters')
    plt.ylabel('PLN')
    plt.title(companys_to_chart[1])
    plt.xticks(index + bar_width, x)
    plt.legend()
    ax.grid(True)
     
    plt.tight_layout()
    
    pdf.savefig()
    plt.close()
    
    name_of_company_1 = companys_to_chart[1]
    
    company = df.loc[(df['NameOfCompany'] == name_of_company_1) & (df['Date'] > datetime.date(2016,10,2))]
    
    company[['Open', 'High','Low','Close']] = company[['Open', 'High','Low','Close']].astype('float')
    
    WIG[['Open', 'High','Low','Close']] = WIG[['Open', 'High','Low','Close']].astype('float')
    
    x = company['Date']
    y = company['Close']
    
    x1 = WIG['Date']
    y1 = WIG['Close']
    
    fig, ax = plt.subplots()
    ax.plot(x,y,label='Price')
    ax.set_ylabel("PLN")
    ax.set_xlabel("Date")
    
    ax2 = ax.twinx()
    ax2.plot(x1,y1, 'y-', label='WIG')
    
    myFmt = DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(myFmt)
    
    fig.autofmt_xdate()
    
    plt.ylabel('Points',size=10)
    plt.title(name_of_company_1)
    ax.grid(True)
    
    fig.legend(bbox_to_anchor=(0.85, 0.35))
    
    pdf.savefig()
    plt.close()
    ###########################################################################
    #third company 
    x_2 = company_2['quarters']
    z_2 = company_2['nett_profit_loss']
    v_2 = company_2['operating_profit_loss']
    b_2 = company_2['EBITDA']
    
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
     
    rects1 = plt.bar(index, z_2, bar_width,
                     alpha=opacity,
                     color='b',
                     label='nett_profit_loss')
     
    rects2 = plt.bar(index + bar_width, v_2, bar_width,
                     alpha=opacity,
                     color='g',
                     label='operating_profit_loss')
    
    rects3 = plt.bar(index + bar_width + bar_width, b_2, bar_width,
                     alpha=opacity,
                     color='y',
                     label='EBITDA')
     
    plt.xlabel('quarters')
    plt.ylabel('PLN')
    plt.title(companys_to_chart[2])
    plt.xticks(index + bar_width, x)
    plt.legend()
    ax.grid(True)
    
    plt.tight_layout()
    
    pdf.savefig()
    plt.close()
    
    name_of_company_2 = companys_to_chart[2]
    
    company = df.loc[(df['NameOfCompany'] == name_of_company_2)& (df['Date'] > datetime.date(2016,10,2))]
    company[['Open', 'High','Low','Close']] = company[['Open', 'High','Low','Close']].astype('float')
    
    WIG[['Open', 'High','Low','Close']] = WIG[['Open', 'High','Low','Close']].astype('float')
    
    x = company['Date']
    y = company['Close']
    
    x1 = WIG['Date']
    y1 = WIG['Close']
    
    fig, ax = plt.subplots()
    ax.plot(x,y,label='Price')
    ax.set_ylabel("PLN")
    ax.set_xlabel("Date")
    
    ax2 = ax.twinx()
    ax2.plot(x1,y1, 'y-', label='WIG')
    
    myFmt = DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(myFmt)
    
    fig.autofmt_xdate()
    
    plt.ylabel('Points',size=10)
    plt.title(name_of_company_2)
    ax.grid(True)
    
    fig.legend(bbox_to_anchor=(0.85, 0.35))
    
    pdf.savefig()
    plt.close()