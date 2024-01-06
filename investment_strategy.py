from main import Stock
import datetime

class InvestmentStrategy:
    def __init__(self, stock_list):
        self.stock_list = stock_list  # List of Stock objects

    def assess_monthly_performance(self, assessment_date):
        selected_stocks = []
        # For each stock in the stock list
        for stock_symbol in self.stock_list:
            stock_instance = Stock(stock_symbol)
            # Get the end date as the assessment date
            end_date = assessment_date
            # Calculate the start date as 30 days before the assessment date
            start_date = end_date - datetime.timedelta(days=30)
            # Calculate the N-day returns for the stock
            stock_returns = stock_instance.n_day_ret(30, end_date)
            # If the stock has positive returns, include it in the selected stocks
            if stock_returns is not None and stock_returns > 0:
                selected_stocks.append(stock_symbol)
        return selected_stocks

    def monthly_reassessment(self, assessment_date):
        # Call assess_monthly_performance method to get selected stocks
        selected_stocks = self.assess_monthly_performance(assessment_date)
        return selected_stocks
