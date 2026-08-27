# Week 1 Final Assignment

## Objective

Test all concepts covered in Week 1: Python basics, advanced Python, NumPy, Pandas, Pydantic, SQL, and basic Python database connectivity.

## Use Case

Build a small learning-store backend foundation using Python, validated data models, SQL, and database connectivity.

## Submission Folder

```text
week1_final_submission/
```

## Part A: Python Functions

Create `python_basics.py` with:

1. `calculate_discounted_price(price, discount_percent)`
2. `is_valid_stock(stock)`
3. `calculate_order_total(items)`
4. `get_products_by_category(products, category)`

## Part B: OOP and File Handling

Create `inventory.py` with:

1. A `Product` class.
2. A method to update stock.
3. Exception handling for invalid stock updates.
4. A function that writes inventory summary to a text file.

## Part C: NumPy and Pandas

Create `sales_analysis.py` with:

1. NumPy calculation for average, minimum, and maximum sales.
2. Pandas DataFrame for product sales.
3. Filter high-selling products.
4. Group revenue by region.

## Part D: Pydantic

Create `schemas.py` with:

1. `CustomerSchema`
2. `ProductSchema`
3. `OrderItemSchema`
4. `OrderSchema`

Include valid and invalid test data.

## Part E: SQL

Create `sql_answers.sql` with queries for:

1. All customers.
2. Active products.
3. Orders with customer names.
4. Order items with product names.
5. Total amount for each order.
6. Revenue per customer.
7. Top 3 products by quantity sold.
8. Customers with no orders.

## Part F: Python Database Connectivity

Create either:

```text
mysql_connection_task.py
```

or:

```text
postgres_connection_task.py
```

The script should:

1. Connect using environment variables.
2. Fetch all customers.
3. Fetch order totals.
4. Use parameterized queries for at least one filtered query.
5. Close the database connection cleanly.

## Evaluation Criteria

| Area | Weight |
| --- | ---: |
| Python basics | 15% |
| OOP, exceptions, and files | 15% |
| NumPy and Pandas | 10% |
| Pydantic validation | 15% |
| SQL queries | 25% |
| Python DB connectivity | 20% |

## Note

Django ORM is not part of the Week 1 final assignment. It should be handled in Week 2 after direct SQL and database fundamentals are clear.

