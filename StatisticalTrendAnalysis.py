# Summary statistics for overall spending
summary_stats = df["Amount"].describe()
quartiles = df["Amount"].quantile([0.25, 0.5, 0.75])

# Analyze monthly trend
monthly_trend = monthly_expenses.set_index("Month")
monthly_trend["Rolling_Avg"] = monthly_trend["Amount"].rolling(window=3).mean()
monthly_trend["Rolling_Median"] = monthly_trend["Amount"].rolling(window=3).median()

# Calculate spending volatility (standard deviation) for each month
monthly_trend["Volatility"] = df.groupby("Month")["Amount"].std().values

# Month-over-Month Change
monthly_trend["MoM_Change"] = monthly_trend["Amount"].pct_change().fillna(0) * 100

# Display enhanced summary statistics and monthly trend analysis
print("Summary Statistics:\n", summary_stats)
print("\nQuartile Analysis:\n", quartiles)
print("\nMonthly Trend Analysis with Rolling Average, Median, Volatility, and MoM Change:\n", monthly_trend.head())