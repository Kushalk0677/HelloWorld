import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import ta
import datetime
import requests
from bs4 import BeautifulSoup


def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data


def preprocess_data(stock_data):
    # Feature engineering
    stock_data['Date'] = stock_data.index
    stock_data['Year'] = stock_data['Date'].dt.year
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data['DayOfWeek'] = stock_data['Date'].dt.dayofweek

    # Technical Indicators
    stock_data = ta.add_all_ta_features(stock_data, open="Open", high="High", low="Low", close="Close", volume="Volume")

    # Sentiment Analysis (Mock Implementation)
    stock_data['Sentiment'] = np.random.uniform(-1, 1, size=len(stock_data))

    # Drop unnecessary columns
    stock_data.drop(['Date'], axis=1, inplace=True)

    return stock_data


def evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    print("Mean Squared Error (Train):", mse_train)
    print("Mean Squared Error (Test):", mse_test)
    return y_pred_train, y_pred_test


def plot_predictions(y_true, y_pred, title):
    plt.figure(figsize=(12, 8))  # Increase figure size
    plt.plot(y_true, label='Actual', color='blue', linestyle='-')
    plt.plot(y_pred, label='Predicted', color='red', linestyle='--')
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Price (INR)')
    plt.grid(True)  # Add gridlines
    plt.legend(loc='upper left')  # Customize legend location
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    plt.show()  # Display the plot interactively


def fetch_news_sentiment(stock_symbol):
    url = f"https://news.google.com/rss/search?q={stock_symbol}+stock&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    sentiments = []
    for item in items:
        title = item.title.text
        description = item.description.text
        sentiment_score = np.random.uniform(-1, 1)
        sentiments.append((title, description, sentiment_score))
    return sentiments


def main():
    # Fetch historical stock data
    symbol = "IDEA.NS"
    start_date = "2010-01-01"
    end_date = "2024-01-01"
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    # Preprocess data
    stock_data = preprocess_data(stock_data)

    # Split data into features and target variable
    X = stock_data.drop(['Close'], axis=1)
    y = stock_data['Close']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define a pipeline for data preprocessing
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean'))
    ])

    # Fit and transform training data
    X_train_preprocessed = pipeline.fit_transform(X_train)

    # Transform testing data
    X_test_preprocessed = pipeline.transform(X_test)

    # Model 1: Linear Regression
    print("Linear Regression:")
    lr = LinearRegression()
    y_pred_train_lr, y_pred_test_lr = evaluate_model(lr, X_train_preprocessed, X_test_preprocessed, y_train, y_test)
    plot_predictions(y_test, y_pred_test_lr, "Linear Regression Prediction")

    # Model 2: Random Forest
    print("Random Forest:")
    rf = RandomForestRegressor(random_state=42)
    y_pred_train_rf, y_pred_test_rf = evaluate_model(rf, X_train_preprocessed, X_test_preprocessed, y_train, y_test)
    plot_predictions(y_test, y_pred_test_rf, "Random Forest Prediction")

    # Feature Importance Analysis (Random Forest)
    print("Feature Importance (Random Forest):")
    feature_importances = pd.Series(rf.feature_importances_, index=X.columns)
    feature_importances.nlargest(10).plot(kind='barh')
    plt.title('Feature Importance (Random Forest)')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.show()

    # News Sentiment Analysis
    print("\nNews Sentiment Analysis:")
    news_sentiment = fetch_news_sentiment(symbol)
    for title, description, sentiment_score in news_sentiment[:5]:
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Sentiment Score: {sentiment_score}\n")


if __name__ == "__main__":
    main()
