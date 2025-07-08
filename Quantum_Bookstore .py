class Book:
    def __init__(self, isbn, title, year, price):
        self.isbn = isbn
        self.title = title
        self.year = year
        self.price = price
        self.book_type = " "
    
    def get_info(self):
        return f"{self.title} ({self.year}) --> ISBN: {self.isbn}"

class PaperBook(Book):
    def __init__(self, isbn, title, year, price, stock):
        super().__init__(isbn, title, year, price)
        self.stock = stock
        self.book_type = "paper"
    
    def can_buy(self, quantity):
        if self.stock >= quantity:
            return True
        else:
            return False
    
    def reduce_stock(self, quantity):
        self.stock = self.stock - quantity

class EBook(Book):
    def __init__(self, isbn, title, year, price, file_type):
        super().__init__(isbn, title, year, price)
        self.file_type = file_type
        self.book_type = "ebook"
    
    def can_buy(self, quantity):
        return True

class ShowcaseBook(Book):
    def __init__(self, isbn, title, year, price):
        super().__init__(isbn, title, year, price)
        self.book_type = "showcase"
    
    def can_buy(self, quantity):
        return False

class BookStore:
    def __init__(self):
        self.books = []
        self.shipping_service = None
        self.email_service = None
    
    def add_book(self, book):
        self.books.append(book)
        print(f"Added book: {book.title}")
    
    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    def remove_old_books(self, year_limit):
        removed_books = []
        new_books = []
        
        for book in self.books:
            if book.year < year_limit:
                removed_books.append(book)
            else:
                new_books.append(book)
        


        self.books = new_books
        print(f"Removed {len(removed_books)} old books")
        return removed_books
    
    def buy_book(self, isbn, quantity, email, address=None):
        book = self.find_book_by_isbn(isbn)
        
        if book is None:
            print("Book is not found")
            return False
        
        if not book.can_buy(quantity):
            if book.book_type == "showcase":
                print("Showcase book is not for sale")
            else:
                print("No enough stock")
            return False
        
        total = book.price * quantity
        
        if book.book_type == "paper":
            if address is None:
                print("Address is required for paper books")
                return False
            
            book.reduce_stock(quantity)
            
            if self.shipping_service:
                self.shipping_service.ship(book, quantity, address)
            
            print(f"Paper book is purchased, being shipped to {address}")
            print(f"Total: EGP{total}")
            return True
            
        elif book.book_type == "ebook":
            if self.email_service:
                self.email_service.send(book, email)
            
            print(f"EBook is purchased, Will email to {email}")
            print(f"Total: EGP{total}")
            return True
        
        return False
    
    def set_shipping_service(self, service):
        self.shipping_service = service
    
    def set_email_service(self, service):
        self.email_service = service

class ShippingService:
    def ship(self, book, quantity, address):
        print(f"Shipping {quantity} copies of '{book.title}' to {address}")

class EmailService:
    def send(self, book, email):
        print(f"Sending '{book.title}' ({book.file_type}) to {email}")

def test_bookstore():
    store = BookStore()
    
    store.set_shipping_service(ShippingService())
    store.set_email_service(EmailService())
    
    book1 = PaperBook("123456", "Example book 1", 2001, 29.99, 15)
    book2 = PaperBook("987654321", "Example book 2", 2025, 19.99, 3)
    book3 = EBook("1111111111", "Example book 3", 2023, 24.99, "pdf")
    book4 = ShowcaseBook("9999999999", "Example book 4", 1999, 5000.00)

    store.add_book(book1)
    store.add_book(book2)
    store.add_book(book3)
    store.add_book(book4)
    
    print("\n***Testing purchases***")
    
    store.buy_book("123456", 2, "customer1@email.com", "123 Main Street")

    store.buy_book("1111111111", 1, "customer2@gmail.com")

    store.buy_book("9999999999", 1, "customer3@email.com")

    store.buy_book("978-0987654321", 5, "customer4@company.com", "789 Business Ave")

    print("\n*** Removing old books***")
    old = store.remove_old_books(2010)
    for book in old:
        print(f"Removed: {book.get_info()}")

    print("\n*** Current inventory ***")
    for book in store.books:
        print(f"- {book.get_info()}")

if __name__ == "__main__":
    test_bookstore()