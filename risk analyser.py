import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


class RiskAnalyzer:
    def __init__(self, ticker, start):
        self.ticker = ticker
        self.start = start
        self.data = yf.download(ticker, start=self.start)["Close"]

    def daily_returns(self):
        self.returns = self.data.pct_change().dropna()

    def price(self):
        lxt_price = self.data.iloc[-1]
        prv_price = self.data.iloc[-2]
        delta_price = (lxt_price - prv_price) / prv_price
        print("\nLast Price, yesterday price and delta price")
        for ticker in self.ticker:
            print(f"{ticker}: last {round(lxt_price[ticker],2)}$,"
                  f" prev {round(prv_price[ticker],2)}$ "
                  f"and {round(delta_price[ticker],2)} %")

    def daily_vol(self):
        self.vol = self.returns.std() * np.sqrt(252)
        print("\nAnnualized Volatility:")
        for ticker in self.ticker:
            print(f"{ticker}: {round(self.vol[ticker]*100,2)} %")

    def sharpe_ratio(self):
        annual_returns = self.returns.mean() * 252
        treasury_10y_yield = yf.download("^TNX", period="1d")["Close"]
        risk_free_rate = float(treasury_10y_yield.iloc[0]) / 100
        print(f"\nrisk free rate: {round(risk_free_rate * 100, 2)}%")
        sharpe_ratio = (annual_returns - risk_free_rate) / self.vol
        for ticker in self.ticker:
            print(f"sharpe ratio of {ticker}: {round(sharpe_ratio[ticker],2)}")
        avg_sharpe_ratio = sum(sharpe_ratio) / len(self.ticker)
        print(f"Average Sharpe Ratio of my portfolio: {round(avg_sharpe_ratio,2)}")

    def VaR(self):
        print("\nValue at Risk (95%):")
        var_list = []
        for ticker in self.ticker:
            var = np.percentile(self.returns[ticker], 5)
            var_list.append(var)
            print(f"{ticker}: {round(var * 100, 2)} %")
        avg_var = sum(var_list) / len(self.ticker)
        print(f"Average Value at Risk (95%): {round(avg_var * 100, 2)}%")

    def plot_returns(self):
        plt.plot(self.returns)
        plt.title('DAILY Returns')
        plt.xlabel('Date')
        plt.ylabel('DAILY Returns')
        plt.legend(self.ticker)
        plt.show()

user_input = input("Enter tickers separated by a comma: ")
tickers = user_input.replace(" ", "").split(",")
start = input("Enter start date (YYYY-MM-DD): ")

ra = RiskAnalyzer(tickers, start)
ra.daily_returns()
ra.price()
ra.daily_vol()
ra.sharpe_ratio()
ra.VaR()
ra.plot_returns()
