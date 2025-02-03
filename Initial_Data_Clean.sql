-- DROP TABLE Customers;

CREATE TABLE Customers (
    customerID VARCHAR(20) PRIMARY KEY,
	gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    Tenure INT,
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(30),
    MonthlyCharges FLOAT,
    TotalCharges FLOAT,
    Churn VARCHAR(10)
);

SELECT * FROM Customers LIMIT 10; --  to check if it imported!

SELECT * FROM Customers WHERE totalCharges IS NULL OR totalCharges = '';

SELECT gender, COUNT(*) AS TotalCustomers FROM Customers GROUP BY gender;
SELECT SeniorCitizen, COUNT(*) AS TotalCustomers FROM Customers GROUP BY gender;

SELECT DISTINCT Churn FROM Customers;

SELECT contract, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS Churned,
       ROUND(AVG(CASE WHEN churn = 1 THEN 1.0 ELSE 0 END) * 100, 2) AS ChurnRate;


SELECT churn, AVG(monthlyCharges) AS AvgMonthlyCharges
FROM Customers
GROUP BY churn;

SELECT churn, SUM(SeniorCitizen) AS SeniorOrNot
FROM Customers
GROUP BY churn;

SELECT churn, SUM(Partner) AS PartnerCount
FROM Customers
GROUP BY churn;

SELECT churn, SUM(Dependents) AS DependentCount
FROM Customers
GROUP BY churn;

SELECT 
    InternetService,
    COUNT(*) AS CustomerCount, 
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM Customers
GROUP BY InternetService
ORDER BY InternetService;

SELECT paymentMethod, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN churn = '1' THEN 1 ELSE 0 END) AS Churned,
       ROUND(AVG(CASE WHEN churn = '1' THEN 1.0 ELSE 0 END) * 100, 2) AS ChurnRate
FROM Customers
GROUP BY paymentMethod
ORDER BY ChurnRate DESC
LIMIT 5;

SELECT InternetService, 
       COUNT(*) AS TotalServices,
       SUM(CASE WHEN churn = '1' THEN 1 ELSE 0 END) AS Churned,
       ROUND(AVG(CASE WHEN churn = '1' THEN 1.0 ELSE 0 END) * 100, 2) AS ChurnRate
FROM Customers
GROUP BY InternetService
ORDER BY ChurnRate DESC
LIMIT 5;

SELECT tenure, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN churn = '0' THEN 1 ELSE 0 END) AS Retained
FROM Customers
GROUP BY tenure;

SELECT COUNT(*) 
FROM Customers 
WHERE InternetService = 0;

UPDATE Customers
SET Contract = CASE 
    WHEN Contract = 'Month-to-month' THEN 0
    WHEN Contract = 'One year' THEN 1
    WHEN Contract = 'Two year' THEN 1
    ELSE Contract
END,
PaymentMethod = CASE 
    WHEN PaymentMethod = 'Electronic check' THEN 1
    ELSE 0
END;

ALTER TABLE Customers
DROP COLUMN tenure,
DROP COLUMN SeniorCitizen,
DROP COLUMN MonthlyCharges,
DROP COLUMN TotalCharges;

SET SQL_SAFE_UPDATES = 0;

UPDATE Customers
SET OnlineSecurity = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE OnlineSecurity END,
    OnlineBackup = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE OnlineBackup END,
    DeviceProtection = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE DeviceProtection END,
    TechSupport = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE TechSupport END,
    StreamingTV = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE StreamingTV END,
    StreamingMovies = CASE WHEN InternetService = 'No internet service' THEN 0 ELSE StreamingMovies END
WHERE InternetService = '0';

UPDATE Customers
SET Contract = CASE 
    WHEN Contract = 'Month-to-month' THEN 0
    WHEN Contract = 'One year' THEN 1
    WHEN Contract = 'Two year' THEN 1
    ELSE Contract
END,
PaymentMethod = CASE 
    WHEN PaymentMethod = 'Electronic check' THEN 1
    ELSE 0
END;

SELECT InternetService, OnlineSecurity, OnlineBackup, DeviceProtection
FROM Customers
WHERE InternetService = '0';

SELECT InternetService, COUNT(*) AS occurrence_count
FROM Customers
GROUP BY InternetService;

SET SQL_SAFE_UPDATES = 0;

UPDATE Customers
SET OnlineSecurity = CASE WHEN OnlineSecurity = 'No internet service' THEN 0 ELSE OnlineSecurity END,
    OnlineBackup = CASE WHEN OnlineBackup = 'No internet service' THEN 0 ELSE OnlineBackup END,
    DeviceProtection = CASE WHEN DeviceProtection = 'No internet service' THEN 0 ELSE DeviceProtection END,
    TechSupport = CASE WHEN TechSupport = 'No internet service' THEN 0 ELSE TechSupport END,
    StreamingTV = CASE WHEN StreamingTV = 'No internet service' THEN 0 ELSE StreamingTV END,
    StreamingMovies = CASE WHEN StreamingMovies = 'No internet service' THEN 0 ELSE StreamingMovies END;

UPDATE Customers
SET MultipleLines = CASE WHEN MultipleLines = 'No phone service' THEN 0 ELSE MultipleLines END;

ALTER TABLE Customers
DROP COLUMN gender;

UPDATE Customers
SET InternetService = CASE 
    WHEN InternetService IN ('DSL', 'Fiber optic') THEN 1
    ELSE 0
END;


SELECT * 
INTO OUTFILE '/var/lib/mysql-files/customers.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
FROM Customers;


SELECT * FROM Customers;

describe Customers;
