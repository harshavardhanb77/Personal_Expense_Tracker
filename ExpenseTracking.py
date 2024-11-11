# Calculate daily total expenses by summing "Amount" for each unique "Date"
daily_expenses = df.groupby("Date")["Amount"].sum().reset_index()

# Calculate monthly total expenses
# Convert "Date" to a monthly period to group by month
df["Month"] = df["Date"].dt.to_period("M")
monthly_expenses = df.groupby("Month")["Amount"].sum().reset_index()

# Calculate weekly total expenses
# Convert "Date" to a weekly period to group by week
df["Week"] = df["Date"].dt.to_period("W")
weekly_expenses = df.groupby("Week")["Amount"].sum().reset_index()

# Calculate total expenses for each category
# Group by "Category" and sum up the "Amount" for each category
category_expenses = df.groupby("Category")["Amount"].sum().reset_index()

# Calculate monthly expenses for each category
# Group by both "Month" and "Category" and sum "Amount" for each combination
# Use unstack() to create a separate column for each category, fill missing values with 0
monthly_category_expenses = df.groupby(["Month", "Category"])["Amount"].sum().unstack().fillna(0).reset_index()

# Yearly summary of expenses
# Calculate the total expenses by summing "Amount" for all transactions
total_expenses = df["Amount"].sum()

# Calculate the total number of days in the dataset
total_days = (df["Date"].max() - df["Date"].min()).days + 1

# Calculate the average daily expenses by dividing total expenses by total days
average_daily_expenses = total_expenses / total_days

# Create a DataFrame for the yearly summary with total and average daily expenses
yearly_summary = pd.DataFrame({
    "Total Expenses": [total_expenses],
    "Average Daily Expenses": [average_daily_expenses]
})

# Calculate breakdown of expenses by category and payment method
# Group by both "Category" and "Payment Method" and sum "Amount" for each combination
# Use unstack() to create a column for each payment method, filling missing values with 0
category_payment_expenses = df.groupby(["Category", "Payment Method"])["Amount"].sum().unstack().fillna(0).reset_index()

# Calculate average spending by day of the week
# Extract day names from "Date" and use them to group by day
df["Day of Week"] = df["Date"].dt.day_name()

# Group by "Day of Week" and calculate the average "Amount" spent on each day
# Reindex to maintain a specific order for days of the week
day_of_week_avg_expenses = df.groupby("Day of Week")["Amount"].mean().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
).reset_index()

# Display each summary table for verification
print("Daily Expenses:\n", daily_expenses.head())
print("\nMonthly Expenses:\n", monthly_expenses.head())
print("\nWeekly Expenses:\n", weekly_expenses.head())
print("\nExpenses per Category:\n", category_expenses)
print("\nMonthly Expenses per Category:\n", monthly_category_expenses.head())
print("\nYearly Summary:\n", yearly_summary)
print("\nCategory Breakdown per Payment Method:\n", category_payment_expenses)
print("\nAverage Expenses by Day of the Week:\n", day_of_week_avg_expenses)
