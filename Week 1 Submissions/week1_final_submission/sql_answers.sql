-- Active: 1787201921682@@127.0.0.1@5432@learning_store
# 1. All Customers
SELECT * FROM customers;

# 2. All active products
SELECT * FROM products WHERE is_active = TRUE;

# 3. Orders with customer names
SELECT o.id, o.customer_id,c.full_name,o.order_status,o.ordered_at FROM orders AS o JOIN customers AS c ON o.customer_id = c.id;

# 4. Order items with product names.
SELECT p.name, oi.quantity, oi.id, oi.order_id, oi.product_id, oi.quantity, oi.unit_price FROM products AS p JOIN order_items AS oi ON p.id = oi.product_id;

# 5. Total amount for each order
SELECT order_id,SUM(quantity*unit_price) FROM order_items GROUP BY order_id;

# 6. Revenue per customer
SELECT c.id, c.full_name, SUM(order_total) AS total_revenue 
FROM customers AS c JOIN (
    SELECT o.id,o.customer_id,ot.order_total AS order_total 
    FROM (
        SELECT order_id,SUM(quantity*unit_price) AS order_total 
        FROM order_items 
        GROUP BY order_id
    ) AS ot JOIN orders AS o ON ot.order_id = o.id
) AS ot ON c.id = ot.customer_id GROUP BY c.id,c.full_name;

#7. Top 3 products by quantity sold
SELECT * FROM products WHERE id in (
    SELECT product_id FROM order_items GROUP BY product_id ORDER BY COUNT(id) DESC LIMIT 3

);

# 8. Customers with no orders
SELECT * FROM customers WHERE id NOT IN (
    SELECT DISTINCT customer_id FROM orders
)