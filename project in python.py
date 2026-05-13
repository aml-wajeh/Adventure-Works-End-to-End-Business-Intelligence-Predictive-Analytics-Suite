import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import matplotlib.pyplot as plt

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Load all tables into DataFrames
dim_geography = pd.read_csv('geography.csv')
fact_product_inventory = pd.read_csv('product_inventory.csv')
dim_product_category = pd.read_csv('product_category.csv')
dim_product_subcategory = pd.read_csv('product_subcategory.csv')
dim_promotion = pd.read_csv('promotion.csv')
dim_employee = pd.read_csv('employee.csv')
dim_reseller = pd.read_csv('reseller.csv')
dim_product = pd.read_csv('product.csv')
fact_internet_sales = pd.read_csv('internet_sales.csv')
dim_sales_territory = pd.read_csv('sales_territory.csv')
fact_reseller_sales = pd.read_csv('reseller_sales.csv')
dim_date = pd.read_csv('date.csv')
dim_currency = pd.read_csv('currency.csv')
dim_customer = pd.read_csv('customer.csv')



# List of all tables
tables = {
    "dim_geography": dim_geography,
    "fact_product_inventory": fact_product_inventory,
    "dim_product_category": dim_product_category,
    "dim_product_subcategory": dim_product_subcategory,
    "dim_promotion": dim_promotion,
    "dim_employee": dim_employee,
    "dim_reseller": dim_reseller,
    "dim_product": dim_product,
    "fact_internet_sales": fact_internet_sales,
    "dim_sales_territory": dim_sales_territory,
    "fact_reseller_sales": fact_reseller_sales,
    "dim_date": dim_date,
    "dim_currency": dim_currency,
    "dim_customer": dim_customer
}



# Cleaning Step ----------------------

# Convert Date columns to datetime
fact_product_inventory['MovementDate'] = pd.to_datetime(fact_product_inventory['MovementDate'])
dim_promotion['StartDate'] = pd.to_datetime(dim_promotion['StartDate'])
dim_promotion['EndDate'] = pd.to_datetime(dim_promotion['EndDate'])
dim_employee['HireDate'] = pd.to_datetime(dim_employee['HireDate'])
dim_employee['BirthDate'] = pd.to_datetime(dim_employee['BirthDate'])
dim_employee['StartDate'] = pd.to_datetime(dim_employee['StartDate'])
dim_product['StartDate'] = pd.to_datetime(dim_product['StartDate'])
fact_internet_sales['OrderDate'] = pd.to_datetime(fact_internet_sales['OrderDate'])
fact_internet_sales['DueDate'] = pd.to_datetime(fact_internet_sales['DueDate'])
fact_internet_sales['ShipDate'] = pd.to_datetime(fact_internet_sales['ShipDate'])
fact_reseller_sales['OrderDate'] = pd.to_datetime(fact_reseller_sales['OrderDate'])
fact_reseller_sales['DueDate'] = pd.to_datetime(fact_reseller_sales['DueDate'])
fact_reseller_sales['ShipDate'] = pd.to_datetime(fact_reseller_sales['ShipDate'])
dim_date['FullDateAlternateKey'] = pd.to_datetime(dim_date['FullDateAlternateKey'])


#  Remove Duplicates
dim_geography = dim_geography.drop_duplicates()
fact_product_inventory = fact_product_inventory.drop_duplicates()
dim_product_category = dim_product_category.drop_duplicates()
dim_product_subcategory = dim_product_subcategory.drop_duplicates()
dim_promotion = dim_promotion.drop_duplicates()
dim_employee = dim_employee.drop_duplicates()
dim_reseller = dim_reseller.drop_duplicates()
dim_product = dim_product.drop_duplicates()
fact_internet_sales = fact_internet_sales.drop_duplicates()
dim_sales_territory = dim_sales_territory.drop_duplicates()
fact_reseller_sales = fact_reseller_sales.drop_duplicates()
dim_date = dim_date.drop_duplicates()
dim_currency = dim_currency.drop_duplicates()
dim_customer = dim_customer.drop_duplicates()


#  Replace Missing Values
dim_geography.fillna({'City': 'Unknown', 'StateProvinceCode': 'Unknown', 'StateProvinceName': 'Unknown', 'CountryRegionCode': 'Unknown', 'EnglishCountryRegionName': 'Unknown', 'PostalCode': 'Unknown', 'SalesTerritoryKey': 0, 'IpAddressLocator': 'Unknown'}, inplace=True)
fact_product_inventory.fillna({'UnitsIn': 0, 'UnitsOut': 0, 'UnitsBalance': 0}, inplace=True)
dim_product_category.fillna({'EnglishProductCategoryName': 'Unknown'}, inplace=True)
dim_product_subcategory.fillna({'EnglishProductSubcategoryName': 'Unknown'}, inplace=True)
dim_promotion.fillna({'DiscountPct': 0, 'EnglishPromotionType': 'Unknown', 'EnglishPromotionCategory': 'Unknown', 'MinQty': 0, 'MaxQty': 0}, inplace=True)
dim_employee.fillna({'MiddleName': 'Unknown', 'Title': 'Unknown', 'LoginID': 'Unknown', 'EmailAddress': 'Unknown', 'Phone': 'Unknown', 'MaritalStatus': 'Unknown', 'EmergencyContactName': 'Unknown', 'EmergencyContactPhone': 'Unknown', 'SalariedFlag': 'Unknown', 'Gender': 'Unknown', 'PayFrequency': 0, 'BaseRate': 0, 'VacationHours': 0, 'SickLeaveHours': 0, 'SalesPersonFlag': 'Unknown', 'DepartmentName': 'Unknown', 'EndDate': 'Unknown'}, inplace=True)
dim_reseller.fillna({'Phone': 'Unknown', 'BusinessType': 'Unknown', 'ResellerName': 'Unknown', 'NumberEmployees': 0, 'OrderFrequency': 'Unknown', 'OrderMonth': 0, 'FirstOrderYear': 0, 'LastOrderYear': 0, 'ProductLine': 'Unknown', 'AddressLine1': 'Unknown', 'AddressLine2': 'Unknown', 'AnnualSales': 0, 'BankName': 'Unknown', 'MinPaymentType': 0, 'MinPaymentAmount': 'Unknown', 'AnnualRevenue': 0, 'YearOpened': 0, 'Status': 'Unknown'}, inplace=True)
dim_product.fillna({'WeightUnitMeasureCode': 'Unknown', 'SizeUnitMeasureCode': 'Unknown', 'EnglishProductName': 'Unknown', 'StandardCost': 0, 'FinishedGoodsFlag': 'Unknown', 'Color': 'Unknown', 'SafetyStockLevel': 0, 'ReorderPoint': 0, 'ListPrice': 0, 'Size': 'Unknown', 'SizeRange': 'Unknown', 'Weight': 'Unknown', 'DaysToManufacture': 0, 'ProductLine': 'Unknown', 'DealerPrice': 0, 'Class': 'Unknown', 'Style': 'Unknown', 'ModelName': 'Unknown', 'EndDate': 'Unknown', 'Status': 'Unknown'}, inplace=True)
fact_internet_sales.fillna({'UnitPriceDiscountPct': 0, 'DiscountAmount': 0}, inplace=True)
dim_sales_territory.fillna({'SalesTerritoryRegion': 'Unknown', 'SalesTerritoryCountry': 'Unknown', 'SalesTerritoryGroup': 'Unknown'}, inplace=True)
fact_reseller_sales.fillna({'UnitPriceDiscountPct': 0, 'DiscountAmount': 0}, inplace=True)
dim_date.fillna({'EnglishDayNameOfWeek': 'Unknown', 'EnglishMonthName': 'Unknown'}, inplace=True)
dim_currency.fillna({'CurrencyName': 'Unknown'}, inplace=True)
dim_customer.fillna({'MiddleName': 'Unknown', 'BirthDate': 'Unknown', 'MaritalStatus': 'Unknown', 'Gender': 'Unknown', 'EmailAddress': 'Unknown', 'YearlyIncome': 0, 'TotalChildren': 0, 'NumberChildrenAtHome': 0, 'EnglishEducation': 'Unknown', 'EnglishOccupation': 'Unknown', 'HouseOwnerFlag': 0, 'NumberCarsOwned': 0, 'AddressLine1': 'Unknown', 'AddressLine2': 'Unknown', 'Phone': 'Unknown', 'DateFirstPurchase': 'Unknown', 'CommuteDistance': 'Unknown'}, inplace=True)


# handle outliers using IQR
def handle_outliers(df, numerical_columns):
    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    return df

# encode categorical variables
def encode_categorical(df):
    label_encoder = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = label_encoder.fit_transform(df[col])
    return df

# normalize numerical data
def normalize_data(df, numerical_columns):
    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    return df


# check and clean data types
def clean_data_types(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
    return df

# Function to perform all cleaning steps
def clean_table(df, adventure_works):
    print(f"Cleaning {adventure_works}...")
    
    # Step 1: Standardize column names
    df = standardize_column_names(df)
    
    # Step 2: Convert date columns to datetime
    df = convert_dates(df)
    
    # Step 3: Remove duplicates
    df = remove_duplicates(df)
    
    # Step 4: Handle missing values
    df = handle_missing_values(df)
    
    # Step 5: Clean data types
    df = clean_data_types(df)
    
    # Step 6: Handle outliers (for numerical columns)
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numerical_columns) > 0:
        df = handle_outliers(df, numerical_columns)
    
    # Step 7: Encode categorical variables
    df = encode_categorical(df)
    
    # Step 8: Normalize numerical data
    if len(numerical_columns) > 0:
        df = normalize_data(df, numerical_columns)
    
    # Step 9: Feature engineering (example: create net_units for inventory)
    if adventure_works == "fact_product_inventory":
        df['net_units'] = df['unitsin'] - df['unitsout']
    
    # Step 10: Final data check
    print(f"Missing values in {adventure_works}:")
    print(df.isnull().sum())
    print(f"Data types in {adventure_works}:")
    print(df.dtypes)
    
    return df

# Apply cleaning steps to all tables
cleaned_tables = {}
for adventure_works, df in tables.items():
    cleaned_tables[adventure_works] = clean_table(df, adventure_works)

# Save cleaned tables to CSV (optional)
for adventure_works, df in cleaned_tables.items():
    df.to_csv(f'cleaned_{adventure_works}.csv', index=False)

print("All tables cleaned and saved successfully!")



#Data Exploration---------------------------

# Descriptive statistics for numerical columns
print(sales_data.describe())

# Descriptive statistics for categorical columns
print(sales_data.describe(include=['object']))

#Inferential Statistics
# Correlation matrix
corr_matrix = sales_data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

#Hypothesis Testing

#Hypothesis 1: Is there a significant difference in sales amount between different product categories?
# ANOVA test
categories = sales_data['englishproductcategoryname'].unique()
category_sales = [sales_data[sales_data['englishproductcategoryname'] == category]['salesamount'] for category in categories]
f_stat, p_value = stats.f_oneway(*category_sales)
print(f"F-statistic: {f_stat}, p-value: {p_value}")

#Hypothesis 2: Is there a significant relationship between customer yearly income and sales amount?
# Pearson correlation test
corr, p_value = stats.pearsonr(sales_data['yearlyincome'], sales_data['salesamount'])
print(f"Correlation: {corr}, p-value: {p_value}")

#Hypothesis 3: Is there a significant difference in sales amount between different genders?
# T-test
male_sales = sales_data[sales_data['gender'] == 'M']['salesamount']
female_sales = sales_data[sales_data['gender'] == 'F']['salesamount']
t_stat, p_value = stats.ttest_ind(male_sales, female_sales)
print(f"T-statistic: {t_stat}, p-value: {p_value}")

#Hypothesis 4: Is there a significant difference in sales amount between different marital statuses?
# T-test
single_sales = sales_data[sales_data['maritalstatus'] == 'S']['salesamount']
married_sales = sales_data[sales_data['maritalstatus'] == 'M']['salesamount']
t_stat, p_value = stats.ttest_ind(single_sales, married_sales)
print(f"T-statistic: {t_stat}, p-value: {p_value}")

#Hypothesis 5: Is there a significant difference in sales amount between different education levels?
# ANOVA test
education_levels = sales_data['englisheducation'].unique()
education_sales = [sales_data[sales_data['englisheducation'] == level]['salesamount'] for level in education_levels]
f_stat, p_value = stats.f_oneway(*education_sales)
print(f"F-statistic: {f_stat}, p-value: {p_value}")



#Machine Learning Models------------------------------------


#1. Linear Regression for Sales Prediction
#Objective:
#Predict the SalesAmount in the FactInternetSales or FactResellerSales tables based on features like ProductKey, CustomerKey, PromotionKey, and OrderQuantity.

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Prepare data for sales prediction
sales_data = cleaned_tables['fact_internet_sales']
X = sales_data[['productkey', 'customerkey', 'promotionkey', 'orderquantity']]
y = sales_data['salesamount']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Feature importance (coefficients)
coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})
print(coefficients)


#2. Random Forest for Customer Segmentation
#Objective:
#Segment customers based on features like YearlyIncome, TotalChildren, NumberCarsOwned, and CommuteDistance to identify high-value customers.

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Prepare data for customer segmentation
customer_data = cleaned_tables['dim_customer']
X = customer_data[['yearlyincome', 'totalchildren', 'numbercarsowned', 'commutedistance']]
y = customer_data['houseownerflag']  # Target variable (e.g., house ownership)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
print(feature_importances.sort_values(by='Importance', ascending=False))



#3. K-Means Clustering for Product Categorization
#Objective:
#Cluster products into categories based on features like StandardCost, ListPrice, SafetyStockLevel, and DaysToManufacture.

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Prepare data for product clustering
product_data = cleaned_tables['dim_product']
X = product_data[['standardcost', 'listprice', 'safetystocklevel', 'daystomanufacture']]

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine the optimal number of clusters using the Elbow Method
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Method
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.show()

# Apply K-Means with the optimal k (e.g., k=3)
kmeans = KMeans(n_clusters=3, random_state=42)
product_data['cluster'] = kmeans.fit_predict(X_scaled)

# Visualize the clusters
plt.figure(figsize=(8, 5))
plt.scatter(product_data['standardcost'], product_data['listprice'], c=product_data['cluster'], cmap='viridis')
plt.title('Product Clusters')
plt.xlabel('Standard Cost')
plt.ylabel('List Price')
plt.colorbar(label='Cluster')
plt.show()

# Analyze cluster characteristics
print(product_data.groupby('cluster').mean())


#Hyperparameter Tuning:
#Use GridSearchCV or RandomizedSearchCV to optimize model parameters.

from sklearn.model_selection import GridSearchCV
param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]}
grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)


#Model Deployment:
#Save the trained models using joblib or pickle for deployment.

import joblib
joblib.dump(model, 'sales_prediction_model.pkl')


# Visualizations----------------------------------------

#1. Descriptive Statistics Charts

#1.1 Bar Chart: Total Sales by Product Category
# Group by product category and sum sales
sales_by_category = cleaned_tables['fact_internet_sales'].groupby('productkey')['salesamount'].sum().reset_index()
sales_by_category = sales_by_category.merge(cleaned_tables['dim_product'], on='productkey')

plt.figure(figsize=(10, 6))
sns.barplot(x='englishproductcategoryname', y='salesamount', data=sales_by_category)
plt.title('Total Sales by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.show()


#1.2 Pie Chart: Sales Distribution by Region
sales_by_region = cleaned_tables['fact_internet_sales'].groupby('salesterritorykey')['salesamount'].sum().reset_index()
sales_by_region = sales_by_region.merge(cleaned_tables['dim_sales_territory'], on='salesterritorykey')

plt.figure(figsize=(8, 8))
plt.pie(sales_by_region['salesamount'], labels=sales_by_region['salesterritoryregion'], autopct='%1.1f%%')
plt.title('Sales Distribution by Region')
plt.show()


#1.3 Box Plot: Distribution of Unit Prices
plt.figure(figsize=(10, 6))
sns.boxplot(x=cleaned_tables['fact_internet_sales']['unitprice'])
plt.title('Distribution of Unit Prices')
plt.xlabel('Unit Price')
plt.show()


#1.4 Histogram: Distribution of Order Quantities
plt.figure(figsize=(10, 6))
sns.histplot(cleaned_tables['fact_internet_sales']['orderquantity'], bins=20, kde=True)
plt.title('Distribution of Order Quantities')
plt.xlabel('Order Quantity')
plt.ylabel('Frequency')
plt.show()


#1.5 Heatmap: Correlation Matrix
corr_matrix = cleaned_tables['fact_internet_sales'].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()



#2. Relationship Charts

#2.1 Scatter Plot: Sales Amount vs. Order Quantity
plt.figure(figsize=(10, 6))
sns.scatterplot(x='orderquantity', y='salesamount', data=cleaned_tables['fact_internet_sales'])
plt.title('Sales Amount vs. Order Quantity')
plt.xlabel('Order Quantity')
plt.ylabel('Sales Amount')
plt.show()


#2.2 Line Chart: Monthly Sales Trend
cleaned_tables['fact_internet_sales']['orderdate'] = pd.to_datetime(cleaned_tables['fact_internet_sales']['orderdate'])
monthly_sales = cleaned_tables['fact_internet_sales'].resample('M', on='orderdate')['salesamount'].sum()

plt.figure(figsize=(12, 6))
monthly_sales.plot()
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales Amount')
plt.show()


#2.3 Pair Plot: Relationships Between Numerical Features
sns.pairplot(cleaned_tables['fact_internet_sales'][['orderquantity', 'unitprice', 'salesamount']])
plt.suptitle('Pair Plot of Numerical Features', y=1.02)
plt.show()


#2.4 Bubble Chart: Sales by Product and Region
plt.figure(figsize=(12, 8))
sns.scatterplot(x='productkey', y='salesterritorykey', size='salesamount', data=cleaned_tables['fact_internet_sales'], sizes=(20, 500))
plt.title('Sales by Product and Region')
plt.xlabel('Product Key')
plt.ylabel('Sales Territory Key')
plt.show()


#2.5 Stacked Bar Chart: Sales by Category and Region
sales_by_category_region = cleaned_tables['fact_internet_sales'].groupby(['productkey', 'salesterritorykey'])['salesamount'].sum().reset_index()
sales_by_category_region = sales_by_category_region.merge(cleaned_tables['dim_product'], on='productkey')

plt.figure(figsize=(12, 8))
sns.barplot(x='salesterritorykey', y='salesamount', hue='englishproductcategoryname', data=sales_by_category_region)
plt.title('Sales by Category and Region')
plt.xlabel('Sales Territory Key')
plt.ylabel('Total Sales Amount')
plt.legend(title='Product Category')
plt.show()



#3. Distribution Charts


#3.1 Kernel Density Estimate (KDE) Plot: Distribution of Sales Amount
plt.figure(figsize=(10, 6))
sns.kdeplot(cleaned_tables['fact_internet_sales']['salesamount'], shade=True)
plt.title('Distribution of Sales Amount')
plt.xlabel('Sales Amount')
plt.ylabel('Density')
plt.show()


#3.2 Violin Plot: Distribution of Unit Prices by Product Category
plt.figure(figsize=(12, 8))
sns.violinplot(x='englishproductcategoryname', y='unitprice', data=sales_by_category)
plt.title('Distribution of Unit Prices by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Unit Price')
plt.xticks(rotation=45)
plt.show()


#3.3 ECDF Plot: Cumulative Distribution of Sales Amount
plt.figure(figsize=(10, 6))
sns.ecdfplot(cleaned_tables['fact_internet_sales']['salesamount'])
plt.title('Cumulative Distribution of Sales Amount')
plt.xlabel('Sales Amount')
plt.ylabel('ECDF')
plt.show()


#3.4 Swarm Plot: Distribution of Order Quantities by Region
plt.figure(figsize=(12, 8))
sns.swarmplot(x='salesterritorykey', y='orderquantity', data=cleaned_tables['fact_internet_sales'])
plt.title('Distribution of Order Quantities by Region')
plt.xlabel('Sales Territory Key')
plt.ylabel('Order Quantity')
plt.show()


#3.5 Rug Plot: Distribution of Sales Amount
plt.figure(figsize=(10, 6))
sns.rugplot(cleaned_tables['fact_internet_sales']['salesamount'])
plt.title('Distribution of Sales Amount')
plt.xlabel('Sales Amount')
plt.show()



#4. Trend and Time Series Charts


#4.1 Line Chart: Daily Sales Trend
daily_sales = cleaned_tables['fact_internet_sales'].resample('D', on='orderdate')['salesamount'].sum()

plt.figure(figsize=(12, 6))
daily_sales.plot()
plt.title('Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Total Sales Amount')
plt.show()


#4.2 Area Chart: Cumulative Sales Over Time
cumulative_sales = cleaned_tables['fact_internet_sales'].resample('M', on='orderdate')['salesamount'].sum().cumsum()

plt.figure(figsize=(12, 6))
cumulative_sales.plot(kind='area')
plt.title('Cumulative Sales Over Time')
plt.xlabel('Month')
plt.ylabel('Cumulative Sales Amount')
plt.show()


#4.3 Seasonal Decomposition: Sales Trend
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(monthly_sales, model='additive', period=12)
decomposition.plot()
plt.suptitle('Seasonal Decomposition of Sales Trend', y=1.02)
plt.show()


#4.4 Rolling Mean: Smooth Sales Trend
rolling_mean = monthly_sales.rolling(window=3).mean()

plt.figure(figsize=(12, 6))
rolling_mean.plot()
plt.title('Rolling Mean of Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.show()


#4.5 Lag Plot: Sales Autocorrelation
from pandas.plotting import lag_plot

plt.figure(figsize=(6, 6))
lag_plot(monthly_sales)
plt.title('Lag Plot of Monthly Sales')
plt.show()



#5. Machine Learning Visualization


#5.1 Feature Importance: Random Forest
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importances)
plt.title('Feature Importance (Random Forest)')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()


#5.2 Confusion Matrix: Classification Results
from sklearn.metrics import confusion_matrix

conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()


#5.3 ROC Curve: Classification Performance
from sklearn.metrics import roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()


#5.4 Residual Plot: Linear Regression
residuals = y_test - y_pred

plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_pred, y=residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Residual Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()


#5.5 Cluster Visualization: K-Means
plt.figure(figsize=(10, 6))
sns.scatterplot(x='standardcost', y='listprice', hue='cluster', data=product_data, palette='viridis')
plt.title('Product Clusters')
plt.xlabel('Standard Cost')
plt.ylabel('List Price')
plt.legend(title='Cluster')
plt.show()



#6. More Visualizations


#6.1 Plotly Chart: Sales by Region
import plotly.express as px

fig = px.bar(sales_by_region, x='salesterritoryregion', y='salesamount', title='Sales by Region')
fig.show()


#6.2 3D Scatter Plot: Sales, Quantity, and Price
fig = px.scatter_3d(cleaned_tables['fact_internet_sales'], x='orderquantity', y='unitprice', z='salesamount', color='productkey')
fig.update_layout(title='3D Scatter Plot: Sales, Quantity, and Price')
fig.show()


#6.3 Sunburst Chart: Sales Hierarchy
fig = px.sunburst(sales_by_category_region, path=['salesterritoryregion', 'englishproductcategoryname'], values='salesamount')
fig.update_layout(title='Sales Hierarchy')
fig.show()


#6.4 Choropleth Map: Sales by Country
fig = px.choropleth(sales_by_region, locations='salesterritorycountry', locationmode='country names', color='salesamount')
fig.update_layout(title='Sales by Country')
fig.show()


#6.5 Animated Line Chart: Sales Over Time
fig = px.line(monthly_sales.reset_index(), x='orderdate', y='salesamount', title='Monthly Sales Trend')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='Sales Amount')
fig.show()