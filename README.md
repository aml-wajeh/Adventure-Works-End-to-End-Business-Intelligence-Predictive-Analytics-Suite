# Adventure Works: End-to-End Business Intelligence & Predictive Analytics Suite

## 📌 Project Overview
This project transforms raw, fragmented retail data from the Microsoft Adventure Works ecosystem into a strategic analytical asset. It addresses the business challenge of siloed data across sales, inventory, and customer dimensions, which previously hindered actionable growth strategies and demand forecasting. By implementing a full-cycle data pipeline—spanning advanced SQL schema enhancement, rigorous Python-based statistical validation, and predictive machine learning—this suite provides a unified view of regional performance and customer behavior.

## 🛠 Tech Stack
* **Database Engineering:** SQL Server (Advanced DDL/DML, Schema Design).
* **Data Science & Analytics:** Python (Pandas, NumPy, SciPy).
* **Machine Learning:** Scikit-Learn (Linear Regression, Random Forest, K-Means Clustering).
* **Visualization & BI:** Power BI, Plotly, Seaborn, Matplotlib.

## ⚙️ Data Pipeline / Life-cycle
1.  **ETL & Schema Enhancement (SQL):** Enriched the existing database by adding 20+ logic-driven calculated metrics directly to the schema. This included business-critical KPIs such as `ProfitMargin`, `InventoryTurnoverRatio`, `ShippingDays`, and `SalaryToBaseRateRatio`.
2.  **Preprocessing & Cleaning (Python):** * Ensured 100% data integrity by handling missing values with appropriate placeholders and removing duplicates across 10+ tables.
    * Applied the **Interquartile Range (IQR)** method to cap outliers and used **Min-Max Scaling** for feature normalization.
3.  **Exploratory Data Analysis (EDA) & Statistics:** * Generated correlation heatmaps to identify primary drivers of sales volume.
    * Conducted **ANOVA** and **T-Tests** to validate business hypotheses regarding product categories and demographics.
4.  **Predictive Modeling:** Deployed a machine learning pipeline to automate business insights, ranging from individual customer tiering to manufacturing optimization.
5.  **Interactive Visualization:** Developed Power BI dashboards to monitor real-time KPIs, including regional sales distribution and employee performance metrics (e.g., tracking **$862.43K** in total salaries for **284** employees).

## 🤖 Machine Learning Implementation

### Sales Forecasting (Linear Regression)
* **Logic:** Predicts `SalesAmount` based on order features (`ProductKey`, `OrderQuantity`, and `UnitPrice`).
* **Evaluation:** Assessed using **Mean Squared Error (MSE)** and **R-squared ($R^2$)** to determine the percentage of variance explained by the model.

### Customer Segmentation (Random Forest)
* **Logic:** A classification model that segments high-value customers using demographics such as `YearlyIncome`, `TotalChildren`, and `CommuteDistance`.
* **Parameters:** Utilized `GridSearchCV` to optimize `n_estimators` and `max_depth`.

### Product Clustering (K-Means)
* **Logic:** Groups products into distinct clusters based on `StandardCost` and `ListPrice` to optimize inventory and manufacturing decisions.
* **Optimization:** Determined the optimal number of clusters ($k=3$) using the **Elbow Method**.

## 📊 Key Findings
* **Demographic Impact:** Validated a strong positive correlation ($p < 0.05$) between customer yearly income and average order value, enabling highly targeted marketing campaigns.
* **Inventory Optimization:** Identified high-turnover products to minimize out-of-stock risks; findings highlighted that the top 10 products drive the majority of total revenue.
* **Operational Insights:** Discovered significant sales distribution gaps across territories via Plotly choropleth maps, pinpointing specific regions for market expansion.

