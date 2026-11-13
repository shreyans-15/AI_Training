from pathlib import Path #helps us work with files and folder path
import pandas as pd
import numpy as np
import logging            # used to record etl progress, warnings and errors
import matplotlib.pyplot as plt

BASE_DIR  = Path(__file__).resolve().parent

DATA_DIR  = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
DATABASE_DIR = BASE_DIR / "database"
LOG_DIR = BASE_DIR / "logs"

# create required folders
def create_folder() -> None:
    """Create report and database folders if they do not exist."""
 
    REPORT_DIR.mkdir(exist_ok=True)
    DATABASE_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

# extract
def extract_data():
    """Read Data from csv files."""
 
    df = pd.read_csv(DATA_DIR/"employee_payroll_dirty.csv")
    print("Payroll data shape: ",df.shape)
    return df

#inspection
def inspect_data(df):
    """Inspect the structure and quality of payroll data."""
 
    print("\nfirst 10 rows:")
    print(df.head(10))
 
    print("\nlast 10 rows:")
    print(df.tail(10))
 
    print("\ndataset Shape:")
    print(df.shape)
 
    print("\ndataset Size:")
    print(df.size)
 
    print("\ncolumn Names:")
    print(df.columns)
 
    print("\ncolumn data types:")
    print(df.dtypes)
 
    print("\ndescriptive summary:")
    print(df.describe())
 
    # missing values in each column
    print("\nmissing values:")
    print(df.isnull().sum())
 
    # count duplicate rows in  all columns
    print("\nduplicate rows:")
    print(df.duplicated().sum())


#cleaning
def clean_payroll(df):
    """Clean and standardize the employee payroll dataset."""
 
    df = df.copy()
 
    # remove duplicate records based on EmployeeID and PayrollMonth
    df = df.drop_duplicates(
        subset=["EmployeeID", "PayrollMonth"],
        keep="first"
    )
 
 
    # Convert BasicSalary column into numeric format
    df["BasicSalary"] = pd.to_numeric(df["BasicSalary"], errors="coerce")
 
    # convert bonus column into numeric format
    df["Bonus"] = pd.to_numeric(df["Bonus"], errors="coerce") #coerce converts invalid value-> NaN
 
    # Calculate the median of the BasicSalary column
    basic_salary_median = df["BasicSalary"].median()
 
    # replace missing BasicSalary values with the column median
    df["BasicSalary"] = df["BasicSalary"].fillna(basic_salary_median)
 
    # calculate the median of the Bonus column
    bonus_median = df["Bonus"].median()
 
    df["Bonus"] = df["Bonus"].fillna(bonus_median)
 
    df["City"] = df["City"].fillna("Unknown")
 
    # remove unwanted spaces and standardize department capitalization
    df["Department"] = df["Department"].astype("string").str.strip().str.title()
 
    # replace inconsistent department names with standard names
    df["Department"] = df["Department"].replace({
        "It": "IT",
        "Information Technology": "IT",
        "Hr": "HR"
    })
 
    # remove unwanted spaces and standardize city names
    df["City"] = df["City"].astype("string").str.strip().str.title()
 
    # convert JoiningDate into Pandas datetime format
    df["JoiningDate"] = pd.to_datetime(
        df["JoiningDate"],
        errors="coerce"
    )
 
    df["PayrollMonth"] = pd.to_datetime(
        df["PayrollMonth"],
        errors="coerce"
    )
 
    # identify records with negative or missing salary values
    invalid_salary = df["BasicSalary"].isna() | (df["BasicSalary"] < 0)
 
    # identify records with invalid attendance values
    invalid_attendance = (
        df["WorkingDays"].isna()
        | df["PresentDays"].isna()
        | (df["WorkingDays"] <= 0)
        | (df["PresentDays"] < 0)
        | (df["PresentDays"] > df["WorkingDays"])
    )
 
    # separate records that contain invalid salary or attendance
    rejected_df = df[invalid_salary | invalid_attendance].copy() # if true select the rows
 
    # keep only valid payroll records
    df = df[~(invalid_salary | invalid_attendance)].copy()
 
    # display the number of rejected records
    print("\nrejected payroll records:")
    print(rejected_df.shape[0])
 
    # display the shape of the cleaned DataFrame
    print("\ncleaned payroll data shape:")
    print(df.shape)
 
    # Display remaining missing values
    print("\nremaining missing values:")
    print(df.isnull().sum())
 
    return df

# transformation
def transform_payroll(df):
    """Perform payroll calculations and analytics."""
 
    df = df.copy()
 
    # gross salary = basic salary + hra + bonus
    df["GrossSalary"] = (
        df["BasicSalary"] + df["HRA"] + df["Bonus"]
    )
 
    # net salary = gross salary - deductions
    df["NetSalary"] = df["GrossSalary"] - df["Deductions"]
 
    # calculate attendance percentage using present and working days
    df["AttendancePercentage"] = (
        df["PresentDays"] / df["WorkingDays"]
    ) * 100
 
    # categorize employees based on their basic salary
    df["SalaryCategory"] = np.select(
        [
            df["BasicSalary"] < 30000,
            df["BasicSalary"] < 70000
        ],
        [
            "Low",
            "Medium"
        ],
        default="High"
    )
 
    high_salary_df = df[df["BasicSalary"] > 75000]
 
    print("\nEmployees earning more than 75000: ")
    print(high_salary_df.head())
 
    # sort payroll records in descending order of BasicSalary
    df = df.sort_values(
        by="BasicSalary",
        ascending=False
    )
 
    # calculate average salary and total payroll for each department
    department_summary = df.groupby("Department").agg(
        AverageSalary=("BasicSalary", "mean"),
        TotalPayroll=("NetSalary", "sum"),
        EmployeeCount=("EmployeeID", "nunique")
    )
 
    print("\ndepartment-wise payroll summary: ")
    print(department_summary)
 
    # select the 10 highest-paid payroll records
    top_10 = df.nlargest(10, "BasicSalary")
 
    print("\ntop 10 highest-paid employees: ")
    print(top_10)
 
    # create a pivot table showing total net salary by department
    payroll_pivot = pd.pivot_table(
        df,
        index="Department",
        values="NetSalary",
        aggfunc="sum"
    )
 
    print("\nDepartment payroll pivot:")
    print(payroll_pivot)
 
    return df

def validate_payroll(
    input_df: pd.DataFrame,
    accepted_df: pd.DataFrame,
    rejected_df: pd.DataFrame
) -> None:
    """Validate payroll records and payroll totals."""
 
    # Ccunt total records received from the CSV
    input_count = input_df.shape[0]
 
    # count accepted payroll records
    accepted_count = accepted_df.shape[0]
 
    # count rejected payroll records
    rejected_count = rejected_df.shape[0]
 
    # calculate total records processed
    total_processed = accepted_count + rejected_count
 
    print("\n========== PAYROLL VALIDATION ==========")
 
    print("Input Records:", input_count)
    print("Accepted Records:", accepted_count)
    print("Rejected Records:", rejected_count)
    print("Total Processed Records:", total_processed)
 
    # check whether all input records are accounted for
    if input_count == total_processed:
        print("Record Count Validation: PASSED")
    else:
        raise ValueError("Record count validation failed!")
 
    # calculate total net payroll
    total_payroll = accepted_df["NetSalary"].sum()
 
    print("\nTotal Accepted Payroll:", total_payroll)
 
    print("Payroll validation completed successfully!")
 

def run_etl_pipeline():
    """Execute the complete payroll ETL pipeline."""
 
    # Step 1: Create required project folders
    create_folder()
 
    # Step 2: Extract raw payroll data from CSV
    payroll_df = extract_data()
 
    # Step 3: Inspect the extracted payroll data
    inspect_data(payroll_df)
 
    # Step 4: Clean the extracted payroll data
    cleaned_df = clean_payroll(payroll_df)
 
    # Step 5: Transform the cleaned payroll data
    transformed_df = transform_payroll(cleaned_df)

    # Step 6: Validate transformed data
    validate_payroll(transformed_df)
 
    # Display successful completion message
    print("\nPayroll ETL pipeline completed successfully!")
 
    # Return transformed payroll data
    return transformed_df


#Program starting point

if __name__ == "__main__":
    run_etl_pipeline()