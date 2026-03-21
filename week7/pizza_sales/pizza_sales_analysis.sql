SELECT 
SUM(total_price) AS total_revenue
FROM pizza_sale;

SELECT 
SUM(total_price) / COUNT(DISTINCT order_id) AS avg_order_value
FROM pizza_sale;

SELECT 
SUM(quantity) AS total_pizzas_sold
FROM pizza_sale;

SELECT 
COUNT(DISTINCT order_id) AS total_orders
FROM pizza_sale;

SELECT 
SUM(quantity) / COUNT(DISTINCT order_id) AS avg_pizzas_per_order
FROM pizza_sale;

SELECT 
DAYNAME(order_date) AS DAY_NAME,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sale
GROUP BY DAYNAME(order_date)
ORDER BY TOTAL_ORDERS DESC;


SELECT 
MONTHNAME(order_date) AS MONTH_NAME,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sale
GROUP BY
MONTH(order_date),
MONTHNAME(order_date)
ORDER BY TOTAL_ORDERS DESC;

SELECT 
pizza_category,
SUM(total_price) AS TOTAL_SALES,
SUM(total_price) * 100.0 / 
(SELECT SUM(total_price) FROM pizza_sale) AS PERCENTAGE_SALES
FROM pizza_sale
GROUP BY pizza_category
ORDER BY PERCENTAGE_SALES DESC;

SELECT 
pizza_size,
SUM(total_price) AS TOTAL_SALES,
SUM(total_price) * 100.0 / 
(SELECT SUM(total_price) FROM pizza_sale) AS PERCENTAGE_SALES
FROM pizza_sale
GROUP BY pizza_size
ORDER BY PERCENTAGE_SALES DESC;

SELECT 
pizza_category,
SUM(quantity) AS TOTAL_PIZZAS_SOLD
FROM pizza_sale
GROUP BY pizza_category
ORDER BY TOTAL_PIZZAS_SOLD DESC;

SELECT 
pizza_name,
SUM(total_price) AS TOTAL_REVENUE
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_REVENUE DESC
LIMIT 5;

SELECT 
pizza_name,
SUM(quantity) AS TOTAL_QUANTITY
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_QUANTITY DESC
LIMIT 5;

SELECT 
pizza_name,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_ORDERS DESC
LIMIT 5;

SELECT 
pizza_name,
SUM(total_price) AS TOTAL_REVENUE
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_REVENUE ASC
LIMIT 5;

SELECT 
pizza_name,
SUM(quantity) AS TOTAL_QUANTITY
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_QUANTITY ASC
LIMIT 5;

SELECT 
pizza_name,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sale
GROUP BY pizza_name
ORDER BY TOTAL_ORDERS ASC
LIMIT 5;