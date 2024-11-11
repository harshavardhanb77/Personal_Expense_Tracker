# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset from CSV file
df = pd.read_csv("enhanced_personal_expense_data.csv")

# Check for duplicates in the dataset and remove them if any
df.drop_duplicates(inplace=True)

# Check for any missing values in each column and display the count per column
missing_values = df.isnull().sum()
print("Missing values per column:\n", missing_values)

# Convert the "Date" column to a datetime object for easier date manipulation
df["Date"] = pd.to_datetime(df["Date"])

# Display data types of all columns to verify proper types
print("\nData Types:\n", df.dtypes)

# Display summary statistics of numerical columns (like 'Amount') for a general overview
print("\nSummary Statistics:\n", df.describe())

# Visualize the distribution of transactions by category using a count plot
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x="Category", order=df["Category"].value_counts().index)
plt.title("Distribution of Transactions by Category")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Analyze the monthly spending pattern by creating a "Month" column from the "Date"
df["Month"] = df["Date"].dt.to_period("M")
# Group data by month and calculate total spending per month
monthly_spending = df.groupby("Month")["Amount"].sum()
# Plot the monthly spending trend over time
monthly_spending.plot(kind="line", marker="o", figsize=(12, 6))
plt.title("Monthly Spending Pattern")
plt.xlabel("Month")
plt.ylabel("Total Amount")
plt.show()

# Analyze spending patterns by day of the week
df["Day of Week"] = df["Date"].dt.day_name()  # Extract day of the week from date
# Group data by day of the week and calculate total spending, ordering days in week order
day_of_week_spending = df.groupby("Day of Week")["Amount"].sum().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)
# Plot total spending by each day of the week
day_of_week_spending.plot(kind="bar", figsize=(10, 6))
plt.title("Spending by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Total Amount")
plt.show()

# Visualize the count of transactions by payment method using a count plot
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x="Payment Method", order=df["Payment Method"].value_counts().index)
plt.title("Transactions by Payment Method")
plt.xticks(rotation=45)
plt.show()

# Analyze transactions by location
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x="Location", order=df["Location"].value_counts().index)
plt.title("Transactions by Location")
plt.xticks(rotation=45)
plt.show()

# Compare spending amount distributions across categories using a box plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Category", y="Amount")
plt.title("Spending Amount Distribution by Category")
plt.xticks(rotation=45)
plt.show()

# Identify the top 10 merchants by total spending
top_merchants = df.groupby("Merchant")["Amount"].sum().nlargest(10)
# Plot total spending for top 10 merchants
top_merchants.plot(kind="bar", figsize=(10, 6))
plt.title("Top 10 Merchants by Spending")
plt.xlabel("Merchant")
plt.ylabel("Total Amount")
plt.show()
