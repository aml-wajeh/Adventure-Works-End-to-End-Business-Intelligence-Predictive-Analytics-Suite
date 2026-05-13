--1. Calculated Columns for dbo.internet_sales--------------------------------------------------------

-- Total Sales per Order
ALTER TABLE dbo.internet_sales ADD TotalSales money AS (ExtendedAmount - DiscountAmount);

-- Profit per Order
ALTER TABLE dbo.internet_sales ADD Profit money AS (SalesAmount - (ProductStandardCost * OrderQuantity));

-- Tax Rate
ALTER TABLE dbo.internet_sales ADD TaxRate float AS (TaxAmt / SalesAmount);

-- Freight Rate
ALTER TABLE dbo.internet_sales ADD FreightRate float AS (Freight / SalesAmount);

--TotalDiscountAmount:
OrderQuantity * UnitPrice * UnitPriceDiscountPct

--NetSalesAmount: 
SalesAmount - DiscountAmount

--ShippingDays: 
DATEDIFF(day, OrderDate, ShipDate)



--2. Calculated Columns for dbo.reseller_sales------------------------------------------------------

-- Total Sales per Order
ALTER TABLE dbo.reseller_sales ADD TotalSales money AS (ExtendedAmount - DiscountAmount);

-- Profit per Order
ALTER TABLE dbo.reseller_sales ADD Profit money AS (SalesAmount - (ProductStandardCost * OrderQuantity));

-- Tax Rate
ALTER TABLE dbo.reseller_sales ADD TaxRate float AS (TaxAmt / SalesAmount);

-- Freight Rate
ALTER TABLE dbo.reseller_sales ADD FreightRate float AS (Freight / SalesAmount);

--ResellerProfit: 
SalesAmount - TotalProductCost

--OrderProcessingDays: 
DATEDIFF(day, OrderDate, DueDate)



--3. Calculated Columns for dbo.product--------------------------------------------------------------

-- List Price to Standard Cost Ratio
ALTER TABLE dbo.product ADD ListPriceToStandardCostRatio float AS (CAST(ListPrice AS float) / CAST(StandardCost AS float));

-- Safety Stock Level Percentage
ALTER TABLE dbo.product ADD SafetyStockLevelPercentage float AS (SafetyStockLevel / ReorderPoint);

-- Days to Manufacture in Weeks
ALTER TABLE dbo.product ADD DaysToManufactureInWeeks float AS (DaysToManufacture / 7);

--ProfitMargin: 
(ListPrice - StandardCost) / ListPrice

--WeightInPounds: 
Weight * 2.20462 (Convert kg to lbs)

--SizeCategory: 
CASE WHEN Size < 10 THEN 'Small' WHEN Size BETWEEN 10 AND 20 THEN 'Medium' ELSE 'Large' END




--4. Calculated Columns for dbo.customer----------------------------------------------------------------

-- Average Yearly Income
ALTER TABLE dbo.customer ADD AverageYearlyIncome money AS (CAST(yearly_income AS money) / NULLIF(CAST(total_children AS int), 0));

-- Commute Distance in Miles
ALTER TABLE dbo.customer ADD CommuteDistanceInMiles float AS (CAST(commute_distance AS float) * 1.60934);

-- Age
ALTER TABLE dbo.customer ADD Age int AS (YEAR(GETDATE()) - YEAR(CAST(birth_date AS date)));

--Age:2
DATEDIFF(year, BirthDate, GETDATE())

--CustomerSegment:
CASE WHEN YearlyIncome < 50000 THEN 'Low' WHEN YearlyIncome BETWEEN 50000 AND 100000 THEN 'Medium' ELSE 'High' END




---5. Calculated Columns for dbo.employee---------------------------------------------------------------------

-- Years of Service
ALTER TABLE dbo.employees ADD YearsOfService int AS (YEAR(GETDATE()) - YEAR(CAST(HireDate AS date)));

-- Salary to Base Rate Ratio
ALTER TABLE dbo.employees ADD SalaryToBaseRateRatio float AS (CAST(BaseRate AS money) / NULLIF(CAST(Salary AS money), 0));

-- Sick Leave Balance
ALTER TABLE dbo.employees ADD SickLeaveBalance float AS (SickLeaveHours / NULLIF(CAST(VacationHours AS float), 0));




--6. Calculated Columns for dbo.product_inventory-----------------------------------------------------------------

-- Inventory Turnover Ratio
ALTER TABLE dbo.product_inventory ADD InventoryTurnoverRatio float AS (UnitsOut / NULLIF(UnitsBalance, 0));

-- Cost of Goods Sold
ALTER TABLE dbo.product_inventory ADD CostOfGoodsSold money AS (UnitCost * UnitsOut);

-- Inventory Value
ALTER TABLE dbo.product_inventory ADD InventoryValue money AS (UnitCost * UnitsBalance);




--7. Calculated Columns for dbo.promotion---------------------------------------------------------------------

-- Promotion Duration in Days
ALTER TABLE dbo.promotion ADD PromotionDuration int AS (DATEDIFF(DAY, CAST(StartDate AS date), CAST(EndDate AS date)));

-- Discount Amount per Unit
ALTER TABLE dbo.promotion ADD DiscountAmountPerUnit money AS (DiscountPct * UnitPrice);



--8. Calculated Columns for dbo.reseller------------------------------------------------------------------------

-- Annual Revenue to Sales Ratio
ALTER TABLE dbo.reseller ADD AnnualRevenueToSalesRatio float AS (CAST(AnnualSales AS money) / NULLIF(CAST(AnnualRevenue AS money), 0));

-- Number of Years in Business
ALTER TABLE dbo.reseller ADD YearsInBusiness int AS (YEAR(GETDATE()) - YEAR(CAST(YearOpened AS int)));

-- Order Frequency Score
ALTER TABLE dbo.reseller ADD OrderFrequencyScore float AS (CASE WHEN OrderFrequency = 'M' THEN 1 WHEN OrderFrequency = 'Q' THEN 4 WHEN OrderFrequency = 'Y' THEN 12 ELSE 0 END);



--9. Calculated Columns for dbo.sales_territory-----------------------------------------------------------------------

-- Territory Size Score
ALTER TABLE dbo.sales_territory ADD TerritorySizeScore float AS (CASE WHEN SalesTerritoryRegion = 'North America' THEN 1 WHEN SalesTerritoryRegion = 'South America' THEN 2 WHEN SalesTerritoryRegion = 'Europe' THEN 3 WHEN SalesTerritoryRegion = 'Asia' THEN 4 ELSE 5 END);




--10. Calculated Columns for dbo.geography----------------------------------------------------------------------------

-- Distance to Headquarters (assuming HQ in New York)
ALTER TABLE dbo.geography ADD DistanceToHQ float AS (SQRT(POWER((Longitude - 74), 2) + POWER((Latitude - 40), 2)));

-- State Population Estimate (hypothetical values)
ALTER TABLE dbo.geography ADD StatePopulationEstimate int AS (CASE WHEN StateProvinceCode = 'CA' THEN 39538223 WHEN StateProvinceCode = 'TX' THEN 29145505 WHEN StateProvinceCode = 'FL' THEN 21538187 ELSE 0 END);








---Key Measures----------------------------


--Total Sales:
SUM(FactInternetSales$.SalesAmount)

--Total Cost:
SUM(FactInternetSales$.TotalProductCost)

--Total Profit:
SUM(FactInternetSales$.SalesAmount) - SUM(FactInternetSales$.TotalProductCost)

--Average Discount Percentage:
AVG(FactInternetSales$.UnitPriceDiscountPct)

--Total Units Sold:
SUM(FactInternetSales$.OrderQuantity)

--Average Shipping Days:
AVG(FactInternetSales$.ShippingDays)

--Total Reseller Sales:
SUM(FactResellerSales$.SalesAmount)

--Total Reseller Profit:
SUM(FactResellerSales$.ResellerProfit)

--Total Customers:
COUNT(DimCustomer$.CustomerKey)

--Average Yearly Income:
AVG(DimCustomer$.YearlyIncome)

--Total Products:
COUNT(DimProduct$.ProductKey)

--Average Product Cost:
AVG(DimProduct$.StandardCost)

--Total Inventory Units:
SUM(FactProductInventory$.UnitsBalance)

--Total Inventory Cost:
SUM(FactProductInventory$.UnitsBalance * FactProductInventory$.UnitCost)

--Total Employees:
COUNT(DimEmployee$.EmployeeKey)

--Average Employee Vacation Hours:
AVG(DimEmployee$.VacationHours)

--Total Promotions:
COUNT(DimPromotion$.PromotionKey)

--Average Promotion Discount:
AVG(DimPromotion$.DiscountPct)

--Total Sales Territories:
COUNT(DimSalesTerritory$.SalesTerritoryKey)

--Average Reseller Order Frequency:
AVG(DimReseller$.OrderFrequency)








--analytic questions---------------------------------------------------------------------------------------

	-- Check FactInternetSales$
SELECT COUNT(*) FROM FactInternetSales$;

-- Check DimProduct$
SELECT COUNT(*) FROM DimProduct$;

-- Check DimProductSubCategory$
SELECT COUNT(*) FROM DimProductSubCategory$;

-- Check DimProductCategory$
SELECT COUNT(*) FROM DimProductCategory$;



--Total Sales Amount per Product
SELECT 
    p.EnglishProductName, 
    SUM(f.SalesAmount) AS TotalSales
FROM 
    FactInternetSales$ f
JOIN 
    DimProduct$ p ON f.ProductKey = p.ProductKey
GROUP BY 
    p.EnglishProductName;


--Total Number of Employees per Sales Territory
SELECT 
    SalesTerritoryKey, COUNT(*) AS EmployeeCount
FROM 
    DimEmployee$
GROUP BY 
    SalesTerritoryKey;


--Total Number of Cars Owned by Customers
SELECT 
    SUM(NumberCarsOwned) AS TotalCarsOwned
FROM 
    DimCustomer$;



--Number of Customers Who Own a House
SELECT 
    COUNT(*) AS HouseOwners
FROM 
    DimCustomer$
WHERE 
    HouseOwnerFlag = 1;


--Average Time to Manufacture a Product
SELECT 
    AVG(DaysToManufacture) AS AvgManufacturingTime
FROM 
    DimProduct$;


--Total Units In and Out per Product
SELECT 
    p.EnglishProductName, 
    SUM(i.UnitsIn) AS TotalUnitsIn, 
    SUM(i.UnitsOut) AS TotalUnitsOut
FROM 
    FactProductInventory$ i
JOIN 
    DimProduct$ p ON i.ProductKey = p.ProductKey
GROUP BY 
    p.EnglishProductName;


--Number of Sales Orders per Month
SELECT 
    d.EnglishMonthName, COUNT(*) AS OrderCount
FROM 
    FactInternetSales$ f
JOIN 
    DimDate$ d ON f.OrderDateKey = d.DateKey
GROUP BY 
    d.EnglishMonthName;


--Average Number of Children per Customer
SELECT 
    AVG(TotalChildren) AS AvgChildren
FROM 
    DimCustomer$;


--Total Tax Amount per Year
SELECT 
    d.CalendarYear, SUM(f.TaxAmt) AS TotalTaxAmount
FROM 
    FactInternetSales$ f
JOIN 
    DimDate$ d ON f.OrderDateKey = d.DateKey
GROUP BY 
    d.CalendarYear;


--Number of Employees in Each Department
SELECT 
    DepartmentName, COUNT(*) AS EmployeeCount
FROM 
    DimEmployee$
GROUP BY 
    DepartmentName;



--Average Order Quantity per Customer
SELECT 
    c.CustomerKey, AVG(f.OrderQuantity) AS AvgOrderQuantity
FROM 
    FactInternetSales$ f
JOIN 
    DimCustomer$ c ON f.CustomerKey = c.CustomerKey
GROUP BY 
    c.CustomerKey;


--Total Revenue per Sales Territory
SELECT 
    t.SalesTerritoryRegion, SUM(f.SalesAmount) AS TotalRevenue
FROM 
    FactInternetSales$ f
JOIN 
    DimSalesTerritory$ t ON f.SalesTerritoryKey = t.SalesTerritoryKey
GROUP BY 
    t.SalesTerritoryRegion;


--Number of Products Out of Stock
SELECT 
    COUNT(*) AS OutOfStockProducts
FROM 
    FactProductInventory$
WHERE 
    UnitsBalance = 0;


--Average Discount Percentage per Promotion
SELECT 
    PromotionKey, AVG(DiscountPct) AS AvgDiscountPercentage
FROM 
    DimPromotion$
GROUP BY 
    PromotionKey;








---Financial Analysis-------------------------------------------

--What are the total sales for each product?
SELECT ProductKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY ProductKey;


--What is the average order value for each customer?
SELECT CustomerKey, AVG(ExtendedAmount) AS AverageOrderValue
FROM dbo.internet_sales$
GROUP BY CustomerKey;


--What are the total profits for each product?
SELECT ProductKey, SUM(Profit) AS TotalProfit
FROM (
    SELECT ProductKey, SalesAmount, ProductStandardCost, OrderQuantity, 
           (SalesAmount - (ProductStandardCost * OrderQuantity)) AS Profit
    FROM dbo.internet_sales$
) AS SalesProfit
GROUP BY ProductKey;


--What is the total revenue by month?
SELECT OrderDateKey AS OrderMonth, SUM(SalesAmount) AS TotalRevenue
FROM dbo.internet_sales$
GROUP BY OrderDateKey;


--What are the top 10 best-selling products?
SELECT TOP 10 ProductKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY ProductKey
ORDER BY TotalSales DESC;


--What is the average discount percentage per order?
SELECT AVG(DiscountAmount) AS AverageDiscountPct
FROM dbo.internet_sales$;


--What is the total tax collected for each product?
SELECT ProductKey, SUM(TaxAmt) AS TotalTax
FROM dbo.internet_sales$
GROUP BY ProductKey;


--What is the average shipping cost per order?
SELECT AVG(Freight) AS AverageShippingCost
FROM dbo.internet_sales$;



--What is the total sales by sales territory?
SELECT SalesTerritoryKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY SalesTerritoryKey;


--What is the total revenue by product category?
SELECT ProductKey, SUM(SalesAmount) AS TotalRevenue
FROM dbo.internet_sales$
GROUP BY ProductKey;






--Customer Analysis----------------------------------------------------


--How many unique customers are there?
SELECT COUNT(DISTINCT CustomerKey) AS UniqueCustomers
FROM dbo.internet_sales$;



--What is the average yearly income of customers?
SELECT AVG(yearly_income) AS AverageYearlyIncome
FROM dbo.customer$;



--What is the total number of orders per customer?
SELECT CustomerKey, COUNT(*) AS TotalOrders
FROM dbo.internet_sales$
GROUP BY CustomerKey;



--What is the average order quantity per customer?
SELECT CustomerKey, AVG(OrderQuantity) AS AverageOrderQuantity
FROM dbo.internet_sales$
GROUP BY CustomerKey;


--What is the total sales per customer?
SELECT CustomerKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY CustomerKey;


--What is the average age of customers?
SELECT AVG(DATEDIFF(YEAR,birth_date, GETDATE())) AS AverageAge
FROM dbo.customer$;



--What is the total sales by gender?
SELECT gender, SUM(SalesAmount) AS TotalSales
FROM dbo.customer$  customer
JOIN dbo.internet_sales$  internet_sales
ON customer.customer_key = internet_sales.CustomerKey
GROUP BY gender;



--What is the average number of children per customer?
SELECT AVG(total_children) AS AverageChildren
FROM dbo.customer$;



--What is the total sales by marital status?
SELECT marital_status, SUM(SalesAmount) AS TotalSales
FROM dbo.customer$ customer
JOIN dbo.internet_sales$ internet_sales
ON customer.customer_key = internet_sales.CustomerKey
GROUP BY marital_status;



--What is the average commute distance per customer?
SELECT AVG(commute_distance) AS AverageCommuteDistance
FROM dbo.customer$;





--Sales Analysis---------------------------------------


--What is the total sales by order date?
SELECT OrderDateKey AS OrderDate, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY CONVERT(date, OrderDateKey);



--What is the average order value by order date?
SELECT CONVERT(date, OrderDateKey) AS OrderDate, AVG(ExtendedAmount) AS AverageOrderValue
FROM dbo.internet_sales$
GROUP BY CONVERT(date, OrderDateKey);


--What is the total sales by ship date?
SELECT CONVERT(date, ShipDateKey) AS ShipDate, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY CONVERT(date, ShipDateKey);


--What is the average order quantity by product?
SELECT ProductKey, AVG(OrderQuantity) AS AverageOrderQuantity
FROM dbo.internet_sales$
GROUP BY ProductKey;


--What is the total sales by promotion?
SELECT PromotionKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY PromotionKey;


--What is the average discount amount per order?
SELECT AVG(DiscountAmount) AS AverageDiscountAmount
FROM dbo.internet_sales$;


--What is the total sales by currency?
SELECT CurrencyKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY CurrencyKey;


--What is the average unit price by product?
SELECT ProductKey, AVG(UnitPrice) AS AverageUnitPrice
FROM dbo.internet_sales$
GROUP BY ProductKey;


--What is the total sales by employee?
SELECT EmployeeKey, SUM(SalesAmount) AS TotalSales
FROM dbo.internet_sales$
GROUP BY EmployeeKey;


--What is the average sales amount per order?
SELECT AVG(SalesAmount) AS AverageSalesAmount
FROM dbo.internet_sales$;




--Inventory Analysis----------------------------------------------


--What is the total inventory value by product?
SELECT ProductKey, SUM(UnitsBalance * UnitCost) AS TotalInventoryValue
FROM dbo.product_inventory$
GROUP BY ProductKey;


--What is the average inventory turnover ratio?
SELECT AVG(UnitsOut / NULLIF(UnitsBalance, 0)) AS AverageInventoryTurnover
FROM dbo.product_inventory$;



--What is the total cost of goods sold by product?
SELECT ProductKey, SUM(UnitCost * UnitsOut) AS TotalCostOfGoods
FROM dbo.product_inventory$
GROUP BY ProductKey;


--What is the average unit cost by product?
SELECT ProductKey, AVG(UnitCost) AS AverageUnitCost
FROM dbo.product_inventory$
GROUP BY ProductKey;


--What is the total units sold by product?
SELECT ProductKey, SUM(UnitsOut) AS TotalUnitsSold
FROM dbo.product_inventory$
GROUP BY ProductKey;


--What is the average units in inventory by product?
SELECT ProductKey, AVG(UnitsIn) AS AverageUnitsInInventory
FROM dbo.product_inventory$
GROUP BY ProductKey;



--What is the total units received by product?
SELECT ProductKey, SUM(UnitsIn) AS TotalUnitsReceived
FROM dbo.product_inventory$
GROUP BY ProductKey;



--What is the average units balance by product?
SELECT ProductKey, AVG(UnitsBalance) AS AverageUnitsBalance
FROM dbo.product_inventory$
GROUP BY ProductKey;


--What is the total units moved by product?
SELECT ProductKey, SUM(UnitsOut - UnitsIn) AS TotalUnitsMoved
FROM dbo.product_inventory$
GROUP BY ProductKey;