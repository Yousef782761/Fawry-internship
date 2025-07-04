from datetime import datetime, timedelta

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, count):
        return self.quantity >= count

    def deduct_stock(self, count):
        if not self.is_available(count):
            raise ValueError(f"Not enough stock for {self.name}")
        self.quantity -= count


class ExpirableProduct(Product):
    def __init__(self, name, price, quantity, expiry_date):
        super().__init__(name, price, quantity)
        self.expiry_date = expiry_date

    def is_expired(self):
        return datetime.now() > self.expiry_date

    def is_available(self, count):
        if self.is_expired():
            return False
        return super().is_available(count)


class Cheese(ExpirableProduct):
    def __init__(self, price, quantity, expiry_date):
        super().__init__("Cheese 400g", price, quantity, expiry_date)
        self.weight_kg = 0.4


class Biscuits(ExpirableProduct):
    def __init__(self, price, quantity, expiry_date):
        super().__init__("Biscuits 700g", price, quantity, expiry_date)
        self.weight_kg = 0.7


class TV(Product):
    def __init__(self, price, quantity):
        super().__init__("Television", price, quantity)
        self.weight_kg = 5.0


class ScratchCard(Product):
    def __init__(self, price, quantity):
        super().__init__("Scratch Card", price, quantity)


class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def can_afford(self, total):
        return self.balance >= total

    def deduct(self, amount):
        if not self.can_afford(amount):
            raise ValueError("Insufficient funds")
        self.balance -= amount


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if not product.is_available(quantity):
            if isinstance(product, ExpirableProduct) and product.is_expired():
                raise Exception(f"{product.name} is expired")
            raise Exception(f"Not enough stock for {product.name}")

        if product.name in self.items:
            current_qty = self.items[product.name][1]
            new_qty = current_qty + quantity
            if not product.is_available(new_qty):
                raise Exception(f"Can't add that many units of {product.name}")
            self.items[product.name][1] = new_qty
        else:
            self.items[product.name] = [product, quantity]

    def total_cost(self):
        return sum(product.price * qty for product, qty in self.items.values())

    def calculate_shipping(self):
        shipping_total = 0.0
        for product, quantity in self.items.values():
            if hasattr(product, 'weight_kg'):
                shipping_total += product.weight_kg * quantity * 10  # $10/kg
        return shipping_total

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return len(self.items) == 0


def checkout(customer, cart):
    if cart.is_empty():
        print("Cart is empty. Nothing to checkout.")
        return

    for product, qty in cart.items.values():
        if isinstance(product, ExpirableProduct) and product.is_expired():
            raise Exception(f"{product.name} is expired")
        if not product.is_available(qty):
            raise Exception(f"{product.name} is out of stock")

    subtotal = cart.total_cost()
    shipping = cart.calculate_shipping()
    grand_total = subtotal + shipping

    print("\n--- Receipt ---")
    for product, qty in cart.items.values():
        print(f"{qty}x {product.name} @ {product.price} = {qty * product.price}")
    print(f"Subtotal: {subtotal} EGP")
    print(f"Shipping: {shipping} EGP")
    print(f"Total Due: {grand_total} EGP")

    customer.deduct(grand_total)
    for product, qty in cart.items.values():
        product.deduct_stock(qty)

    cart.clear()
    print(f"Checkout complete. Remaining balance: {customer.balance:.2f} EGP")


if __name__ == "__main__":
    print("Test Case 1: Normal Purchase ")
    try:
        cust1 = Customer("Youssef", 1000)
        cart1 = Cart()

        cheese = Cheese(90, 5, datetime.now() + timedelta(days=10))
        biscuits = Biscuits(120, 2, datetime.now() + timedelta(days=15))
        tv = TV(400, 1)
        card = ScratchCard(20, 10)

        cart1.add(cheese, 2)
        cart1.add(biscuits, 1)
        cart1.add(tv, 1)
        cart1.add(card, 3)

        checkout(cust1, cart1)
    except Exception as e:
        print(f"Error: {e}")

    print("\n Test Case 2: Expired Product")
    try:
        cust2 = Customer("Youssef", 500)
        cart2 = Cart()

        old_cheese = Cheese(85, 5, datetime.now() - timedelta(days=2))
        cart2.add(old_cheese, 1)
    except Exception as e:
        print(f"Expected error: {e}")

    print("\nTest Case 3: Insufficient Stock ")
    try:
        cust3 = Customer("Ali", 800)
        cart3 = Cart()

        limited_tv = TV(500, 1)
        cart3.add(limited_tv, 2)
    except Exception as e:
        print(f"Expected error: {e}")

    print("\n Test Case 4: Insufficient Balance")
    try:
        cust4 = Customer("Mohammed", 100)
        cart4 = Cart()

        tv = TV(300, 2)
        cart4.add(tv, 1)
        checkout(cust4, cart4)
    except Exception as e:
        print(f"Expected error: {e}")

    print("\n Test Case 5: Empty Cart Checkout")
    try:
        cust5 = Customer("saif", 200)
        empty_cart = Cart()
        checkout(cust5, empty_cart)
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n Test Case 6: Add Product Twice and Merge Quantity")
    try:
        cust6 = Customer("Mahmoud", 1000)
        cart6 = Cart()

        biscuits = Biscuits(100, 10, datetime.now() + timedelta(days=20))
        cart6.add(biscuits, 2)
        cart6.add(biscuits, 3)  

        checkout(cust6, cart6)
    except Exception as e:
        print(f"Error: {e}")
