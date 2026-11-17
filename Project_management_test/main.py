import pandas as pd

sales_df = pd.DataFrame ({

    "orderID": [1001,1002,1003,1004,1005,1006,1007,1008],
    "productID": ["P01","P02","P03","P01","P04","P02","P03","P04"],
    "city": ["Pune","Mumbai","Delhi","Pune","Mumbai","Delhi","Pune","Delhi"],
    "quantity": [2,3,1,1,4,2,2,3],
    "unitprice": [25000,1500,45000,25000,NaN,1500,45000,2500]
})

products_df = pd.DataFrame ({

    "productID": ["P01","P02","P03","P04"],
    "productName": ["Laptop","Keyboard","Smartphone","Headphones"],
    "category": ["Electronics","Accessories","Electronics","Accessories"]
})

print(products_df.shape)  #number of rows and columns (rows,columns)
print(sales_df.head(3))
print(sales_df.tail(3))
sales_df.info()
products_df.info()
sales_df.describe()
products_df.describe()

print(products_df.isna())
print(products_df.column.isnull().count())
products_df["unitprice"].isnull() = products_df["unitprice"].median() 

#Create a new column TotalAmount = Quantity * UnitPrice.
temp_df = sales_df.copy()
sales_df["TotalAmount"] = temp_df["quantity"] * temp_df["unitprice"]
print(sales_df)

#Filter orders having TotalAmount greater than ₹20,000.
print(sales_df["TotalAmount"].where(sales_df["TotalAmount"] > 20000))


print(sales_df["Quantity"].where(sales_df["City"] == "Pune").sum())

