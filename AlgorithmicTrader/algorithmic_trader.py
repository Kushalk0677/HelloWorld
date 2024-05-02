import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import yfinance as yf

# Function to collect historical stock price data
def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Function to preprocess and prepare data for modeling
def prepare_data(stock_data):
    # Calculate daily returns
    stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()

    # Create lag features
    for i in range(1, 6):
        stock_data[f'Lag {i}'] = stock_data['Daily Return'].shift(i)

    # Drop missing values
    stock_data.dropna(inplace=True)

    return stock_data

# Function to train and evaluate the model
def train_model(X_train, y_train, X_test, y_test):
    # Initialize linear regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Evaluate the model
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

    return model, train_rmse, test_rmse

# Main function
def main(selected_stock):
    # Define parameters
    start_date = '2020-01-01'  # Start date for data collection
    end_date = '2022-01-01'  # End date for data collection

    # Get historical stock data for the selected stock
    stock_data = get_stock_data(selected_stock, start_date, end_date)

    # Prepare data for modeling
    prepared_data = prepare_data(stock_data)

    # Split data into features (X) and target variable (y)
    X = prepared_data[['Lag 1', 'Lag 2', 'Lag 3', 'Lag 4', 'Lag 5']]
    y = prepared_data['Daily Return']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate the model
    model, train_rmse, test_rmse = train_model(X_train, y_train, X_test, y_test)

    # Make predictions for the next day
    last_day_features = X.iloc[-1:].values.reshape(1, -1)
    next_day_prediction = model.predict(last_day_features)
    return f"Model training RMSE: {train_rmse}\nModel testing RMSE: {test_rmse}\nPredicted daily return for the next day: {next_day_prediction[0]}"

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
