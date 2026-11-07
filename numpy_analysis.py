#Step1 Import Numpy
import numpy as np
#step2 create salary array
salary = np.array([65000,58000,72000,80000,85000,68000,90000,76000])
print("==========Salary=========")
print(salary)

#step3 check numpy array properties
print("==========Salary Operations=========")
print("Array: ",salary)
print("Type: ", type(salary))
print("Dimensions: ", salary.ndim)
print("Shape: ",(salary.shape))
print("Size: ",(salary.size))
print("Data Type: ",(salary.dtype))

salary = np.array([65000,58000,72000,80000,85000,68000,90000,76000])
print("Dimensions: ", salary.ndim)

rating = np.array([4,5,4,2,4,8,4,6])
print("==========Rating=========")
print(rating)

#check properties
print("==========Ratings Properties=========")
print("Rating Shape",rating.shape)
print("Rating Size",rating.size)
print("Rating Data Type",rating.dtype)

#step5 numpy indexing
print("=============Numpy Indexing============")
print("First Salary:",salary[0])
print("Third Salary:",salary[2])
print("Last Salary:",salary[-1])
print("Second Last Salary:",salary[-2])
print("Third Last Salary:",salary[-3])

#step6 numy slicing
#first three:
print("==========numpy slicing=========")
print(salary[0:3])

#last three
print(salary[-3:])

#all except first two
print(salary[2:])

#Find employees Earing Above 75000
#Business: Identify employees in a higher salary bracket
print("============Salary Above 75000=========")

high_salary = salary[salary > 75000]
print("Employees Salary: ",high_salary)
print("Employee Count: ",len(high_salary))

#Find employees with rating above 4.5
#Business: Identify high-performing Employees.
print("==========high performing employees========")
high_rating = rating[rating > 4.5]
print("High Ratings: ",high_rating)
print("Number of Employees: ",len(high_rating))

#condotional salary increment
#business: employee earning below 70000 get 10% increment
#other employees recieve 5%
new_salary = np.where(salary < 70000,salary * 1.10,salary * 1.05)
print("Original salary: ",salary)
print("Updated Salary: ",new_salary)

#performance_based bonus
#business: employees rated 4.5 or above recieve 15% bonus
#other employeees recieve 5%
print("===========Performance Bonus=========")

bonus = np.where (rating >= 4.5,salary * 0.15, salary * 0.05)
print("Employee Bonus:",bonus)

#calculate salary after bonus
#business: calculate salary plus performance bonus

print("==========Salary after bonus=========")
salary_with_bonus = salary + bonus

print("Original salary:",salary)
print("Bonus: ",bonus)
print("Salary after bonus: ",salary_with_bonus)

