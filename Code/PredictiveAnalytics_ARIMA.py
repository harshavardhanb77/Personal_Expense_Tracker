# Import necessary libraries
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load the dataset from the specified file path
file_path = '/content/enhanced_personal_expense_data.csv'
df = pd.read_csv(file_path)

# Convert the "Date" column to datetime format for easier time-based manipulation
df['Date'] = pd.to_datetime(df['Date'])

# Set "Date" column as the index of the DataFrame to facilitate resampling by date
df.set_index('Date', inplace=True)

# Resample the data to a monthly frequency, summing the "Amount" for each month
monthly_data = df['Amount'].resample('M').sum()

# Plot the monthly aggregated data to visualize the spending trend over time
plt.figure(figsize=(10, 5))
plt.plot(monthly_data, marker='o')
plt.title('Monthly Aggregated Amount')
plt.xlabel('Date')
plt.ylabel('Total Amount')
plt.show()

# Fit an ARIMA model to the monthly data
# Start with a simple ARIMA(1, 1, 1) model, where:
#   - p = 1 (AR term),
#   - d = 1 (differencing to make the series stationary),
#   - q = 1 (MA term)
model = ARIMA(monthly_data, order=(1, 1, 1))
arima_model = model.fit()

# Forecast the next 12 months of spending using the fitted ARIMA model
forecast = arima_model.forecast(steps=12)

# Plot both the historical monthly data and the forecasted values for comparison
plt.figure(figsize=(10, 5))
plt.plot(monthly_data, label='Historical Data')  # Plot historical data
plt.plot(forecast, label='Forecast', color='orange')  # Plot forecasted data
plt.title('ARIMA Forecast for Monthly Spending')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.show()

# Print a summary of the ARIMA model to see model parameters and performance metrics
print(arima_model.summary())
