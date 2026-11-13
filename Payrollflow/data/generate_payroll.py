import pandas as pd
import numpy as np
import random
 
# Reproducible random data
random.seed(42)
np.random.seed(42)
 
# Indian first names
first_names = [
    "Rahul", "Priya", "Amit", "Sneha", "Arjun",
    "Neha", "Rohit", "Ananya", "Karan", "Pooja",
    "Vikas", "Shreya", "Aditya", "Riya", "Manish",
    "Kavya", "Varun", "Simran", "Nikhil", "Isha",
    "Saurabh", "Meera", "Akash", "Divya", "Harsh",
    "Ankit", "Tanvi", "Mohit", "Aarav", "Nisha"
]
 
# Indian surnames
last_names = [
    "Sharma", "Verma", "Kumar", "Patel", "Singh",
    "Gupta", "Mehta", "Agarwal", "Malhotra", "Reddy",
    "Joshi", "Mishra", "Chopra", "Shah", "Yadav",
    "Kapoor", "Das", "Iyer", "Bansal", "Saxena"
]
 
# Departments and cities
departments = [
    "IT", "HR", "Finance", "Sales", "Operations"
]
 
cities = [
    "Pune", "Mumbai", "Delhi", "Noida", "Bangalore"
]
 
# Six payroll months
months = pd.date_range(
    start="2026-01-01",
    periods=6,
    freq="MS"
)
 
records = []
 
# Generate 1000 employees
for emp_id in range(1001, 2001):
 
    # Employee details (remain constant)
    name = random.choice(first_names) + " " + random.choice(last_names)
 
    department = random.choice(departments)
    city = random.choice(cities)
 
    joining_date = pd.Timestamp(
        random.randint(2020, 2025),
        random.randint(1, 12),
        random.randint(1, 28)
    )
 
    # Generate six monthly payroll records
    for month in months:
 
        basic_salary = random.randint(25000, 90000)
 
        hra = round(basic_salary * 0.40, 2)
 
        bonus = random.randint(1000, 10000)
 
        deductions = random.randint(1000, 5000)
 
        working_days = random.choice([20, 21, 22, 23])
 
        present_days = random.randint(
            working_days - 4,
            working_days
        )
 
        performance_rating = random.randint(1, 5)
 
        records.append({
            "EmployeeID": emp_id,
            "EmployeeName": name,
            "Department": department,
            "City": city,
            "JoiningDate": joining_date,
            "PayrollMonth": month,
            "BasicSalary": basic_salary,
            "HRA": hra,
            "Bonus": bonus,
            "Deductions": deductions,
            "WorkingDays": working_days,
            "PresentDays": present_days,
            "PerformanceRating": performance_rating
        })
 
# Convert records into DataFrame
df = pd.DataFrame(records)
 
# Export CSV
df.to_csv("employee_payroll.csv", index=False)
 
# Display results
print("Payroll dataset generated successfully!")
 
print("Total records:", df.shape[0])
 
print("Total employees:", df["EmployeeID"].nunique())
 
print("Total months:", df["PayrollMonth"].nunique())
 
print("\nFirst 10 records:")
print(df.head(10))
 
print("\nDataset shape:")
print(df.shape)
 