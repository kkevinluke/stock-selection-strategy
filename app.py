import datetime
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt
from main import Stock  # Importing Stock class from main.py
from investment_strategy import InvestmentStrategy
from benchmark_compare import BenchmarkStrategy
from evaluation_metrics import EvaluationMetrics
from data_handling import fetch_nifty50_historical_prices


# Define the calculate equity curve functions
def calculate_benchmark_equity(start_date, end_date):
    # Fetch historical prices for Nifty 50 using the provided function
    nifty_historical_prices = fetch_nifty50_historical_prices(start_date, end_date)

    if nifty_historical_prices is None or not nifty_historical_prices:
        return None  # Handle case where data retrieval fails or no data available

    # Extract closing prices from fetched historical data
    nifty_closing_prices = list(nifty_historical_prices.values())

    # Calculate equity curve for Nifty 50 based on closing prices
    benchmark_equity_curve = [100000]  # Assuming starting equity is 100,000
    for i in range(1, len(nifty_closing_prices)):
        daily_return = (nifty_closing_prices[i] / nifty_closing_prices[i - 1]) - 1
        daily_equity = benchmark_equity_curve[-1] * (1 + daily_return)
        benchmark_equity_curve.append(daily_equity)

    return benchmark_equity_curve


def calculate_sample_strategy_equity(selected_stocks, start_date, end_date):
    # Fetch historical prices for selected stocks
    selected_stocks_historical_prices = {}
    for stock_symbol in selected_stocks:
        stock_instance = Stock(stock_symbol)
        historical_prices = {}
        current_date = start_date
        while current_date <= end_date:
            price = stock_instance.cur_price(current_date)
            historical_prices[current_date] = price
            current_date += datetime.timedelta(days=1)
        selected_stocks_historical_prices[stock_symbol] = historical_prices

    # Calculate equity curve for the sample strategy based on selected stocks' historical prices
    sample_strategy_equity_curve = [100000]  # Assuming starting equity is 100,000 for the strategy
    for i in range(1, len(list(selected_stocks_historical_prices.values())[0])):
        daily_total_equity = 0
        for stock_symbol in selected_stocks:
            stock_price = selected_stocks_historical_prices[stock_symbol][
                list(selected_stocks_historical_prices[stock_symbol].keys())[i]]
            previous_stock_price = selected_stocks_historical_prices[stock_symbol][
                list(selected_stocks_historical_prices[stock_symbol].keys())[i - 1]]
            daily_return = (stock_price / previous_stock_price) - 1
            daily_equity = sample_strategy_equity_curve[-1] * (
                        1 + daily_return / len(selected_stocks))  # Distribute return equally among stocks
            daily_total_equity += daily_equity
        sample_strategy_equity_curve.append(daily_total_equity)

    return sample_strategy_equity_curve


def implement_sample_strategy(selected_stocks, start_date, end_date):
    # Implement the sample strategy based on positive returns for selected stocks
    positive_return_stocks = []
    for stock_symbol in selected_stocks:
        stock_instance = Stock(stock_symbol)
        stock_returns = stock_instance.n_day_ret((end_date - start_date).days, end_date)
        if stock_returns is not None and stock_returns > 0:
            positive_return_stocks.append(stock_symbol)

    # Calculate equity curve for the sample strategy based on selected stocks with positive returns
    strategy_equity = calculate_sample_strategy_equity(positive_return_stocks, start_date, end_date)
    return strategy_equity


# Title and description in the sidebar
st.sidebar.title('Performance Evaluation App')
st.sidebar.write('Evaluate performance of Nifty index, benchmark, and a sample strategy.')

# Date inputs for simulation
start_date = st.sidebar.date_input("Start Date", datetime(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2023, 12, 31))

# Input for the number of days for stock selection
days_for_stock_selection = st.sidebar.number_input("Days for Stock Selection", min_value=1, value=30)

# Input for initial equity
initial_equity = st.sidebar.number_input("Initial Equity", min_value=0, value=100000)

# Display the selected date range
st.write(f"Selected date range: {start_date} to {end_date}")

# Initialize instances of InvestmentStrategy, BenchmarkStrategy, and EvaluationMetrics
# Use your stock_list to initialize these instances
stock_list = ['RELIANCE', 'HCLTECH', 'TATAMOTORS', 'M&M', 'EICHERMOT', 'JSWSTEEL', 'BAJFINANCE',
              'APOLLOHOSP', 'WIPRO', 'ADANIENT']  # Your list of stock symbols
investment_strategy = InvestmentStrategy(stock_list)
benchmark_strategy = BenchmarkStrategy(stock_list)
evaluation_metrics = EvaluationMetrics(stock_list)

# Get selected stocks for the sample strategy based on input days_for_stock_selection
selected_stocks = investment_strategy.assess_monthly_performance(end_date)

# Display selected stocks
st.write("Selected Stocks for Sample Strategy:")
st.write(selected_stocks)

# Calculate performance metrics for Nifty, benchmark, and sample strategy
benchmark_performance = benchmark_strategy.compare_with_nifty50(start_date, end_date)
strategy_performance = evaluation_metrics.evaluate_strategy(selected_stocks, start_date, end_date)

# Display performance metrics
st.write("Performance Metrics:")
st.write("Benchmark Performance:", benchmark_performance)
st.write("Sample Strategy Performance:", strategy_performance)

# Visualize equity curves in a single plot
# Implement code here to plot equity curves using matplotlib
# Generate equity curves data for Nifty, benchmark, and sample strategy
stock_instance = Stock('NIFTY50')
benchmark_equity_curve = calculate_benchmark_equity(start_date, end_date)
sample_strategy_equity_curve = implement_sample_strategy(selected_stocks, start_date, end_date)

# Plotting equity curves
st.write("Equity Curves:")
plt.figure(figsize=(10, 6))

# Plotting benchmark equity curve
plt.plot(benchmark_equity_curve, label='Benchmark')

# Plotting sample strategy equity curve
plt.plot(sample_strategy_equity_curve, label='Sample Strategy')

# Customize plot
plt.xlabel('Time')
plt.ylabel('Equity')
plt.title('Equity Curves')
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)
