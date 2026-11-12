import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------
# FILE PATHS AND OUTPUT FOLDER
# ---------------------------------------------------------------------

SALES_FILE = "Cadbury_Dairy_Milk_Sales_2025_Synthetic.csv"
PRODUCT_FILE = "Cadbury_Product_Master.csv"
STORE_FILE = "Cadbury_Store_Master.csv"

# ---------------------------------------------------------------------
# PANDAS A — DATA LOADING AND INSPECTION (P01-P15)
# ---------------------------------------------------------------------

# P01. Load the sales CSV into a DataFrame.
df = pd.read_csv(SALES_FILE)

# P02. Display the first 10 records.
print("\nP02 — First 10 records")
print(df.head(10))

# P03. Display the last 10 records.
print("\nP03 — Last 10 records")
print(df.tail(10))

# P04. Find the number of rows and columns.
print("\nP04 — Number of rows and columns")
print("Rows:", df.shape[0], "| Columns:", df.shape[1])

# P05. List all column names.
print("\nP05 — Column names")
print(df.columns.tolist())

# P06. Inspect column data types.
print("\nP06 — Data types")
print(df.dtypes)

# P07. Generate a concise DataFrame information summary.
print("\nP07 — DataFrame information")
df.info()

# P08. Calculate descriptive statistics for numeric fields.
print("\nP08 — Numeric descriptive statistics")
print(df.describe())

# P09. Calculate descriptive statistics for categorical fields.
print("\nP09 — Categorical descriptive statistics")
print(df.describe(include=["object"]))

# P10. Identify missing values by column.
print("\nP10 — Missing values by column")
print(df.isna().sum())

# P11. Count duplicate Order_ID values.
print("\nP11 — Duplicate Order_ID count")
print(df["Order_ID"].duplicated().sum())

# P12. Find unique product names and their count.
print("\nP12 — Unique product names and count")
print(df["Product_Name"].unique())
print("Unique product count:", df["Product_Name"].nunique())

# P13. Find unique cities and regions.
print("\nP13 — Unique cities and regions")
print("Cities:", sorted(df["City"].dropna().unique()))
print("Regions:", sorted(df["Region"].dropna().unique()))

# P14. Convert Order_Date to datetime and verify the result.
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
print("\nP14 — Order_Date data type")
print(df["Order_Date"].dtype)

# P15. Create a data dictionary listing every field and its business meaning.
data_dictionary = {
    "Order_ID": "Unique order identification number",
    "Order_Date": "Date when the order was placed",
    "Region": "Geographical sales region",
    "City": "City where the order was placed",
    "Store_ID": "Unique store identification number",
    "Sales_Channel": "Channel through which the product was sold",
    "Product_ID": "Unique product identification number",
    "Product_Name": "Name of the chocolate product",
    "Pack_Size_g": "Product pack size in grams",
    "Unit_MRP_INR": "Maximum retail price per unit",
    "Discount_Pct": "Discount percentage applied",
    "Unit_Selling_Price_INR": "Actual selling price per unit",
    "Quantity": "Number of units ordered",
    "Gross_Sales_INR": "Sales value before discount",
    "Net_Revenue_INR": "Revenue after discount",
    "Unit_Cost_INR": "Cost of one product unit",
    "Total_Cost_INR": "Total product cost for the order",
    "Delivery_Cost_INR": "Delivery expense for the order",
    "Profit_INR": "Profit earned from the order",
    "Payment_Method": "Method used to pay",
    "Customer_Age": "Age of the customer",
    "Customer_Segment": "Customer category",
    "Customer_Rating": "Customer rating for the transaction",
    "Promotion_Flag": "Indicator showing whether a promotion was applied",
    "Returned_Flag": "Indicator showing whether the order was returned",
}
data_dictionary_df = pd.DataFrame(
    list(data_dictionary.items()),
    columns=["Column_Name", "Business_Meaning"]
)
print("\nP15 — Data dictionary")
print(data_dictionary_df.to_string(index=False))

# ---------------------------------------------------------------------
# PANDAS B — CLEANING AND FEATURE ENGINEERING (P16-P30)
# ---------------------------------------------------------------------

# P16. Create a working copy without modifying raw data.
sales = df.copy()

# P17. Remove exact duplicate records, if any.
sales = sales.drop_duplicates().copy()
print("\nP17 — Exact duplicate rows removed; remaining rows:", len(sales))

# P18. Apply a consistent naming convention to columns.
# Existing column names already use underscores; this standardizes whitespace.
sales.columns = (
    sales.columns.str.strip()
    .str.replace(r"\s+", "_", regex=True)
)
print("\nP18 — Standardized column names")
print(sales.columns.tolist())

# P19. Validate that Quantity is positive.
invalid_quantity = sales[sales["Quantity"] <= 0]
print("\nP19 — Records with non-positive Quantity")
print(invalid_quantity)

# P20. Identify records with Discount_Pct outside 0-100.
invalid_discount = sales[
    (sales["Discount_Pct"] < 0) | (sales["Discount_Pct"] > 100)
]
print("\nP20 — Discount outside 0-100")
print(invalid_discount)

# P21. Detect negative revenue, cost, or profit values and explain their meaning.
negative_financial_values = sales[
    (sales["Gross_Sales_INR"] < 0)
    | (sales["Net_Revenue_INR"] < 0)
    | (sales["Total_Cost_INR"] < 0)
    | (sales["Delivery_Cost_INR"] < 0)
    | (sales["Profit_INR"] < 0)
]
print("\nP21 — Records with negative financial values")
print(negative_financial_values)
print(
    "Interpretation: negative revenue or cost values may indicate data issues "
    "or adjustments; negative profit indicates a loss-making order. "
    "Returned_Flag alone does not reverse a transaction in this case study."
)

# P22. Recalculate Net_Revenue_INR from Quantity and Unit_Selling_Price_INR.
sales["Recomputed_Net_Revenue_INR"] = (
    sales["Quantity"] * sales["Unit_Selling_Price_INR"]
)
print("\nP22 — Recomputed net revenue (sample)")
print(sales[["Order_ID", "Net_Revenue_INR", "Recomputed_Net_Revenue_INR"]].head())

# P23. Compare recorded and recomputed revenue with a tolerance.
tolerance = 0.01
sales["Revenue_Difference_INR"] = (
    sales["Net_Revenue_INR"] - sales["Recomputed_Net_Revenue_INR"]
)
sales["Revenue_Matches"] = sales["Revenue_Difference_INR"].abs() <= tolerance
print("\nP23 — Revenue comparison")
print("Rows within tolerance:", int(sales["Revenue_Matches"].sum()))
print("Rows outside tolerance:", int((~sales["Revenue_Matches"]).sum()))

# P24. Recalculate Profit_INR using revenue, costs, and delivery.
sales["Recomputed_Profit_INR"] = (
    sales["Recomputed_Net_Revenue_INR"]
    - sales["Total_Cost_INR"]
    - sales["Delivery_Cost_INR"]
)
print("\nP24 — Recomputed profit (sample)")
print(sales[["Order_ID", "Profit_INR", "Recomputed_Profit_INR"]].head())

# P25. Create Profit_Margin_Pct with safe division.
sales["Profit_Margin_Pct"] = np.where(
    sales["Recomputed_Net_Revenue_INR"] != 0,
    sales["Recomputed_Profit_INR"] / sales["Recomputed_Net_Revenue_INR"] * 100,
    np.nan
)
print("\nP25 — Profit margin (sample)")
print(sales[["Order_ID", "Profit_Margin_Pct"]].head())

# P26. Create Year, Month, and Month_Name fields from Order_Date.
sales["Year"] = sales["Order_Date"].dt.year
sales["Month"] = sales["Order_Date"].dt.month
sales["Month_Name"] = sales["Order_Date"].dt.month_name()

# P27. Create Quarter and Weekday fields.
sales["Quarter"] = sales["Order_Date"].dt.to_period("Q").astype(str)
sales["Weekday"] = sales["Order_Date"].dt.day_name()

# P28. Create Weekend_Flag from Order_Date.
sales["Weekend_Flag"] = sales["Order_Date"].dt.dayofweek >= 5

# P29. Create Discount_Band categories (none, low, medium, high).
# Assumption: low = >0-5%, medium = >5-15%, high = >15%.
discount_bins = [-np.inf, 0, 5, 15, np.inf]
discount_labels = ["none", "low", "medium", "high"]
sales["Discount_Band"] = pd.cut(
    sales["Discount_Pct"],
    bins=discount_bins,
    labels=discount_labels,
    right=True
)

# P30. Create Order_Value_Band using quantiles or defined thresholds.
# qcut creates three approximately equal-sized groups where possible.
sales["Order_Value_Band"] = pd.qcut(
    sales["Recomputed_Net_Revenue_INR"],
    q=3,
    labels=["Low", "Medium", "High"],
    duplicates="drop"
)
print("\nP26-P30 — Engineered columns (sample)")
print(
    sales[
        [
            "Order_Date", "Year", "Month", "Month_Name", "Quarter",
            "Weekday", "Weekend_Flag", "Discount_Band", "Order_Value_Band"
        ]
    ].head()
)

# ---------------------------------------------------------------------
# PANDAS C — SELECTION, FILTERING AND SORTING (P31-P45)
# ---------------------------------------------------------------------

# P31. Select Order_ID, Product_Name, City, Quantity and Net_Revenue_INR.
print("\nP31 — Selected columns")
print(
    sales[
        ["Order_ID", "Product_Name", "City", "Quantity", "Net_Revenue_INR"]
    ]
)

# P32. Filter transactions from Mumbai.
print("\nP32 — Mumbai transactions")
print(sales[sales["City"].str.casefold() == "mumbai"])

# P33. Filter orders for Dairy Milk Silk.
print("\nP33 — Dairy Milk Silk orders")
print(sales[sales["Product_Name"] == "Dairy Milk Silk"])

# P34. Filter transactions with Quantity >= 10.
print("\nP34 — Quantity >= 10")
print(sales[sales["Quantity"] >= 10])

# P35. Filter orders with Discount_Pct >= 15.
print("\nP35 — Discount >= 15%")
print(sales[sales["Discount_Pct"] >= 15])

# P36. Find loss-making orders where Profit_INR < 0.
print("\nP36 — Loss-making orders")
print(sales[sales["Recomputed_Profit_INR"] < 0])

# P37. Find orders from North region placed in Q4.
print("\nP37 — North region, Q4 orders")
print(sales[(sales["Region"] == "North") & (sales["Order_Date"].dt.quarter == 4)])

# P38. Filter e-commerce orders paid by UPI.
print("\nP38 — E-commerce orders paid by UPI")
print(
    sales[
        (sales["Sales_Channel"].str.casefold() == "e-commerce")
        & (sales["Payment_Method"].str.casefold() == "upi")
    ]
)

# P39. Find orders between two user-selected dates.
# Change these dates when you want a different date range.
start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2025-03-31")
print("\nP39 — Orders between selected dates")
print(sales[sales["Order_Date"].between(start_date, end_date)])

# P40. Find orders where Product_Name contains Dairy Milk.
print("\nP40 — Product name contains 'Dairy Milk'")
print(sales[sales["Product_Name"].str.contains("Dairy Milk", case=False, na=False)])

# P41. Find transactions with Customer_Rating <= 2.
print("\nP41 — Customer rating <= 2")
print(sales[sales["Customer_Rating"] <= 2])

# P42. Sort orders by Net_Revenue_INR descending.
print("\nP42 — Orders sorted by net revenue descending")
print(sales.sort_values("Recomputed_Net_Revenue_INR", ascending=False))

# P43. Show the top 20 orders by Profit_INR.
print("\nP43 — Top 20 orders by profit")
print(sales.nlargest(20, "Recomputed_Profit_INR"))

# P44. Sort by Region ascending then Quantity descending.
print("\nP44 — Region ascending, Quantity descending")
print(sales.sort_values(["Region", "Quantity"], ascending=[True, False]))

# P45. Select transactions meeting three simultaneous business conditions.
# Example conditions: West region, discount >= 10%, and positive profit.
print("\nP45 — West + discount >= 10% + profitable orders")
print(
    sales[
        (sales["Region"] == "West")
        & (sales["Discount_Pct"] >= 10)
        & (sales["Recomputed_Profit_INR"] > 0)
    ]
)

# ---------------------------------------------------------------------
# PANDAS D — AGGREGATION AND BUSINESS METRICS (P46-P60)
# ---------------------------------------------------------------------

# P46. Calculate total net revenue.
total_revenue = sales["Recomputed_Net_Revenue_INR"].sum()
print("\nP46 — Total net revenue:", total_revenue)

# P47. Calculate total profit.
total_profit = sales["Recomputed_Profit_INR"].sum()
print("\nP47 — Total profit:", total_profit)

# P48. Calculate total quantity sold.
total_quantity = sales["Quantity"].sum()
print("\nP48 — Total quantity sold:", total_quantity)

# P49. Calculate overall profit margin percentage.
overall_margin = (
    total_profit / total_revenue * 100 if total_revenue != 0 else np.nan
)
print("\nP49 — Overall profit margin (%):", overall_margin)

# P50. Calculate average order value.
average_order_value = (
    total_revenue / sales["Order_ID"].nunique()
    if sales["Order_ID"].nunique() else np.nan
)
print("\nP50 — Average order value:", average_order_value)

# P51. Count orders by Sales_Channel.
print("\nP51 — Order count by sales channel")
print(sales.groupby("Sales_Channel")["Order_ID"].nunique())

# P52. Calculate revenue by Product_Name.
print("\nP52 — Revenue by product")
revenue_by_product = sales.groupby("Product_Name")["Recomputed_Net_Revenue_INR"].sum()
print(revenue_by_product.sort_values(ascending=False))

# P53. Calculate profit by Region.
print("\nP53 — Profit by region")
profit_by_region = sales.groupby("Region")["Recomputed_Profit_INR"].sum()
print(profit_by_region.sort_values(ascending=False))

# P54. Calculate units sold by City.
print("\nP54 — Units sold by city")
print(sales.groupby("City")["Quantity"].sum().sort_values(ascending=False))

# P55. Find the top five products by revenue.
print("\nP55 — Top five products by revenue")
print(revenue_by_product.nlargest(5))

# P56. Find the bottom five cities by profit.
print("\nP56 — Bottom five cities by profit")
print(
    sales.groupby("City")["Recomputed_Profit_INR"]
    .sum()
    .nsmallest(5)
)

# P57. Calculate mean and median discount by channel.
print("\nP57 — Mean and median discount by channel")
print(
    sales.groupby("Sales_Channel")["Discount_Pct"]
    .agg(["mean", "median"])
)

# P58. Calculate revenue and profit grouped by Region and Product_Name.
print("\nP58 — Revenue and profit by region and product")
print(
    sales.groupby(["Region", "Product_Name"])[
        ["Recomputed_Net_Revenue_INR", "Recomputed_Profit_INR"]
    ].sum()
)

# P59. Calculate order count, revenue, and average rating by Customer_Segment.
print("\nP59 — Metrics by customer segment")
print(
    sales.groupby("Customer_Segment").agg(
        Order_Count=("Order_ID", "nunique"),
        Revenue=("Recomputed_Net_Revenue_INR", "sum"),
        Average_Rating=("Customer_Rating", "mean")
    )
)

# P60. Calculate return rate by product using Returned_Flag.
print("\nP60 — Return rate by product (%)")
print(
    sales.groupby("Product_Name")["Returned_Flag"].mean().mul(100)
)

# ---------------------------------------------------------------------
# PANDAS E — ADVANCED ANALYTICS AND JOINS (P61-P75)
# ---------------------------------------------------------------------

# P61. Build a monthly revenue trend table.
monthly_revenue = (
    sales.groupby(sales["Order_Date"].dt.to_period("M"))[
        "Recomputed_Net_Revenue_INR"
    ].sum().rename("Revenue").reset_index()
)
monthly_revenue["Order_Date"] = monthly_revenue["Order_Date"].astype(str)
print("\nP61 — Monthly revenue trend")
print(monthly_revenue)

# P62. Compute month-over-month revenue growth percentage.
monthly_revenue["MoM_Growth_Pct"] = monthly_revenue["Revenue"].pct_change() * 100
print("\nP62 — Month-over-month revenue growth")
print(monthly_revenue)

# P63. Build a quarterly profit comparison.
print("\nP63 — Quarterly profit comparison")
quarterly_profit = (
    sales.groupby(sales["Order_Date"].dt.to_period("Q"))[
        "Recomputed_Profit_INR"
    ].sum()
)
print(quarterly_profit)

# P64. Create a pivot table: Region by Product_Name with revenue totals.
print("\nP64 — Region x Product revenue pivot")
region_product_pivot = pd.pivot_table(
    sales,
    index="Region",
    columns="Product_Name",
    values="Recomputed_Net_Revenue_INR",
    aggfunc="sum",
    fill_value=0
)
print(region_product_pivot)

# P65. Create a pivot table: Sales_Channel by Month with order counts.
print("\nP65 — Sales channel x month order-count pivot")
channel_month_pivot = pd.pivot_table(
    sales,
    index="Sales_Channel",
    columns="Month",
    values="Order_ID",
    aggfunc="nunique",
    fill_value=0
)
print(channel_month_pivot)

# P66. Create a cross-tab of Customer_Segment versus Payment_Method.
print("\nP66 — Customer segment x payment method cross-tab")
print(pd.crosstab(sales["Customer_Segment"], sales["Payment_Method"]))

# P67. Calculate a seven-day rolling revenue average on daily totals.
daily_revenue = (
    sales.groupby(sales["Order_Date"].dt.normalize())[
        "Recomputed_Net_Revenue_INR"
    ].sum().sort_index()
)
daily_rolling_average = daily_revenue.rolling(window=7, min_periods=1).mean()
print("\nP67 — Daily revenue and seven-day rolling average")
print(pd.DataFrame({
    "Daily_Revenue": daily_revenue,
    "Seven_Day_Rolling_Average": daily_rolling_average
}))

# P68. Calculate cumulative revenue over time.
cumulative_revenue = daily_revenue.cumsum()
print("\nP68 — Cumulative revenue")
print(cumulative_revenue)

# P69. Rank products within each region by revenue.
region_product_revenue = (
    sales.groupby(["Region", "Product_Name"])["Recomputed_Net_Revenue_INR"]
    .sum().reset_index()
)
region_product_revenue["Revenue_Rank"] = (
    region_product_revenue.groupby("Region")["Recomputed_Net_Revenue_INR"]
    .rank(method="dense", ascending=False)
)
print("\nP69 — Product revenue rank within each region")
print(region_product_revenue.sort_values(["Region", "Revenue_Rank"]))

# P70. Calculate each product share of total revenue.
product_share = (
    sales.groupby("Product_Name")["Recomputed_Net_Revenue_INR"].sum()
    .div(total_revenue).mul(100).sort_values(ascending=False)
)
print("\nP70 — Product share of total revenue (%)")
print(product_share)

# P71. Merge sales with the product master on Product_ID.
product_master = pd.read_csv(PRODUCT_FILE)
sales_product = sales.merge(
    product_master,
    on="Product_ID",
    how="left",
    suffixes=("", "_Master"),
    validate="many_to_one"
)
print("\nP71 — Sales merged with product master")
print(sales_product.head())

# P72. Merge sales with the store master on Store_ID.
store_master = pd.read_csv(STORE_FILE)
sales_product_store = sales_product.merge(
    store_master,
    on="Store_ID",
    how="left",
    validate="many_to_one"
)
print("\nP72 — Sales merged with store master")
print(sales_product_store.head())

# P73. Compare actual unit MRP with standard product master MRP.
sales_product_store["MRP_Difference_INR"] = (
    sales_product_store["Unit_MRP_INR"]
    - sales_product_store["Standard_MRP_INR"]
)
sales_product_store["MRP_Matches_Master"] = (
    sales_product_store["MRP_Difference_INR"].abs() <= 0.01
)
print("\nP73 — Actual versus standard MRP")
print(
    sales_product_store[
        [
            "Product_ID", "Product_Name", "Unit_MRP_INR",
            "Standard_MRP_INR", "MRP_Difference_INR", "MRP_Matches_Master"
        ]
    ].drop_duplicates().sort_values("Product_ID")
)

# P74. Calculate store-level revenue, profit, order count and average order value.
store_metrics = (
    sales_product_store.groupby("Store_ID").agg(
        Revenue=("Recomputed_Net_Revenue_INR", "sum"),
        Profit=("Recomputed_Profit_INR", "sum"),
        Order_Count=("Order_ID", "nunique")
    )
)
store_metrics["Average_Order_Value"] = (
    store_metrics["Revenue"] / store_metrics["Order_Count"]
)
store_metrics = store_metrics.reset_index()
print("\nP74 — Store-level metrics")
print(store_metrics.sort_values("Revenue", ascending=False))

# P75. Identify top-performing stores and prepare a five-point management summary.
top_stores = store_metrics.nlargest(5, "Revenue")
print("\nP75 — Top five stores")
print(top_stores)

best_store = top_stores.iloc[0] if not top_stores.empty else None
best_product = revenue_by_product.idxmax() if not revenue_by_product.empty else "N/A"
best_region = profit_by_region.idxmax() if not profit_by_region.empty else "N/A"
best_channel = (
    sales.groupby("Sales_Channel")["Recomputed_Net_Revenue_INR"].sum().idxmax()
)
highest_return_product = (
    sales.groupby("Product_Name")["Returned_Flag"].mean().idxmax()
)
management_summary = [
    f"Total net revenue was INR {total_revenue:,.2f} and total profit was INR {total_profit:,.2f}.",
    f"{best_product} was the highest-revenue product.",
    f"{best_region} generated the highest total profit among regions.",
    f"{best_channel} was the highest-revenue sales channel.",
    f"{highest_return_product} had the highest return rate; investigate product/customer feedback."
]
if best_store is not None:
    management_summary.append(
        f"Store {best_store['Store_ID']} led store revenue at INR {best_store['Revenue']:,.2f}."
    )
print("\nManagement summary")
for point in management_summary[:5]:
    print("-", point)

# ---------------------------------------------------------------------
# NUMPY A — ARRAY FUNDAMENTALS (N01-N10)
# ---------------------------------------------------------------------

# N01. Convert Quantity to a NumPy array.
quantity_array = sales["Quantity"].to_numpy()
print("\nN01 — Quantity array")
print(quantity_array)

# N02. Convert Net_Revenue_INR to a NumPy array.
revenue_array = sales["Recomputed_Net_Revenue_INR"].to_numpy()
print("\nN02 — Revenue array")
print(revenue_array)

# N03. Inspect array dimensions, shape, size and dtype.
print("\nN03 — Quantity array properties")
print("Dimensions:", quantity_array.ndim)
print("Shape:", quantity_array.shape)
print("Size:", quantity_array.size)
print("Data type:", quantity_array.dtype)

# N04. Create an array of unique discount percentages.
unique_discounts = np.unique(sales["Discount_Pct"].dropna().to_numpy())
print("\nN04 — Unique discount percentages")
print(unique_discounts)

# N05. Use np.arange to create day numbers 1 through 30.
day_numbers = np.arange(1, 31)
print("\nN05 — Day numbers")
print(day_numbers)

# N06. Use np.linspace to create 10 hypothetical discount rates from 0 to 30%.
hypothetical_discounts = np.linspace(0, 30, 10)
print("\nN06 — Ten hypothetical discount rates")
print(hypothetical_discounts)

# N07. Reshape the first 120 quantities into a 12 x 10 matrix.
quantity_matrix = quantity_array[:120].reshape(12, 10)
print("\nN07 — Quantity matrix (12 x 10)")
print(quantity_matrix)

# N08. Flatten the quantity matrix back to one dimension.
flattened_quantities = quantity_matrix.flatten()
print("\nN08 — Flattened quantity matrix")
print(flattened_quantities)

# N09. Concatenate the first 50 and next 50 revenue values.
concatenated_revenue = np.concatenate((revenue_array[:50], revenue_array[50:100]))
print("\nN09 — Concatenated revenue values")
print(concatenated_revenue)

# N10. Use boolean indexing to extract revenues above INR 1,000.
revenue_above_1000 = revenue_array[revenue_array > 1000]
print("\nN10 — Revenues above INR 1,000")
print(revenue_above_1000)

# ---------------------------------------------------------------------
# NUMPY B — STATISTICS AND NUMERICAL OPERATIONS (N11-N20)
# ---------------------------------------------------------------------

# N11. Calculate total revenue using np.sum.
print("\nN11 — Total revenue")
print(np.sum(revenue_array))

# N12. Calculate mean order revenue using np.mean.
print("\nN12 — Mean order revenue")
print(np.mean(revenue_array))

# N13. Calculate median order revenue using np.median.
print("\nN13 — Median order revenue")
print(np.median(revenue_array))

# N14. Calculate revenue standard deviation using np.std.
print("\nN14 — Revenue standard deviation")
print(np.std(revenue_array))

# N15. Calculate revenue variance using np.var.
print("\nN15 — Revenue variance")
print(np.var(revenue_array))

# N16. Calculate minimum and maximum transaction revenue.
print("\nN16 — Minimum and maximum revenue")
print("Minimum:", np.min(revenue_array))
print("Maximum:", np.max(revenue_array))

# N17. Calculate revenue percentiles at 25, 50, 75 and 90.
print("\nN17 — Revenue percentiles")
print(np.percentile(revenue_array, [25, 50, 75, 90]))

# N18. Calculate a weighted average selling price using quantities as weights.
weighted_average_price = np.average(
    sales["Unit_Selling_Price_INR"].to_numpy(),
    weights=quantity_array
)
print("\nN18 — Quantity-weighted average selling price")
print(weighted_average_price)

# N19. Calculate correlation between Discount_Pct and Quantity.
correlation = np.corrcoef(
    sales["Discount_Pct"].to_numpy(),
    quantity_array
)[0, 1]
print("\nN19 — Correlation between discount and quantity")
print(correlation)

# N20. Use np.unique(return_counts=True) to count order quantities.
unique_quantities, quantity_counts = np.unique(
    quantity_array, return_counts=True
)
print("\nN20 — Unique quantities and their counts")
print(pd.DataFrame({
    "Quantity": unique_quantities,
    "Count": quantity_counts
}))

# ---------------------------------------------------------------------
# NUMPY C — CONDITIONAL ANALYSIS AND SIMULATION (N21-N30)
# ---------------------------------------------------------------------

# N21. Use np.where to label orders as profitable or loss-making.
profit_labels = np.where(
    sales["Recomputed_Profit_INR"].to_numpy() >= 0,
    "Profitable",
    "Loss-making"
)
print("\nN21 — Profitability labels")
print(profit_labels)

# N22. Use np.select to assign low, medium and high revenue categories.
revenue_conditions = [
    sales["Recomputed_Net_Revenue_INR"].to_numpy() < 500,
    sales["Recomputed_Net_Revenue_INR"].to_numpy().between(500, 1500).to_numpy(),
    sales["Recomputed_Net_Revenue_INR"].to_numpy() > 1500
]
revenue_categories = np.select(
    revenue_conditions,
    ["Low", "Medium", "High"],
    default="Unknown"
)
print("\nN22 — Revenue categories")
print(revenue_categories)

# N23. Use np.clip to cap hypothetical discount rates at 20%.
capped_discounts = np.clip(hypothetical_discounts, 0, 20)
print("\nN23 — Discount rates capped at 20%")
print(capped_discounts)

# N24. Use np.round to format profit margins to two decimals.
rounded_margins = np.round(sales["Profit_Margin_Pct"].to_numpy(), 2)
print("\nN24 — Profit margins rounded to two decimals")
print(rounded_margins)

# N25. Use np.sort to obtain the ten largest order revenues.
ten_largest_revenues = np.sort(revenue_array)[-10:][::-1]
print("\nN25 — Ten largest order revenues")
print(ten_largest_revenues)

# N26. Use np.argsort to locate indices of the ten most profitable orders.
profit_array = sales["Recomputed_Profit_INR"].to_numpy()
top_profit_indices = np.argsort(profit_array)[-10:][::-1]
print("\nN26 — Indices of ten most profitable orders")
print(top_profit_indices)
print(sales.iloc[top_profit_indices][["Order_ID", "Recomputed_Profit_INR"]])

# N27. Use np.isnan or np.isfinite to test numeric-array validity.
print("\nN27 — Numeric array validity")
print("NaN values in revenue:", np.isnan(revenue_array).sum())
print("Non-finite revenue values:", (~np.isfinite(revenue_array)).sum())

# N28. Calculate projected revenue under a 5% unit sales uplift.
projected_revenue_5pct = np.sum(revenue_array) * 1.05
print("\nN28 — Projected revenue after 5% uplift")
print(projected_revenue_5pct)

# N29. Simulate 1,000 demand-growth scenarios using a fixed random seed and report percentiles.
rng = np.random.default_rng(seed=42)
growth_scenarios = rng.normal(loc=0.05, scale=0.02, size=1000)
simulated_revenues = total_revenue * (1 + growth_scenarios)
print("\nN29 — Demand-growth simulation percentiles")
print(np.percentile(simulated_revenues, [5, 25, 50, 75, 95]))

# N30. Calculate break-even quantity for a selected product using price, unit cost and an assumed fixed cost.
# Assumptions: choose Dairy Milk Classic; fixed cost is a hypothetical INR 10,000.
selected_product_id = "P01"
assumed_fixed_cost = 10000
selected_product = product_master.loc[
    product_master["Product_ID"] == selected_product_id
].iloc[0]
unit_contribution = (
    selected_product["Standard_MRP_INR"]
    - selected_product["Standard_Cost_INR"]
)
break_even_quantity = (
    np.ceil(assumed_fixed_cost / unit_contribution)
    if unit_contribution > 0 else np.inf
)
print("\nN30 — Break-even quantity")
print("Selected product:", selected_product["Product_Name"])
print("Assumed fixed cost:", assumed_fixed_cost)
print("Unit contribution:", unit_contribution)
print("Break-even quantity:", break_even_quantity)