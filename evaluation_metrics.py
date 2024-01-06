from main import Stock
import numpy as np
import datetime


class EvaluationMetrics:
    def __init__(self, stock_list):
        self.stock_list = stock_list  # List of Stock objects

    def calculate_cagr(self, stock_symbol, start_date, end_date):
        '''Compound Annual Growth Rate'''
        stock_instance = Stock(stock_symbol)
        start_price = stock_instance.cur_price(start_date)
        end_price = stock_instance.cur_price(end_date)

        if start_price is None or end_price is None:
            return None

        time_period = (end_date - start_date).days / 365.0
        cagr = ((end_price / start_price) ** (1 / time_period)) - 1
        return cagr * 100  # Convert to percentage

    def calculate_volatility(self, stock_symbol, start_date, end_date):
        '''Volatility'''
        stock_instance = Stock(stock_symbol)
        daily_returns = []
        cur_date = start_date

        while cur_date <= end_date:
            cur_price = stock_instance.cur_price(cur_date)
            prev_date = cur_date - datetime.timedelta(days=1)
            prev_price = stock_instance.cur_price(prev_date)
            if cur_price is not None and prev_price is not None:
                daily_returns.append((cur_price / prev_price) - 1)
            cur_date += datetime.timedelta(days=1)  # going to next date

        if not daily_returns:
            return None

        volatility = np.std(daily_returns) * np.sqrt(252)  # 252 trading days in a year
        return volatility * 100  # Convert to percentage

    def calculate_sharpe_ratio(self, stock_symbol, start_date, end_date):
        '''Sharpe Ratio - Measures risk adjusted relative returns'''
        risk_free_rate = 0.05  # Example risk-free rate
        cagr = self.calculate_cagr(stock_symbol, start_date, end_date)
        volatility = self.calculate_volatility(stock_symbol, start_date, end_date)

        if cagr is None or volatility is None:
            return None

        sharpe_ratio = (cagr - risk_free_rate) / volatility
        return sharpe_ratio

    def evaluate_nifty_index(self, start_date, end_date):
        '''Evaluate nifty with all Metrics'''
        nifty_symbol = "^NSEI"
        cagr = self.calculate_cagr(nifty_symbol, start_date, end_date)
        volatility = self.calculate_volatility(nifty_symbol, start_date, end_date)
        sharpe_ratio = self.calculate_sharpe_ratio(nifty_symbol, start_date, end_date)
        return {'CAGR (%)': cagr, 'Volatility (%)': volatility, 'Sharpe Ratio': sharpe_ratio}

    def evaluate_strategy(self, strategy_stocks, start_date, end_date):
        '''Evaluate strategy with all Metrics'''
        # You should pass the list of stocks in the strategy as strategy_stocks
        # Calculate metrics for the strategy based on the list of stocks provided
        cagr_list, volatility_list, sharpe_ratio_list = [], [], []

        for stock_symbol in strategy_stocks:
            cagr = self.calculate_cagr(stock_symbol, start_date, end_date)
            volatility = self.calculate_volatility(stock_symbol, start_date, end_date)
            sharpe_ratio = self.calculate_sharpe_ratio(stock_symbol, start_date, end_date)

            if cagr is not None and volatility is not None and sharpe_ratio is not None:
                cagr_list.append(cagr)
                volatility_list.append(volatility)
                sharpe_ratio_list.append(sharpe_ratio)

        avg_cagr = np.mean(cagr_list)
        avg_volatility = np.mean(volatility_list)
        avg_sharpe_ratio = np.mean(sharpe_ratio_list)

        return {'CAGR (%)': avg_cagr, 'Volatility (%)': avg_volatility, 'Sharpe Ratio': avg_sharpe_ratio}

    # This method is basically the NIFTY50 Index, but we will iterate through all the 50 stocks here.
    def evaluate_benchmark_allocation(self, benchmark_stocks, start_date, end_date):
        cagr_list, volatility_list, sharpe_ratio_list = [], [], []

        for stock_symbol in benchmark_stocks:
            cagr = self.calculate_cagr(stock_symbol, start_date, end_date)
            volatility = self.calculate_volatility(stock_symbol, start_date, end_date)
            sharpe_ratio = self.calculate_sharpe_ratio(stock_symbol, start_date, end_date)

            if cagr is not None and volatility is not None and sharpe_ratio is not None:
                cagr_list.append(cagr)
                volatility_list.append(volatility)
                sharpe_ratio_list.append(sharpe_ratio)

        avg_cagr = np.mean(cagr_list)
        avg_volatility = np.mean(volatility_list)
        avg_sharpe_ratio = np.mean(sharpe_ratio_list)

        return {'CAGR (%)': avg_cagr, 'Volatility (%)': avg_volatility, 'Sharpe Ratio': avg_sharpe_ratio}
