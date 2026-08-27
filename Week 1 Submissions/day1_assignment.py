
def is_prime(number):
    if number == 2:
        return True
    for i in range(2,number//2):
        if number%i == 0:
            return False
    return True

def reverse_string(text):
    rs = ''
    for i in range(len(text)):
        rs = rs + text[len(text)-i-1]
    return rs

def calculate_cart_total(items):
    return sum(items)

def find_largest(numbers):
    l = numbers[0]
    if len(numbers) == 1:
        return l
    for i in range(1,len(numbers)):
        if l < numbers[i]:
            l = numbers[i]
    return l

def generate_multiplication_table(number):
    tables = []
    for i in range(10):
        tables.append(number*(i+1))
    return tables

if __name__ == "__main__":
    print(is_prime(5))
    print(reverse_string('Apples'))
    print(calculate_cart_total([1,2,3,4,5]))
    print(find_largest([1,5,2,4,3]))
    print(generate_multiplication_table(5))