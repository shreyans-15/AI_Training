import numpy as np
import pandas as pd

df = pd.read_csv("HSBC_Synthetic_Banking_Customers.csv")

balances = np.array(df["Account_Balance"])

print(balances)

print("Dimensions: ",balances.ndim)
print("Shape: ",balances.shape)
print("Size: ",balances.size)
print("Data_type: ",balances.dtype)

print("Minimum balance: ",np.min(balances))
print("Maximum balance: ",np.max(balances))

print("Mean balance: ",np.mean(balances))
print("Balance sum:", np.sum(balances))
print("Median balance:", np.median(balances))
print("Standard Deviation:", np.std(balances))

print("25th percentile: ",np.percentile(balances, 25))
print("50th percentile: ",np.percentile(balances, 50))
print("75th percentile: ",np.percentile(balances, 75))

high_balances=[]

for balance in balances:
    if balance > 500000:
       high_balances.append(balance)

print("balances above INR 500000: ", high_balances)

#redit_scores = np.array(df["Credit_Score"])

credit_scores = np.array(df["Credit_Score"])

low_scores = credit_scores[credit_scores < 650]

print("Credit Scores below 650:")
print(low_scores)

ascending_balances = np.sort(balances)

print("Balances in Ascending Order:")
print(ascending_balances)

descending_balances = np.sort(balances)[::-1]

print("Balances in Descending Order:")
print(descending_balances)

total_deposits = np.sum(df["Monthly_Deposit"])
total_withdrawals = np.sum(df["Monthly_Withdrawal"])

print("Total Monthly Deposits: ",total_deposits)
print("Total Monthly Withdrawals: ", total_withdrawals)

increased_balances = balances * 1.05

print("Balances after 5 percent increase: ")
print(increased_balances)

# Q11
balance_category = np.where(balances > 500000, "High", "Low")
print(balance_category)

# Q12
conditions = [
    balances < 100000,
    (balances >= 100000) & (balances <= 500000),
    balances > 500000
]

choices = ["Low", "Medium", "High"]

categories = np.select(
    conditions,
    choices,
    default="Unknown"
)
print(categories)

# Q13
income = np.array(df["Monthly_Income"])

deposit_income_ratio = np.where(
    income != 0,
    df["Monthly_Deposit"] / income,
    0
)

print(deposit_income_ratio)

# Q14
high_withdrawal = df[df["Monthly_Withdrawal"] > df["Monthly_Deposit"]]
print(high_withdrawal)

# Q15
scores, counts = np.unique(df["Credit_Score"], return_counts=True)

for score, count in zip(scores, counts):
    print(score, count)

# Q16
top5_indices = np.argsort(balances)[-5:]
print(top5_indices)
print(balances[top5_indices])

# Q17
min_bal = np.min(balances)
max_bal = np.max(balances)

if max_bal == min_bal:
    normalized = np.zeros_like(balances, dtype=float)
else:
    normalized = (balances - min_bal) / (max_bal - min_bal)

print(normalized)

# Q18
mean_bal = np.mean(balances)
std_bal = np.std(balances)

if std_bal == 0:
    z_scores = np.zeros_like(balances, dtype=float)
else:
    z_scores = (balances - mean_bal) / std_bal

print(z_scores)

# Q19
financial_matrix = np.column_stack((
    df["Account_Balance"],
    df["Monthly_Deposit"],
    df["Monthly_Withdrawal"]
))

print(financial_matrix)

print("Column Totals:")
print(np.sum(financial_matrix, axis=0))

print("Row Totals:")
print(np.sum(financial_matrix, axis=1))

# Q20
correlation = np.corrcoef(
    df["Monthly_Income"],
    df["Account_Balance"]
)[0,1]

print("Pearson Correlation:", correlation)

# ---------------- PANDAS ----------------


# Q22
print(df.head(10))
print(df.tail(10))

# Q23
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())

# Q24
print(df.describe())

# Q25
print(df.isnull().sum())

print("Duplicate Customer IDs:")
print(df["Customer_ID"].duplicated().sum())

# Q26
print(df[
    ["Customer_Name",
     "City",
     "Account_Balance",
     "Credit_Score"]
])

# Q27
customers_25_40 = df[
    (df["Age"] >= 25) &
    (df["Age"] <= 40)
]

print(customers_25_40)

# Q28
active_savings = df[
    (df["Account_Type"] == "Savings") &
    (df["Account_Status"] == "Active")
]

print(active_savings)

# Q29
sorted_df = df.sort_values(
    by=["Account_Balance", "Monthly_Income"],
    ascending=False
)

print(sorted_df)

# Q30
df["Net_Monthly_Flow"] = (
    df["Monthly_Deposit"] -
    df["Monthly_Withdrawal"]
)

print(df[[
    "Customer_Name",
    "Net_Monthly_Flow"
]])

# Q31
city_balance = df.groupby("City")["Account_Balance"].sum()

print(city_balance)

# Q32
avg_income = df.groupby(
    "Account_Type"
)["Monthly_Income"].mean()

print(avg_income)

# Q33
branch_summary = df.groupby("Branch")[
    ["Monthly_Deposit",
     "Monthly_Withdrawal"]
].sum()

print(branch_summary)

# Q34
balance_stats = df.groupby("Branch")[
    "Account_Balance"
].agg(
    ["min", "max", "mean", "median"]
)

print(balance_stats)

# Q35
pivot = pd.pivot_table(
    df,
    values="Account_Balance",
    index="City",
    columns="Account_Type",
    aggfunc="sum"
)

print(pivot)

# Q36
bins = [18, 25, 40, 60, 100]
labels = ["18-25", "26-40", "41-60", "61+"]

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

print(df[["Age", "Age_Group"]])

# Q37
branch_avg = df.groupby("Branch")[
    "Account_Balance"
].transform("mean")

df["Balance_minus_Branch_Avg"] = (
    df["Account_Balance"] -
    branch_avg
)

print(df[
    ["Customer_Name",
     "Balance_minus_Branch_Avg"]
])

# Q38
branch_details = pd.DataFrame({
    "Branch": [
        "Mumbai",
        "Delhi",
        "Pune",
        "Chennai",
        "Hyderabad",
        "Bengaluru"
    ],
    "Region": [
        "West",
        "North",
        "West",
        "South",
        "South",
        "South"
    ]
})

merged_df = pd.merge(
    df,
    branch_details,
    on="Branch",
    how="left",
    validate="many_to_one"
)

print(merged_df.head())

# Q39
top3_city = (
    df.sort_values(
        "Account_Balance",
        ascending=False
    )
    .groupby("City")
    .head(3)
)

print(top3_city[
    ["City",
     "Customer_Name",
     "Account_Balance"]
])

# Q40

status_counts = (
    df.groupby(["Branch", "Account_Status"])
      .size()
      .unstack(fill_value=0)
)

summary = df.groupby("Branch").agg({
    "Account_Balance": "sum",
    "Credit_Score": "mean",
    "Net_Monthly_Flow": "sum"
})

summary = summary.join(status_counts)

print(summary)

