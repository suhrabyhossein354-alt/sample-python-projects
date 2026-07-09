class Books:  
    def __init__(self, title, author, yop, stock):
        self.title = title
        self.author = author
        self.yop = yop
        self.stock = int(stock)  

    def __str__(self):
        return f"Book: {self.title} | Author: {self.author} | Year: {self.yop} | Stock: {self.stock}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, yop, stock):
        for book in self.books:
            if book.title.lower() == title.lower():
                print(f"Book '{title}' already exists!")
                return
        
        new_book = Books(title, author, yop, stock)
        self.books.append(new_book)
        print(f"{title} added successfully.")

    def remove_book(self, title):
        book_to_remove = None
        for book in self.books:
            if book.title.lower() == title.lower():
                book_to_remove = book
                break
        
        if book_to_remove:
            self.books.remove(book_to_remove)
            print(f"{title} removed")
        else:
            print(f"{title} is not in list")

    def search_book(self, book_name):
        found = False
        for book in self.books:
            if book.title.lower() == book_name.lower():
                print(f"Found: {book}")
                found = True
                break
        if not found:
            print("This book is not in the list.")

    def all_books(self):
        if not self.books:
            print("List is empty.")
            return
        print("The books:\n↓↓↓↓↓↓↓↓↓")
        for book in self.books:
            print(book)

my_library = Library()

while True:
    print("\n----- Library Menu -----")
    print("1. Books List")
    print("2. Add Book")
    print("3. Remove Book")
    print("4. Search Book")
    print("5. Exit")
    
    choice = input("Choose a number between 1 and 5: ")
    
    if choice == "1":
        my_library.all_books()
    elif choice == "2":
        title = input("Enter book name: ")
        author = input("Enter book author: ")
        yop = input("Enter year of book: ")
        stock = input("Enter stock: ")
        my_library.add_book(title, author, yop, stock)
    elif choice == "3":
        title = input("Enter book name to remove: ")
        my_library.remove_book(title)
    elif choice == "4":
        title = input("Enter book name to search: ")
        my_library.search_book(title)
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid input. Please try again.")   
        continue



    