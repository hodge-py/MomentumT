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
                uptrend = False
                ticker = stocks[x]
                ticker_data = yf.Ticker(stocks[x]).history(period="1y", interval="1d")
                ticker_data = ticker_data['Close']
                month_days = ticker_data[-30:]
                week_days = ticker_data[-7:]
                quarter_days = ticker_data[-90:]
                weekly_momentum = ((week_days.iloc[-1] - week_days.iloc[0]) / week_days.iloc[0]) * 100
                monthly_momentum = ((month_days.iloc[-1] - month_days.iloc[0]) / month_days.iloc[0]) * 100
                quarterly_momentum = ((quarter_days.iloc[-1] - quarter_days.iloc[0]) / quarter_days.iloc[0]) * 100

                currentPrice = ticker_data.iloc[-21]
                start_price = ticker_data.iloc[0]

                momentum_score = (currentPrice - start_price) / start_price * 100

                moving_200 = ticker_data.rolling(window=200).mean()
                current_price = ticker_data.iloc[-1]

                if momentum_score > 0.10 and current_price > moving_200.iloc[-1]:
                    uptrend = True


                container = [{'Ticker': ticker,'Sector': sector[x],'Category': category[x],'Weekly_Momentum': weekly_momentum,'Monthly_Momentum': monthly_momentum,'Quarterly_Momentum': quarterly_momentum, 'Momentum_Score': momentum_score, 'Uptrend': uptrend}]

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