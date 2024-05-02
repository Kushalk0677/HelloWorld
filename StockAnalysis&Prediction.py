import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data


def predict_stock_prices(stock_data):
    # Feature engineering
    stock_data['Date'] = stock_data.index
    stock_data['Year'] = stock_data['Date'].dt.year
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data['DayOfWeek'] = stock_data['Date'].dt.dayofweek

    # Split data into features and target variable
    X = stock_data[['Year', 'Month', 'Day', 'DayOfWeek']].values
    y = stock_data['Close'].values

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Evaluate model
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    print("Mean Squared Error (Train):", mse_train)
    print("Mean Squared Error (Test):", mse_test)

    # Plot predictions vs actual values
    plt.figure(figsize=(10, 6))
    plt.plot(y_test, label='Actual')
    plt.plot(y_pred_test, label='Predicted')
    plt.title('Vodafone Idea Stock Price Prediction')
    plt.xlabel('Days')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    symbol = "IDEA.NS"
    start_date = "2010-01-01"
    end_date = "2024-01-01"

    # Fetch data
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    # Predict stock prices
    predict_stock_prices(stock_data)

