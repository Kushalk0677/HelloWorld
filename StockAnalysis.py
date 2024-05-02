#https://www.datacamp.com/blog/60-python-projects-for-all-levels-expertise
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data


def analyze_data(stock_data):
    # Basic statistics
    print("Basic Statistics:")
    print(stock_data.describe())

    # Correlation analysis
    print("\nCorrelation Analysis:")
    correlation_matrix = stock_data.corr()
    print(correlation_matrix)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Close'], label='Close Price')
    plt.title('Vodafone Idea Stock Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.legend()

    plt.subplot(2, 1, 2)
    sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu")
    plt.title('Correlation Heatmap')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    symbol = "IDEA.NS"
    start_date = "2010-01-01"
    end_date = "2024-01-01"

    # Fetch data
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    # Analyze data
    analyze_data(stock_data)
