class StockValueError(Exception):
    pass

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity, action = 'Sell'):
        if action == 'Sell':
            if self.stock - quantity >= 0:
                self.stock -= quantity
                return True
            else:
                print('Insufficient stock')
                raise StockValueError
        else:
            if self.stock + quantity <= 0:
                print('Stock overflow')
                raise StockValueError
            else:
                self.stock += quantity
                return True

    def __str__(self):
        return f'{self.name} - ${self.price} - Stock: {self.stock}'

def write_inventory_file(products):
    with open('inventory.txt','w',encoding='utf=8') as file:
        lines = ['Name - Price - Stock\n',
                 *[str(product)+'\n' for product in products]
                ]
        file.writelines(lines)
    print('wrote file')

def main():
    products = [
        Product('Laptop', 1200, 10),
        Product('Smartphone', 800,4),
        Product('Tablet', 500,2)
    ]
    products[0].update_stock(3,'Sell')
    try:
        products[2].update_stock(3,"Buy")
    except StockValueError as e:
        print(e)
    write_inventory_file(products)


if __name__ == "__main__":
    main()
