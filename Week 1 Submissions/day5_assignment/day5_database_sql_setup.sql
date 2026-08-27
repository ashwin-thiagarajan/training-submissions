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
