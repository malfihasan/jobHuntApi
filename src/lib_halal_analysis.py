import os
import json
import matplotlib.pyplot as plt
from math import sqrt

from src.lib_common import   get_db, create_connection
from src.settings import *

import yfinance as yf
import yahoo_fin.stock_info as si # depricate this pacakge 
import finvizfinance
from yahoofinancials import YahooFinancials

import time
from datetime import date, datetime, timedelta
from dateutil import tz

class stock_summary_generator:
    
    def __init__(self,  cur_time = None):
        self.target_date = time.strftime("%Y%m%d") if cur_time is None else cur_time 
        self.stock_list = self.convert_to_list(get_db(table_name="halal_stocks"))

        dict_list = self.load_detail_table().to_dict('records')
        self.stock_detail_dict = { i["Ticker"]:i for i in dict_list}

    def initiate_detail_table(self):
        conn = create_connection('data/halal_screening.db')
        c = conn.cursor()
        c.execute(CreateBDQuery)
        conn.commit()
        c.close()

    def convert_to_list(self, df):
        df['index'] = df.Symbol
        df.reset_index()
        return df.set_index('index').to_dict('records')
    
    def load_detail_table(self,detail_table_name = "stock_database"):
        return get_db(detail_table_name)
    

    def analysis_trigger_check(self, ticker):
        pass

    def earning_analysis(self, tickerEarningDF):

        # convert dataframe to list records
        earning_list = tickerEarningDF.to_dict('index')

        print(list(earning_list.keys())[0].strftime('%Y%m%d'))

        # get the current date
        current_date = date.today()


        # get the last earning date info
        last_earning_date = sorted([earning_date for earning_date, _ in earning_list.items() if earning_date.date()  < current_date])
        if len(last_earning_date)>0:
            last_earning_date = last_earning_date[-1]

        next_earning_date = sorted([earning_date for earning_date, _ in earning_list.items() if earning_date.date()  > current_date])
        if len(next_earning_date)>0:
            next_earning_date = next_earning_date[0]
        
        # get the next earning date info
        next2week = current_date + timedelta(days=14)
        next3week = current_date + timedelta(days=21)
        nextweek = current_date + timedelta(days=7)

        next2week = date.today() + timedelta(days=14)
        next3week = date.today() + timedelta(days=21)
        next4week = date.today() + timedelta(days=28)
        nextweek = date.today() + timedelta(days=7)

        as_date = next_earning_date.date()


        week_after_earning = True if (as_date >= next2week ) & (as_date < next3week) else False 

        two_week_after_earning = True if (as_date >= next3week ) & (as_date < next4week) else False 

        next_week_earning = True if (as_date >= nextweek ) & (as_date < next2week) else False 

        print( week_after_earning, two_week_after_earning, next_week_earning)
        print(last_earning_date)
        print(next_earning_date)

        return {
            "HasEarningWeekAfter": week_after_earning,
            "HasEarningTwoWeekAfter": two_week_after_earning,
            "HasEarningNextWeek": next_week_earning,
            "LastEarningDate": last_earning_date,
            "NextEarningDate": next_earning_date,
            "LastEarningInfo": earning_list[last_earning_date],
            "NextEarningInfo": earning_list[next_earning_date]
        }


    def process_stock(self, tickerSymbol):

        ## make a empty 
        stock_info_dict = {}
        
        ## base free connector 
        #get data on this ticker
        
        # yf info package 
        tickerData = yf.Ticker(tickerSymbol) # working 
        tickerDataInfo = tickerData.info
        
        # yf earning package 
        tickerDataEarningDF =  tickerData.earnings_dates
        earning_dict = self.earning_analysis(tickerDataEarningDF)
        print(earning_dict)

        # # yahoofinancials package
        # yahoo_financials = YahooFinancials(tickerSymbol)

        # # finvizfinance package
        # stock = finvizfinance.quote.finvizfinance(tickerSymbol)  # working !



        ## Assigning values:
        # 'Market_Cap' 
        stock_info_dict['Market_Cap'] = tickerDataInfo['marketCap']

        # 'EPS',
        stock_info_dict['EPS'] = tickerDataInfo['trailingEps']

        # 'Week52High',
        stock_info_dict['Week52High'] = tickerDataInfo['fiftyTwoWeekHigh']

        # 'Week52Low' ,
        stock_info_dict['Week52Low'] = tickerDataInfo['fiftyTwoWeekLow']

        # 'Y1TargetEst' ,
        stock_info_dict['Y1TargetEst'] = tickerDataInfo['targetMeanPrice']

        # # 'ExDividendDate',
        # stock_info_dict['ExDividendDate'] = tickerDataInfo['exDividendDate']

        # 'ExEarningDate',
        stock_info_dict['ExEarningDate'] = earning_dict['LastEarningDate'].date().strftime('%Y%m%d')

        # 'ForwardDividendYield',
        stock_info_dict['ForwardDividendYield'] = tickerDataInfo['dividendYield']

        # 'NextEarning',
        stock_info_dict['NextEarning'] =  earning_dict['NextEarningDate'].date().strftime('%Y%m%d')

        # 'Country',
        stock_info_dict['Country'] = tickerDataInfo['country']

        # 'State',
        stock_info_dict['State'] = tickerDataInfo['state']

        # 'Sector',
        stock_info_dict['Sector'] = tickerDataInfo['sector']

        # 'DividendRate',
        stock_info_dict['DividendRate'] = tickerDataInfo['dividendRate']

        # 'PbyERatio',
        stock_info_dict['PbyERatio'] = tickerDataInfo['trailingPE']

        # 'Volume',
        stock_info_dict['Volume'] = tickerDataInfo['volume']

        # 'PbySReal',
        stock_info_dict['PbySReal'] = tickerDataInfo['priceToSalesTrailing12Months']

        # 'Dividend',
        stock_info_dict['Dividend'] = tickerDataInfo['dividendRate']

        # 'LTDebtEq',   
        stock_info_dict['LTDebtEq'] = tickerDataInfo['debtToEquity']

        # # 'NearestEarnings',
        # stock_info_dict['NearestEarnings'] = tickerDataInfo['earningsTimestamp']

        # 'Recommendation',
        stock_info_dict['Recommendation'] = tickerDataInfo['recommendationKey']

        # 'StockIndex',
        stock_info_dict['StockIndex'] = tickerDataInfo['exchange']

        # 'ProfitMargin',
        stock_info_dict['ProfitMargin'] = tickerDataInfo['profitMargins']

        # 'Income',
        stock_info_dict['Income'] = tickerDataInfo['totalRevenue']

        # 'UpdateDte',  
        stock_info_dict['UpdateDte'] = self.target_date

        # 'HasEarningWeekAfter',
        stock_info_dict['HasEarningWeekAfter'] = False

        # 'HasEarningTwoWeekAfter',
        stock_info_dict['HasEarningTwoWeekAfter'] = False

        # 'HasEarningNextWeek'
        stock_info_dict['HasEarningNextWeek'] = False

        # # 'CashAndCashEquivalents',
        # stock_info_dict['CashAndCashEquivalents'] = tickerDataInfo['cash']

        # # 'Receivables',
        # stock_info_dict['Receivables'] = tickerDataInfo['receivables']

        # # 'CurrentAssets',
        # stock_info_dict['CurrentAssets'] = tickerDataInfo['totalCurrentAssets']

        # # 'TotalAssets',
        # stock_info_dict['TotalAssets'] = tickerDataInfo['totalAssets']

        # # 'CurrentLiabilities',
        # stock_info_dict['CurrentLiabilities'] = tickerDataInfo['totalCurrentLiabilities']

        # # 'TotalEquity',
        # stock_info_dict['TotalEquity'] = tickerDataInfo['totalStockholderEquity']

        # # 'TotalRevenue',
        # stock_info_dict['TotalRevenue'] = tickerDataInfo['totalRevenue']

        # # 'TotalDebt',
        # stock_info_dict['TotalDebt'] = tickerDataInfo['totalDebt']

        # # 'TotalEquityV2',
        # stock_info_dict['TotalEquityV2'] = tickerDataInfo['totalStockholderEquity']

        # # 'NetInterestIncome',
        # stock_info_dict['NetInterestIncome'] = tickerDataInfo['netInterestIncome']

        # 'DJIMFinal',
        stock_info_dict['DJIMFinal'] = False

        # 'FTSEFinal',
        stock_info_dict['FTSEFinal'] = False

        # 'MSCIFinal',
        stock_info_dict['MSCIFinal'] = False

        # 'MSCIMFinal',
        stock_info_dict['MSCIMFinal'] = False

        # 'SPSFinal',
        stock_info_dict['SPSFinal'] = False

        # 'WAHFinal',
        stock_info_dict['WAHFinal'] = False

        # 'AAOIFIFinal',
        stock_info_dict['AAOIFIFinal'] = False
    
        # 'PERSONFinal',
        stock_info_dict['PERSONFinal'] = False

        # 'Updatedecision'
        stock_info_dict['Updatedecision'] = " "
    

        return tickerDataInfo, stock_info_dict


        #get data on this ticker
        tickerData = yf.Ticker(tickerSymbol) # working 
        print(tickerData.info)
        #siDict = si.get_quote_table(tickerSymbol) # not working 
        # siDict = si.get_analysts_info(tickerSymbol) # working 
        # print(siDict)
        # # try:
        # #     stock = finvizfinance(tickerSymbol) 
        # #     stock_fundamental = stock.TickerFundament()
        # # except:
        # #     stock_fundamental = {}
        # #     stock_fundamental['Null'] = 0.0
        # stock = finvizfinance.quote.finvizfinance(tickerSymbol)  # working ! 
        # print(stock.ticker_fundament())
        # from finvizfinance.earnings import Earnings

        # #print(finvizfinance.insider.Insider(option='latest'))
        # print(finvizfinance.earnings.Earnings(period='Next Week').output_csv( filename = "data/next_week_earning.csv"))

        # dfStockList.at[tickerSymbol, 'update_time'] = datetime.strftime(date.today(), "%Y-%m-%d")



        # #get the historical prices for this ticker

        # try:
        #     er_date = si.get_next_earnings_date(tickerSymbol).strftime("%Y-%m-%d")
        #     dfStockList.at[tickerSymbol, 'Next_earning'] = er_date
        #     k1, k2, k3 = self.update_earning(er_date)
        #     dfStockList.at[tickerSymbol, 'next_week_earning'] = k1
        #     dfStockList.at[tickerSymbol, 'week_after_earning'] = k2
        #     dfStockList.at[tickerSymbol, 'two_week_after_earning'] = k3
            
        # except:
        #     dfStockList.at[tickerSymbol, 'Next_earning'] = " "




        # dfStockList.at[tickerSymbol, 'Market_Cap'] = siDict['Market Cap']
        # dfStockList.at[tickerSymbol, 'P/E_ratio'] = siDict['PE Ratio (TTM)']
        # dfStockList.at[tickerSymbol, 'Volume'] = siDict['Volume']

        # dfStockList.at[tickerSymbol, 'EPS'] = siDict['EPS (TTM)']

        # dfStockList.at[tickerSymbol, '1y_Target_Est'] = siDict['1y Target Est']

        # dfStockList.at[tickerSymbol, 'Ex-Dividend_Date'] = siDict['Ex-Dividend Date']

        # dfStockList.at[tickerSymbol, 'Forward_Dividend_n_Yield'] = siDict['Forward Dividend & Yield']

        # siInfo = dict(tickerData.info)
        # if 'country' in siInfo.keys():
        #     dfStockList.at[tickerSymbol, 'Country'] = siInfo['country']

        # if 'state' in siInfo.keys():
        #     dfStockList.at[tickerSymbol, 'State'] = siInfo['state']

        # if 'sector' in siInfo.keys():
        #     dfStockList.at[tickerSymbol, 'Sector'] = siInfo['sector']

        # if 'dividendRate' in siInfo.keys():
        #     dfStockList.at[tickerSymbol, 'DividendRate'] = siInfo['dividendRate']

        # if 'P/S' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'P/S'] = stock_fundament['P/S']

        # if 'Dividend %' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Dividend_%'] = stock_fundament['Dividend %']

        # if 'LT Debt/Eq' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'LT_Debt/Eq'] = stock_fundament['LT Debt/Eq']

        # if 'Target Price' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Target_Price'] = stock_fundament['Target Price']

        # if 'Earnings' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Nearest_Earnings'] = stock_fundament['Earnings']

        # if 'Recom' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Recommendation'] = stock_fundament['Recom']

        # if 'Index' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Index'] = stock_fundament['Index']

        # if 'Profit Margin' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Profit_margin'] = stock_fundament['Profit Margin']

        # if 'Income' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, 'Income'] = stock_fundament['Income']

        # if '52W Range From' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, '52_Week_Low'] = stock_fundament['52W Range From']

        # if '52W Range To' in stock_fundament.keys():
        #     dfStockList.at[tickerSymbol, '52_Week_High'] = stock_fundament['52W Range To']

        # return dfStockList.copy(), siDict['Market Cap']

        #return siDict


    def iterate_stock_list(self):
        for stock in self.stock_list:
            ## process stock

            yield stock
    

