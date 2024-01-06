import datetime
import requests


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.historical_data = None
        self._download_data()

    def _download_data(self):
        # Download historical data from Yahoo Finance API
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1=0&period2={int(datetime.datetime.now().timestamp())}&interval=1d&events=history"
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            self.historical_data = response.text
        else:
            self.historical_data = None  # Handle error if data retrieval fails

    def cur_price(self, cur_date):
        # Get the closing price for the specified date
        if self.historical_data:
            lines = self.historical_data.strip().split('\n')
            header = lines[0]
            data = [line.split(',') for line in lines[1:]]
            date_index = header.split(',').index('Date')
            close_index = header.split(',').index('Close')
            for row in data:
                if row[date_index] == cur_date:
                    return float(row[close_index])
            return None  # Handle if data for the specified date is not available
        else:
            return None  # Handle if historical data is not available

    def n_day_ret(self, N, cur_date):
        # Calculate N-day returns based on the specified date
        if self.historical_data:
            lines = self.historical_data.strip().split('\n')
            header = lines[0]
            data = [line.split(',') for line in lines[1:]]
            date_index = header.split(',').index('Date')
            close_index = header.split(',').index('Close')
            cur_date_index = -1
            for i, row in enumerate(data):
                if row[date_index] == cur_date:
                    cur_date_index = i
                    break
            if cur_date_index != -1 and cur_date_index - N >= 0:
                cur_price = float(data[cur_date_index][close_index])
                n_day_price = float(data[cur_date_index - N][close_index])
                return (cur_price / n_day_price) - 1
            else:
                return None  # Handle if data for the specified date or N days ago is not available
        else:
            return None  # Handle if historical data is not available

    def daily_ret(self, cur_date):
        # Calculate daily returns for the specified date
        return self.n_day_ret(1, cur_date)

    def last_30_days_price(self, cur_date):
        # Get an array of last 30 days prices before the specified date
        if self.historical_data:
            lines = self.historical_data.strip().split('\n')
            header = lines[0]
            data = [line.split(',') for line in lines[1:]]
            date_index = header.split(',').index('Date')
            close_index = header.split(',').index('Close')
            cur_date_index = -1
            for i, row in enumerate(data):
                if row[date_index] == cur_date:
                    cur_date_index = i
                    break
            if cur_date_index != -1 and cur_date_index - 30 >= 0:
                last_30_days_prices = [float(data[cur_date_index - i][close_index]) for i in range(1, 31)]
                return last_30_days_prices
            else:
                return None  # Handle if data for the specified date or last 30 days is not available
        else:
            return None  # Handle if historical data is not available



# Example usage:
ticker_symbol = '^NSEI'  # Replace 'AAPL' with the desired stock ticker
stock = Stock(ticker_symbol)

# Get the closing price for a specific date
print(f"Closing price on 2022-06-15: {stock.cur_price('2022-06-15')}")

# Get 5-day returns as of a specific date
print(f"5-day returns as of 2022-06-15: {stock.n_day_ret(5, '2022-06-15')}")

# Get daily returns for a specific date
print(f"Daily returns on 2022-06-15: {stock.daily_ret('2022-06-15')}")

# Get an array of last 30 days prices before a specific date
print(f"Last 30 days prices until 2022-06-15: {stock.last_30_days_price('2022-06-15')}")
