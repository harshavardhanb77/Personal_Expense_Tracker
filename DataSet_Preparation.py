# Import necessary libraries
import pandas as pd
import numpy as np
import datetime

# Set random seed for reproducibility
np.random.seed(0)

# Define various categories of data for transaction simulation
categories = ["Groceries", "Entertainment", "Bills", "Transport", "Eating Out", "Healthcare"]
payment_methods = ["Cash", "Credit Card", "Debit Card", "Bank Transfer"]
locations = ["Supermarket", "Mall", "Online", "Restaurant", "Pharmacy", "Fuel Station"]
merchants = ["Walmart", "Amazon", "Starbucks", "Netflix", "Shell", "CVS"]

# Generate a range of dates from 2022-01-01 to 2024-11-01, with daily frequency
dates = pd.date_range(start="2022-01-01", end="2024-11-01", freq="D")

# Create a dictionary to hold generated data for each transaction
data = {
    # Generate unique transaction IDs for each row
    "Transaction ID": range(1, 1001),
    
    # Randomly select a date from the generated date range for each transaction
    "Date": np.random.choice(dates, 1000),
    
    # Generate random transaction amounts between $5 and $200, rounded to two decimal places
    "Amount": np.random.uniform(5, 200, 1000).round(2),
    
    # Randomly assign a category from the predefined list
    "Category": np.random.choice(categories, 1000),
    
    # Randomly assign a payment method from the predefined list
    "Payment Method": np.random.choice(payment_methods, 1000),
    
    # Randomly assign a location from the predefined list
    "Location": np.random.choice(locations, 1000),
    
    # Randomly assign a merchant from the predefined list
    "Merchant": np.random.choice(merchants, 1000),
    
    # Randomly assign a description for each transaction
    "Description": np.random.choice(
        [
            "Weekly groceries",
            "Dinner with friends",
            "Monthly subscription",
            "Bus fare",
            "Doctor's visit",
            "Gas refill",
            "Movie night",
            "Gift shopping",
        ],
        1000,
    ),
}

# Create a DataFrame from the generated data
df = pd.DataFrame(data)

# Add a new column for transaction type based on the category
# Transactions in "Bills" and "Healthcare" are categorized as "Fixed"; others as "Variable"
df["Transaction Type"] = df["Category"].apply(
    lambda x: "Fixed" if x in ["Bills", "Healthcare"] else "Variable"
)

# Add a column for the day of the week based on the transaction date
df["Day of Week"] = df["Date"].dt.day_name()

# Save the generated dataset to a CSV file
df.to_csv("enhanced_personal_expense_data.csv", index=False)

# Display the first few rows of the DataFrame to verify
df.head()
