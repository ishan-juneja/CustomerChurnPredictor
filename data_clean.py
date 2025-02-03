import mysql.connector

# Connect to your MySQL database
db = mysql.connector.connect(
	host="localhost",
	port=3306,
	user="root",
	password="Balderdash2004@",
	database="CustomerChurn"
)
cursor = db.cursor()

# Step 1: Get the column names of the table (excluding 'gender' to avoid grouping on it)
table_name = "Customers"
cursor.execute(f"SHOW COLUMNS FROM {table_name}")
columns = [row[0] for row in cursor.fetchall() if row[0] != "gender"]
print("hi")

# Step 2: Loop through the columns and find unique values
for column in columns:
	if column != "Tenure" and column != "customerID" and column != "MonthlyCharges" and column != "TotalCharges":
		query = f"SELECT DISTINCT `{column}` FROM `{table_name}`"
		print(f"Executing: {query}")
		cursor.execute(query)
		results = cursor.fetchall()

		print(f"Results for column `{column}`:")
		for row in results:
			print(row)


# Step 3: Clean the inconsistencies identified:
# eg: Executing: SELECT `PaperlessBilling`, COUNT(*) AS TotalCustomers FROM Customers GROUP BY gender, `PaperlessBilling`
# Results for column `PaperlessBilling`:
# ('Yes', 2085)
# ('No', 1466)
# ('Yes', 2083)
# ('No', 1398)


# Function to clean text fields
def clean_text(value):
    if isinstance(value, str):
        value = value.strip().upper().replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", " ")
        if value == "YES":
            return 1
        elif value == "NO":
            return 0
    return value  # If it's not a string, return as is


# Standardize columns
columns_to_clean = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                    'Churn', 'PaymentMethod', 'StreamingTV', 'gender', 'Dependents', 'Partner']
for column in columns_to_clean:
    # Fetch column values
    cursor.execute(f"SELECT CustomerID, {column} FROM Customers")
    rows = cursor.fetchall()

    for customer_id, value in rows:
        cleaned_value = clean_text(value)

        # Update only if value changed
        if cleaned_value != value:
            cursor.execute(f"UPDATE Customers SET {column} = %s WHERE CustomerID = %s", (cleaned_value, customer_id))


# What does having a No Internet Service name alongside no do? should we trim it

# Executing: SELECT `OnlineBackup`, COUNT(*) AS TotalCustomers FROM Customers GROUP BY gender, `OnlineBackup`
# Results for column `OnlineBackup`:
# ('Yes', 1223)
# ('No', 1573)
# ('Yes', 1202)
# ('No', 1514)
# ('No internet service', 746)
# ('No internet service', 774)

# Step 4: Review the changes I made
for column in columns:
	if column != "Tenure" and column != "customerID" and column != "MonthlyCharges" and column != "TotalCharges":
		query = f"SELECT DISTINCT `{column}` FROM `{table_name}`"
		print(f"Executing: {query}")
		cursor.execute(query)
		results = cursor.fetchall()

		print(f"Results for column `{column}`:")
		for row in results:
			print(row)

# Step 5: Finding the churn rate by specific values
'''
customers with shorter contracts tend to churn out faster --> intuitively makes sense
Month to Month - 42.71
One Year - 11.28
Two Year - 2.85

Seniors or not it doesn't feel that indicative --> 666 vs 476

Partner Difference is a lot stronger: 2724 vs 669
Dependent Difference is also valid

for monthly charges there is a difference in 13 dollars
- how significant is this?

for electronic check vs the other 3
- the churn rate for electronic check is a lot higher

there is a significant difference between Fiber Optic, DSL, and No Internet
- we need to find a way to make internet service its own column as it 
  provides no other value otherwise
  
strange enough, the charges for the programs didn't seem to have a big difference
so we will take them out
'''


# Final observations
# - we have certain values such as no internet service, and categories that must be numerified for the ML Model
# - we can make it a question of whether one has an electric check or not vs checking for the specific type
# - not considering: tenure, seniors, monthly charges, total charges
# - we need to make the lines that say no internet service also 0, since technically its a no

# Close the connection
db.commit()
cursor.close()
db.close()
