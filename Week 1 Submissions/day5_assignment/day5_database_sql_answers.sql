# SETUP ++++++++++++++++++++++++++++
DROP TABLE order_items;
DROP TABLE orders;
DROP TABLE products;
DROP TABLE customers;
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Stock INT NOT NULL
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Email VARCHAR(150) NOT NULL UNIQUE,
    RegistrationDate DATE NOT NULL
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE ProductReviews (
    ReviewID INT PRIMARY KEY,
    ProductID INT NOT NULL,
    CustomerID INT NOT NULL,
    Rating INT NOT NULL,
    Review VARCHAR(500),
    ReviewDate DATE NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    CHECK (Rating BETWEEN 1 AND 5)
);

INSERT INTO Products (ProductID, ProductName, Category, Price, Stock) VALUES
    (101, 'Leather Recliner', 'Recliners', 500, 50),
    (102, 'Fabric Recliner', 'Recliners', 400, 30),
    (103, 'Sectional Sofa', 'Sofas', 700, 20),
    (104, 'Sleeper Sofa', 'Sofas', 650, 15);

INSERT INTO Customers (CustomerID, CustomerName, Country, Email, RegistrationDate) VALUES
    (1, 'John Doe', 'USA', 'john.doe@example.com', '2022-01-15'),
    (2, 'Jane Smith', 'UK', 'jane.smith@example.com', '2022-03-10'),
    (3, 'Robert Brown', 'Canada', 'robert.b@example.com', '2023-06-25');

INSERT INTO Orders (OrderID, CustomerID, ProductID, Quantity, OrderDate, TotalAmount, Region) VALUES
    (201, 1, 101, 2, '2023-12-20', 1000, 'North America'),
    (202, 2, 103, 1, '2023-12-22', 700, 'Europe'),
    (203, 3, 104, 1, '2024-01-15', 650, 'North America');

INSERT INTO ProductReviews (ReviewID, ProductID, CustomerID, Rating, Review, ReviewDate) VALUES
    (301, 101, 1, 5, 'Excellent quality!', '2023-12-25'),
    (302, 103, 2, 4, 'Comfortable and stylish.', '2023-12-26'),
    (303, 104, 3, 3, 'Not as durable as expected.', '2024-01-16');

# Answers =======================================================
# 1. Product Sales by Region
WITH ProductSales AS (
    SELECT 
        o.region, 
        p.productid, 
        p.productname, 
        SUM(o.quantity) AS total_quantity_sold
    FROM orders AS o 
    JOIN products AS p 
        ON o.productid = p.productid
    GROUP BY o.region, p.productid, p.productname
),
MaxRegionSales AS (
    SELECT 
        region, 
        MAX(total_quantity_sold) AS max_sold
    FROM ProductSales
    GROUP BY region
)
SELECT 
    ps.region, 
    ps.productid, 
    ps.productname, 
    ps.total_quantity_sold
FROM ProductSales ps
JOIN MaxRegionSales mrs 
    ON ps.region = mrs.region
    AND ps.total_quantity_sold = mrs.max_sold;

# 2. Highly Rated Products by Region
WITH ProductRegionalRating AS (
    SELECT o.region,pr.productid, AVG(pr.rating) AS avg_rating from productreviews as pr JOIN orders as o ON pr.productid = o.productid GROUP BY o.region, pr.productid
)
SELECT prr.region AS Region, prr.productid AS ProductID, p.productname AS ProductName, prr.avg_rating AS AverageRating FROM ProductRegionalRating AS prr JOIN products AS p ON p.productid = prr.productid WHERE prr.avg_rating >= 4;

# 3. Top Rated Prodcuts Globally
SELECT p.productid AS ProductID, p.productname AS ProductName, AVG(pr.rating) AS AverageRating, COUNT(pr.rating) AS ReviewCount FROM products as p JOIN productreviews as pr ON p.productid = pr.productid GROUP BY p.productid ORDER BY AVG(pr.rating) DESC, COUNT(pr.rating) DESC;

# 4. Revenue by Region
SELECT o.region AS Region, SUM(o.quantity * p.price) AS TotalRevenue FROM orders AS o JOIN products AS p ON o.productid = p.productid GROUP BY o.region;

# 5. Customers With Reviews
SELECT c.customerid AS CustomerID, c.customername AS CustomerName, ppr.productname AS ProductName, ppr.rating AS Rating,ppr.reviewdate AS ReviewDate FROM customers AS c JOIN (
    SELECT pr.customerid, pr.rating, pr.reviewdate,p.productname FROM productreviews AS pr JOIN products AS p ON pr.productid = p.productid
) AS ppr ON c.customerid = ppr.customerid;

# 6. Products Never Ordered
SELECT p.productid AS ProductID, p.productname AS ProductName, p.category AS Category FROM products AS p WHERE p.productid NOT IN (
    SELECT DISTINCT productid FROM orders
);
