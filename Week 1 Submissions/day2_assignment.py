# # Day 2 Assignment: Python Advanced

# ## Submission File

# ```text
# day2_assignment.py
# ```

# ## Tasks

# 1. Create a `Product` class with `product_id`, `name`, `category`, `price`, and `stock`.
# 2. Add a method `sell(quantity)` that reduces stock.
# 3. Raise a custom exception if requested quantity is greater than stock.
# 4. Given a list of product dictionaries, return products grouped by category.
# 5. Read a CSV-like text file and calculate total stock value.

# ## Evaluation

# - Correct OOP usage.
# - Clear exception handling.
# - Correct dictionary/list operations.
# - Proper file handling using `with open(...)`.

class NotEnoughStockError(Exception):
    pass

class Product:
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        try:
            if self.stock < quantity:
                raise NotEnoughStockError
            self.stock = self.stock - quantity
        except NotEnoughStockError as e:
            print('Not enough stock.')

def group_products_by_category(products):
    grouped_products = {}
    for p in products:
        if p.category in grouped_products:
            grouped_products[p.category].append({
                "product_id" : p.product_id,
                "name" : p.name,
                "price" : p.price,
                "stock" : p.stock
            })
        else:
            grouped_products[p.category] = [{
                "product_id" : p.product_id,
                "name" : p.name,
                "price" : p.price,
                "stock" : p.stock
            }]
    return grouped_products


if __name__ == "__main__":
    sample_products = [
        Product(1,"Leather Recliner", "Recliners",30,3),
        Product(2,"Fabric Recliner","Recliners",20,5),
        Product(3,"Sectional Sofa","Sofas",50,2)
    ]

    print(sample_products[0].sell(2))
    print(sample_products[0].sell(4))
    print(group_products_by_category(sample_products))
