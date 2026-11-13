import pandas as pd
import numpy as np

#Q1
df = pd.read_csv("employee_payroll_dirty.csv")

print(f"Display first 10 records")
print(pd.head(10))

print(f"Display last 10 records")
print(pd.tail(10))

#Q2
print("Dataset shape: ",df.shape)
print("Column names: ")
print(df.columns)

#Q3
print("Descriptive statistics: ")
print(df.describe())

#Q4
print("Missing value in each column: ")
print(df.isnull().sum())

#Q5
df = df.drop_duplicates(
    subset = ["EmployeeID","PayrollMonth"],
)

print("Shape after removing duplicates: ",df.shape)

#Q6
df["BasicSalary"] = df["BasicSalary"].fillna(df["BasicSalary"].median())
df["Bonus"] = df["Bonus"].fillna(df["Bonus"].median())

print("Missing salary values: ",df["BasicSalary"].isnull().sum())
print("Missing bonus values: ",df["Bonus"].isnull.sum())

# 7
df["Department"] = df["Department"].str.strip().str.upper()
df["Department"] = df["Department"].replace({"INFORMATION TECHNOLOGY": "IT"})
df["City"] = df["City"].str.strip().str.title()
 
# 8
df["JoiningDate"] = pd.to_datetime(df["JoiningDate"])
df["PayrollMonth"] = pd.to_datetime(df["PayrollMonth"])
 
# 9
high_salary = df[df["BasicSalary"] > 75000]
print(high_salary)
 
# 10
df = df.sort_values(by="BasicSalary", ascending=False)
 
# 11
df["GrossSalary"] = df["BasicSalary"] + df["HRA"] + df["Bonus"]
 
# 12
df["NetSalary"] = df["GrossSalary"] - df["Deductions"]
 
# 13
df["AttendancePercentage"] = (df["PresentDays"] / df["WorkingDays"]) * 100
 
# 14 using numpy select
conditions = [
    df["BasicSalary"] <= 40000,
    df["BasicSalary"] <= 70000
]
categories = ["Low", "Medium"]
df["SalaryCategory"] = np.select(conditions, categories, default="High")
 
# 15
department_groups = df.groupby("Department")
print(department_groups.size())
 
# 16
department_avg_salary = df.groupby("Department")["BasicSalary"].mean()
print(department_avg_salary)
 
# 17
top_10 = df.nlargest(10, "BasicSalary")    #it selects the top 10 rows with the largest values in the "BasicSalary" column
print(top_10)
 
# 18 department wise payroll pivot table
payroll_pivot = pd.pivot_table(
    df,
    index="Department",
    columns="PayrollMonth",
    values="NetSalary",
    aggfunc="sum",
    fill_value=0
)
print(payroll_pivot)
 
# 19 validate salary, attendance and employee ids
invalid_data = (
    (df["BasicSalary"] < 0) |
    (df["WorkingDays"] <= 0) |
    (df["PresentDays"] < 0) |
    (df["PresentDays"] > df["WorkingDays"]) |
    (df["EmployeeID"].isnull()) |
    (df["EmployeeID"] <= 0)
)
 
rejected_rows = df[invalid_data].copy()
df = df[~invalid_data].copy()   # ~ means NOT
 
# 20 export cleaned and rejected records
rejected_rows.to_csv("rejected_payroll_records.csv", index=False)
df.to_csv("employee_payroll_cleaned.csv", index=False)
 
print("Cleaned dataset exported successfully!")
 