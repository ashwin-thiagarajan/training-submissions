def calculate_discounted_price(price, discount_percent):
    return price*(100-discount_percent)/100

def is_valid_stock(stock):
    return True if stock >= 0 else False


def calculate_order_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total

def get_products_by_category(products, category):
    return [product for product in products if product['category'] == category]

def main():
    print(calculate_discounted_price(100, 15))
    print(is_valid_stock(5))
    print(is_valid_stock(-1))
    print(calculate_order_total([
        {'price': 10, 'quantity':3},
        {'price': 20, 'quantity':2},
        {'price':40, 'quantity':4}
    ]))
    print(get_products_by_category([
        {'product_id': 1, 'category': 'Odd'},
        {'product_id': 2, 'category': 'Even'},
        {'product_id': 3, 'category': 'Odd'}
    ],'Odd'))

if __name__ == "__main__":
    main()