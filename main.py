import pandas as pd
import numpy as np
import yfinance as yf
import time

class MomentumT:
    def __init__(self):
        self.week = "1wk"
        self.month = "1mo"
        self.quarter = "3mo"


    def calculate_momentum(self):
        stocks, sector, category = self.grab_stock_symbols()
        stockFrame = pd.DataFrame(columns=['Ticker', 'Sector', 'Category', 'Weekly_Momentum', 'Monthly_Momentum', 'Quarterly_Momentum'])

        for x in range(len(stocks)):
            try:
                ticker = stocks[x]
                ticker_data = yf.Ticker(stocks[x]).history(period="6mo", interval="1d")
                ticker_data = ticker_data['Close']
                month_days = ticker_data[-30:]
                week_days = ticker_data[-7:]
                quarter_days = ticker_data[-90:]
                weekly_momentum = ((week_days.iloc[-1] - week_days.iloc[0]) / week_days.iloc[0]) * 100
                monthly_momentum = ((month_days.iloc[-1] - month_days.iloc[0]) / month_days.iloc[0]) * 100
                quarterly_momentum = ((quarter_days.iloc[-1] - quarter_days.iloc[0]) / quarter_days.iloc[0]) * 100
                container = [{'Ticker': ticker,'Sector': sector[x],'Category': category[x],'Weekly_Momentum': weekly_momentum,'Monthly_Momentum': monthly_momentum,'Quarterly_Momentum': quarterly_momentum }]

                stockFrame = pd.concat([stockFrame, pd.DataFrame(container)], ignore_index=True)

                time.sleep(2)

            except Exception as e:
                print(f"An error occurred: {e}")
                
        
        return stockFrame.sort_values(by=['Quarterly_Momentum','Monthly_Momentum','Weekly_Momentum'], ascending=False)


    def grab_stock_symbols(self):
        stocks = pd.read_csv('symbols.csv')['Ticker Symbol'].tolist()
        sector = pd.read_csv('symbols.csv')['Sector'].tolist()
        category = pd.read_csv('symbols.csv')['Category'].tolist()
        return stocks, sector, category

if __name__ == "__main__":
    momentum_t = MomentumT()
    signals = momentum_t.calculate_momentum()
    signals.to_csv('momentum_signals.csv', index=False)