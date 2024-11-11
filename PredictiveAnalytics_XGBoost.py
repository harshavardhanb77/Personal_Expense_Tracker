# Import necessary libraries
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the dataset from the specified file path
file_path = '/content/enhanced_personal_expense_data.csv'
df = pd.read_csv(file_path)

# Convert the "Date" column to datetime format for easier date-based manipulation
df['Date'] = pd.to_datetime(df['Date'])

# Set "Date" as the index and resample data by month, summing up "Amount" for each month
df.set_index('Date', inplace=True)
monthly_data = df['Amount'].resample('M').sum()

# Define a function to create lagged features for supervised learning
# This helps transform the time series data into a format suitable for regression modeling
def create_lagged_features(data, lag=12):
    df_lagged = pd.DataFrame(data)
    # Create lagged features up to the specified number of months
    for i in range(1, lag + 1):
        df_lagged[f'lag_{i}'] = df_lagged['Amount'].shift(i)
    df_lagged = df_lagged.dropna()  # Drop rows with NaN values introduced by lagging
    return df_lagged

# Prepare the dataset with 12 lags (monthly lags up to 12 months in the past)
lagged_data = create_lagged_features(monthly_data)

# Separate the dataset into features (X) and target (y) variables
X = lagged_data.drop('Amount', axis=1)  # Features: lagged values
y = lagged_data['Amount']  # Target: current month amount

# Split data into training and testing sets (80% train, 20% test), preserving order with shuffle=False
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Initialize the XGBoost model with specified parameters
# Objective is set to 'reg:squarederror' for regression; other parameters adjust model complexity
xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=3, learning_rate=0.1)
# Fit the model on the training data
xgb_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = xgb_model.predict(X_test)

# Calculate the root mean squared error (RMSE) to evaluate model accuracy
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squared Error: {rmse}")

# Plot the actual vs. predicted values for the test set to assess forecast accuracy
plt.figure(figsize=(10, 5))
plt.plot(monthly_data.index[-len(y_test):], y_test, label='Actual', marker='o')
plt.plot(monthly_data.index[-len(y_test):], y_pred, label='Predicted', marker='x')
plt.title('XGBoost Forecast vs Actual for Monthly Spending')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.show()

# Forecast for the next 12 months
# Start by preparing the latest observed values as input for forecasting
last_values = X.iloc[-1:].values  # Get the last set of lagged features

forecast = []  # Initialize list to store forecasted values
for i in range(12):  # Loop to forecast for the next 12 months
    # Predict the next month's amount based on current lagged values
    next_pred = xgb_model.predict(last_values)
    forecast.append(next_pred[0])  # Append the prediction to the forecast list
    
    # Update last_values for the next iteration by shifting it (rolling window approach)
    last_values = np.roll(last_values, -1)  # Shift values left
    last_values[0, -1] = next_pred  # Replace the last position with the latest prediction

# Generate a date range for the forecast period (12 months ahead)
forecast_dates = pd.date_range(monthly_data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')

# Plot forecasted values alongside historical data for comparison
plt.figure(figsize=(10, 5))
plt.plot(monthly_data, label='Historical Data')  # Plot historical monthly spending
plt.plot(forecast_dates, forecast, label='XGBoost Forecast', color='purple')  # Plot 12-month forecast
plt.title('XGBoost Forecast for Next 12 Months')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.show()
