import datetime
from main import Stock


# Simulated function to fetch historical Nifty50 index prices
def fetch_nifty50_historical_prices(start_date, end_date):
    stock_instance = Stock('^NSEI')

    # Simulated historical prices (random values for demonstration)
    historical_prices = {}
    current_date = start_date
    while current_date <= end_date:
        price = stock_instance.cur_price(current_date)
        historical_prices[current_date] = price
        current_date += datetime.timedelta(days=1)
    return historical_prices

