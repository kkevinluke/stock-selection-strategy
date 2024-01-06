from main import Stock
class BenchmarkStrategy:
    def __init__(self, stock_list):
        self.stock_list = stock_list  # List of Stock objects
        self.nifty50_list = ["ICICIBANK","SBIN","AXISBANK","INDUSINDBK","HDFCBANK","RELIANCE","INFY","TATASTEEL","TITAN","NESTLEIND","APOLLOHOSP","TATACONSUM","HEROMOTOCO","EICHERMOT","SBILIFE","COALINDIA","BRITANNIA","NTPC","UPL","HINDUNILVR","SHREECEM","HINDALCO","TECHM","BHARTIARTL","BPCL","SUNPHARMA","ULTRACEMCO","JSWSTEEL","GRASIM","ASIANPAINT","DRREDDY","BAJFINANCE","MARUTI","HCLTECH","LT","WIPRO","TATAMOTORS","M&M","BAJAJ-AUTO","TCS","KOTAKBANK","POWERGRID","CIPLA","HDFCLIFE","DIVISLAB","ADANIPORTS","ONGC","ITC","BAJAJFINSV","HDFCBANK"]

    # Making the 2 main criteria for making the comparison.
    # Logic to evaluate selected stock strategy
    def evaluate_strategy_performance(self, start_date, end_date):
        positive_strategy_performance = 0

        stock_returns_sum = 0
        for stock in self.stock_list:
            stock_instance = Stock(stock)
            # Check if the stock has positive returns within the specified date range
            # Accessing the NDayRet Method from the Stock Class in the main file.
            stock_returns = stock_instance.n_day_ret((end_date - start_date).days, end_date)
            # ^ Assuming NDayRet method takes the number of days between start_date and end_date
            # Consider a stock's positive returns as part of the strategy's positive performance
            if stock_returns > 0:
                stock_returns_sum += stock_returns

        positive_strategy_performance = stock_returns_sum/len(self.stock_list)  # Avg of Stocks with Positive returns

        return positive_strategy_performance  # Number of stocks with positive returns as strategy performance

    # Logic to evaluate Nifty 50 strategy
    def calculate_nifty50_performance(self, start_date, end_date):

        # Creating Stock Instance for NIFTY 50
        stock_instance = Stock("NIFTY50")
        nifty50_returns = stock_instance.n_day_ret((end_date - start_date).days, end_date)
        # Considering positive returns as Nifty50 performance
        nifty50_performance = nifty50_returns if nifty50_returns and nifty50_returns > 0 else None

        return nifty50_performance  # Number of stocks with positive returns as strategy performance

    def compare_with_nifty50(self, start_date, end_date):

        # Simulated logic to compare the performance with Nifty50
        # You would typically use actual historical data and comparison metrics here
        active_strategy_performance = self.evaluate_strategy_performance(start_date, end_date)
        nifty50_performance = self.calculate_nifty50_performance(start_date, end_date)

        # Simulated result (comparison)
        comparison_result = {
            'ActiveStrategy': active_strategy_performance,
            'Nifty50Benchmark': nifty50_performance
        }
        return comparison_result


