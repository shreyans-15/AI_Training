import pandas as pd
import numpy as np
 
# Read the original clean CSV file
df = pd.read_csv("employee_payroll.csv")
 
# 1. Introduce missing values
df.loc[[10, 25, 100], "Bonus"] = np.nan
df.loc[[50, 150], "BasicSalary"] = np.nan
df.loc[[200, 300], "City"] = np.nan
 
# 2. Introduce duplicate employee-month records
duplicates = df.iloc[[5, 20, 60, 110]].copy()
df = pd.concat([df, duplicates], ignore_index=True)
 
# 3. Introduce invalid salary values
df.loc[[400, 500, 600], "BasicSalary"] = -5000
 
# 4. Introduce inconsistent department names
df.loc[[700, 701], "Department"] = "it"
df.loc[[702, 703], "Department"] = "Information Technology"
df.loc[[704, 705], "Department"] = "hr"
 
# Save the dirty dataset
df.to_csv("employee_payroll_dirty.csv", index=False)
 
# Display dataset information
print("Dirty dataset created successfully!")
 
print("\nDataset shape:")
print(df.shape)
 
print("\nMissing values:")
print(df.isnull().sum())
 
print("\nDuplicate employee-month records:")
print(df.duplicated(subset=["EmployeeID", "PayrollMonth"]).sum())
 
print("\nDepartment values:")
print(df["Department"].value_counts())
 
print("\nInvalid salary records:")
print(df[df["BasicSalary"] < 0])
 