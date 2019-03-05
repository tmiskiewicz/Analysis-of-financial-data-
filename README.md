Download and analysis of financial data in Python

In repositorie you can find 3 scripts (financial_data_web_scraping, stock_price_data_api and 
analysis_of_the growth_of_financial_indicators_and_generation_of_reports )  that allow on download 
financial statements about polish companys from website www.bankier.pl
and price of stocks from www.quandl.com

1. Financial data web scraping script allows you to download all financial data about polish companys that are listed on
   the Warsaw Stock Exchange. You can scrap data like: net revenues from sales, nett profit loss, EBITDA, earnings
   per share, book value per share, operating profit/loss. All data are convert into CSV file. After that it can be load
   into database PGadmin as Financial Data
2. Stock price data web scraping allows you to download  High, Low, Close and Open prices of stocks and Volume of trades
   of all polish companies. You can also download all those data for polish the warsaw stock exchange index.
3. The last script helps you to analysis of the growth of financial indicators and generation of reports. In this case you 
   check three companies that have the highest growth of nett profit loss, operating profit_loss and EBITDA. After that 
   script returns PDF report with charts of price stocks and campers with the Warsaw Stock Exchange index. It also shows 
   charts with financial data (growth of nett profit loss, operating profit loss and EBITDA). Script can be easily modifying 
   and shows another financial data.