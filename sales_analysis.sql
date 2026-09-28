USE e_commerce_sales_data_analysis;

SELECT * FROM cleaned_sales

SELECT COUNT(*) AS total_rows
FROM cleaned_sales;

SHOW COLUMNS FROM cleaned_sales;

SELECT SUM(sales) AS total_sales
FROM cleaned_sales;

SELECT COUNT(DISTINCT CustomerID) AS total_customers
FROM cleaned_sales;

DESCRIBE cleaned_sales;

SELECT COUNT(DISTINCT Customer ID) AS total_customers
FROM cleaned_sales;

SELECT COUNT(DISTINCT 'Customer ID')
FROM cleaned_sales;

SELECT COUNT(DISTINCT 'Order ID') 
FROM cleaned_sales;

SELECT
    category,
    SUM(sales) AS total_sales
FROM cleaned_sales
GROUP BY category
ORDER BY total_sales DESC;

SELECT
    region,
    SUM(sales) AS total_sales
FROM cleaned_sales
GROUP BY region
ORDER BY total_sales DESC;

SELECT
    Segment,
    COUNT(DISTINCT `Customer ID`) AS customers,
    SUM(Sales) AS total_sales
FROM cleaned_sales
GROUP BY Segment
ORDER BY total_sales DESC;

SELECT
    segment,
    COUNT(DISTINCT 'Customer ID') AS customers,
    SUM(Sales) AS total_sales,
   
FROM cleaned_sales
GROUP BY segment
ORDER BY total_sales DESC;

SELECT
    *
FROM cleaned_sales
WHERE category = 'Furniture';

USE e_commerce_sales_data_analysis;

SELECT AVG(Sales) AS average_sales
FROM cleaned_sales;

SELECT
    'Order ID',
    'Product',
    Sales
FROM cleaned_sales
WHERE Sales > (
    SELECT AVG(Sales)
    FROM cleaned_sales
)
ORDER BY Sales DESC;

CREATE TABLE Customers AS
SELECT DISTINCT
    'Customer ID',
    'Customer Name',
    Segment,
    Country,
    City,
    State,
    'Postal Code',
    Region
FROM cleaned_sales;

SELECT *
FROM customers
LIMIT 10;

SELECT COUNT(DISTINCT 'Customer ID') AS total_customers
FROM cleaned_sales;

SELECT
    s.`Order ID`,
    s.`Customer ID`,
    c.`Customer Name`,
    c.`Segment`,
    s.`Sales`
FROM cleaned_sales AS s
INNER JOIN Customers AS c
    ON s.`Customer ID` = c.`Customer ID`
LIMIT 20;

SELECT
    c.`Customer ID`,
    c.`Customer Name`,
    c.`Segment`,
    SUM(s.`Sales`) AS total_sales
FROM cleaned_sales AS s
INNER JOIN Customers AS c
    ON s.`Customer ID` = c.`Customer ID`
GROUP BY
    c.`Customer ID`,
    c.`Customer Name`,
    c.`Segment`
ORDER BY total_sales DESC
LIMIT 10;

SELECT
    s.`Order ID`,
    s.`Customer ID`,
    c.`Customer Name`,
    s.Sales
FROM cleaned_sales AS s
LEFT JOIN Customers AS c
    ON s.`Customer ID` = c.`Customer ID`
LIMIT 20;

SELECT
    c.`Segment`,
    s.`Category`,
    SUM(s.`Sales`) AS total_sales
FROM cleaned_sales AS s
INNER JOIN Customers AS c
    ON s.`Customer ID` = c.`Customer ID`
GROUP BY
    c.`Segment`,
    s.`Category`
ORDER BY total_sales DESC;

SELECT
    c.`Region`,
    c.`Segment`,
    COUNT(DISTINCT c.`Customer ID`) AS customers,
    SUM(s.`Sales`) AS total_sales
FROM cleaned_sales AS s
INNER JOIN Customers AS c
    ON s.`Customer ID` = c.`Customer ID`
GROUP BY
    c.`Region`,
    c.`Segment`
ORDER BY
    c.`Region`,
    total_sales DESC;
    
SELECT ROUND(SUM(sales), 2) AS total_sales
FROM cleaned_sales;

SELECT COUNT(DISTINCT `Order ID`) AS total_orders
FROM cleaned_sales;

SELECT COUNT(DISTINCT `Customer ID`) AS total_customers
FROM cleaned_sales;