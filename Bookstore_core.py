"""
Program: Book ordering system
Author: Reem Elsaadany
Date: December 2025
Description:
This program allows the user to manage a bookstore by adding customers, books, and creating orders
"""


'''
This file contains all classes and functionalities of the Bookstore ordering system
'''
import tkinter as tk
from tkinter import ttk
import pickle as pkl


books = []
Book_ID = 1

customers = []
Customer_ID = 1

orders = []
Order_ID = 1
# create parent class "Book"
class Book:
    def __init__(self, bookID, bookName, year, genre, author, type, price):
        self.__bookID = bookID
        self.__bookName = bookName
        self.__year = year
        self.__genre = genre
        self.__author = author
        self.__type = type
        self.__price = price

    # define getters and setters
    @property
    def bookID(self):
        return self.__bookID
    
    @bookID.setter
    def bookID(self ,newBookID):
        self.__bookID = newBookID
    
    @property
    def bookName(self):
        return self.__bookName
    
    @bookName.setter
    def bookName(self, newBookName):
        self.__bookName = newBookName

    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self,newYear):
        self.__year = newYear
    
    @property
    def genre(self):
        return self.__genre
    
    @genre.setter
    def genre(self,newGenre):
        self.__genre = newGenre

    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, newAuthor):
        self.__author = newAuthor

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, newType):
        self.__type = newType

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, newPrice):
        self.__price = newPrice

    def _change_both_type(self):
        if self.type == "Both":
            self.type = "Physical & Electronic"

        
# create parent class "Person"
class Person:
    def __init__(self, firstName, lastName, email, address):
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._address = address

    #define getters and setters
    @property
    def firstName(self):
        return self._firstName
    
    @firstName.setter
    def firstName(self, newFirstName):
        self._firstName = newFirstName

    @property
    def lastName(self):
        return self._lastName
    
    @lastName.setter
    def lastName(self, newLastName):
        self._lastName = newLastName

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, newEmail):
        self._email = newEmail

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, newAddress):
        self._address = newAddress


# create subclass "Customer" that inherits from "Person"
class Customer(Person):
    def __init__(self, customerID, firstName, lastName,email, address):
        super().__init__(firstName, lastName, email, address)
        self._customerID = customerID

    # getters and setters for customer class
    @property
    def customerID(self):
        return self._customerID
    
    @customerID.setter
    def customerID(self, new_ID):
        self._customerID = new_ID

# create parent class cart
class Cart:
    def __init__(self, booksOrdered, cartPrice):
        self._booksOrdered = booksOrdered
        self._cartPrice = cartPrice

    @property
    def booksOrdered(self):
        return self._booksOrdered
    
    @booksOrdered.setter
    def booksOrdered(self, books_selected):
        self._booksOrdered = books_selected

    @property
    def cartPrice(self):
        return self._cartPrice
    
    @cartPrice.setter
    def cartPrice(self, new_price):
        self._cartPrice = new_price

# create subclass order that inherits from cart and customer
class Order (Customer, Cart):
    def __init__(self, firstName, lastName, email, address, customerID, booksOrdered, cartPrice, orderID, shippingAddress, urgentShipping, totalPrice):
        self._booksOrdered = booksOrdered
        self._cartPrice = cartPrice
        Customer.__init__(self, customerID, firstName, lastName, email, address)
        Cart.__init__(self, booksOrdered, cartPrice)
        self.__orderID = orderID
        self.__shippingAddress = shippingAddress
        self.__urgentShipping = urgentShipping
        self.__totalPrice = totalPrice

    @property
    def orderID(self):
        return self.__orderID
    
    @orderID.setter
    def orderID(self, new_ID):
        self.__orderID = new_ID

    @property
    def shippingAddress(self):
        return self.__shippingAddress
    
    @shippingAddress.setter
    def shippingAddress(self, new_shipping_address):
        self.__shippingAddress = new_shipping_address

    @property
    def urgentShipping(self):
        return self.__urgentShipping
    
    @urgentShipping.setter
    def urgentShipping(self, urgent_shipping):
        self.__urgentShipping = urgent_shipping

    @property
    def totalPrice(self):
        return self.__totalPrice
    
    @totalPrice.setter
    def totalPrice(self, new_total):
        self.__totalPrice = new_total

def show_frame(frame):
    '''this function changes the frames in the window after pressing certain buttons'''
    frame.tkraise()

def create_new_record():
    '''this function resets the book ID count and removes all the objects in the program'''
    global Book_ID, books, Customer_ID, customers, Order_ID, orders
    Book_ID = 1
    Customer_ID = 1
    Order_ID = 1
    books = []
    customers = []
    orders = []

def save_lists():
    ''' this function saves current data in the records to a pickle file'''
    data_to_be_saved = {
        "Book ID": Book_ID,
        "Books list": books,
        "Customer ID": Customer_ID,
        "Customers list": customers,
        "Order ID": Order_ID,
        "Orders": orders
    }
    with open("Books.pkl", "wb") as f:
        pkl.dump(data_to_be_saved, f)

def load_lists():
    '''this function loads data from a pre-existing pickle file'''
    global Book_ID, books, Customer_ID, customers, Order_ID, orders
    with open("Books.pkl", "rb") as f:
        loaded_data = pkl.load(f)
        Book_ID = loaded_data["Book ID"]
        books = loaded_data["Books list"]
        Customer_ID = loaded_data["Customer ID"]
        customers = loaded_data["Customers list"]
        Order_ID = loaded_data["Order ID"]
        orders = loaded_data["Orders"]

def find_search_matches(search_entry):
    '''this function creates a list of all the objects that match the search criteria'''
    id = search_entry.get()
    search_matches = []
    for order in orders:
        if id in order.orderID:
            search_matches.append(order)
    
    return search_matches

def clear_entry_fields(entries_list):
    '''this function clears all the entry widgets in an "add object" tab'''
    for entry in entries_list:
        entry.delete(0, tk.END)

def add_book_object(name_entry, year_entry, author_entry, genre, type_radiobuttons, price_entry):
    '''this function takes the input from the entry fields and creates a new object with the data'''
    global Book_ID
    new_book = Book(bookID=f"B-{Book_ID:08}",bookName=name_entry.get(),year=year_entry.get(),author=author_entry.get(),genre=genre,type=type_radiobuttons.get(),price=price_entry.get())
    new_book._change_both_type()

    books.append(new_book)
    Book_ID += 1 # after creating a new book object, increase the book ID variable by 1

def check_book_attributes(name_entry, year_entry, author_entry, genre_combobox, other_genre_entry, type_str, price_entry):
    '''this function checks the entries of the user to add a book to make sure the input is valid'''
    book = {
        "name": name_entry.get(), "year of release": year_entry.get(), "author": author_entry.get(),
        "genre": genre_combobox.get(),"other genre": other_genre_entry.get(), "type": type_str.get(), "price": price_entry.get()
    }
    book_errors_list = [] # store a list of all the errors in the entries that the user provided

    if book["name"].strip() == '': # if book name is not provided, show an error message
        book_errors_list.append("Book name entry cannot remain empty. please input a name.")
    elif len(book["name"]) > 150: # if book name exceeds character limit, raise an error message
        book_errors_list.append("Book name cannot exceed 150 characters.")
    
    if book["year of release"].strip() == '': # if user did not provide a year of release, raise an error message
        book_errors_list.append("Year of release cannot remain empty. please input the year of release.")
    else:
        try: # if user inputs invalid year, raise an error message
            if int(book["year of release"]) < 0 or int(book["year of release"]) > 2026:
                book_errors_list.append("Year of release is invalid. Please provide a valid year of release.")
        except: # if user input anything thats not an integer, raise an error
            book_errors_list.append("Year of release must be a number. Please write the year of release in numbers")
    
    if book["author"].strip() == '': # if the user did not provide an author's name, raise an error message
        book_errors_list.append("Book's author cannot remain empty. Please provide the author's name.")
    elif len(book["author"]) > 50: #if author name exceeds character limit, raise an error
        book_errors_list.append("Author's name cannot exceed 50 characters.")
    
    if book["genre"] == "Select Genre...": # if the user did not select a genre yet, raise an error message
        book_errors_list.append("Please select the book's genre.")
    elif book["genre"] == "Other" and book["other genre"].strip() == '': # if the user selected "other" genre and didnt specify, raise an error message
        book_errors_list.append("Please specify the other genre of the book.")
    
    if not book["type"]: # if the user did not select a book type, raise an error message
        book_errors_list.append("Please select the book's type.")
    
    if book["price"].strip() == '': # if the user did not provide a price, raise an error message
        book_errors_list.append("Book price cannot remain empty. please provide the book's price.")
    else:
        try:
            float(book["price"])
        except: # if the user provided a price that is not a number (or a number followed by symbols), raise an error message
            book_errors_list.append("Book's price must be a number. Please provide a valid number without characters or symbols.")

    return book_errors_list

genre = ['Select Genre...', 'Sci-fi', 'Romance', 'Fantasy', 'Thriller', 'Fiction', 'Education', 'Other']        
def other_genre(genre_combobox, genre_entry):
    '''this function returns the value of either the genre combobox or the entry field to a variable based on the user's input'''
    if genre_combobox.get() == "Other":
        return genre_entry.get()
    else:
        return genre_combobox.get()

cart_price = 0.0 # price of the items in the cart only
shipping_price = 0.0 # price of shipping the order
total_price = 0.0 # price of all the items and the shipping

def increase_cart_price(index): 
    '''This function adds the price of the specified book to the total price of the items in the cart'''
    global cart_price
    cart_price += float(books[index].price)
    return cart_price
    
def check_customer_attributes(forename, surname, email, address):
    '''This function checks the the data the user input for incorrect or missing values'''
    customer = {
        "Forename": forename.get(), "Surname": surname.get(),
        "Email": email.get(), "Address": address.get()
    }
    customer_error_list = [] # This list stores any possible error in the user's input

    if customer["Forename"].strip() == '' or customer["Surname"].strip() == '':
        customer_error_list.append("Customer name cannot be empty. Please provide the customer's first and last name.") # if a first or last name are not provided, raise an error message
    else:
        if len(customer["Forename"]) > 50:
            customer_error_list.append("Customer first name exceeds 50 character limit.") # if the first name exceeds 50 characters, raise an error
        if len(customer["Surname"]) > 50:
            customer_error_list.append("Customer last name exceeds 50 character limit.") # if the last name exceeds 50 characters, raise an error
    
    if customer["Email"].strip() == '':
        customer_error_list.append("Please provide an email.") # if an email is not provided, raise an error
    elif "@" not in customer["Email"] or "." not in customer["Email"]:
        customer_error_list.append("Invalid email. Email must contain '@' and '.'.") # if an email does not contain @ or ., raise an error

    if customer["Address"].strip() == '':
        customer_error_list.append("Please provide the customer's Home address.") # if an address was not provided, raise an error

    return customer_error_list

def order_shipping_address(customer_address, shipping_boolean, shipping_address_entry):
    '''This function checks the shipping address checkbutton, which checks if the customer wants the order to be shipped to their home address '''
    boolean = shipping_boolean.get()
    if boolean == True:
        return customer_address.get() # if the checkbutton is true, return the customer's address
    else:
        return shipping_address_entry.get() # if the checkbutton is false, return the contents of the shipping address entry

def check_order_attributes(selected_books, shipping_boolean, other_shipping_address):
    '''This function checks for any missing data for the order'''
    order = {
        "Books": list(selected_books.get(0, tk.END)), "Shipping address boolean": shipping_boolean.get(),
        "Other shipping address": other_shipping_address.get()
    }
    order_errors_list = []

    if not order["Books"]: # if there are no books in the cart, raise an error message
        order_errors_list.append("You cannot create an order when your cart is empty. Please add books to your cart.")

    if order["Shipping address boolean"] == False: # if the user has no shipping address provided and the checkbutton is false, raise an error
        if not order["Other shipping address"]:
            order_errors_list.append("Please provide the shipping address.")

    return order_errors_list

def add_customer_object(forename, surname, email, address):
    '''this function takes the input from the entry fields and creates a new object with the data'''
    global Customer_ID
    new_customer = Customer(customerID=f"C-{Customer_ID:08}",firstName=forename.get(),lastName=surname.get(),email=email.get(),address=address.get())

    customers.append(new_customer)
    Customer_ID += 1 # after creating a new customer object, increase the customer ID variable by 1

def add_order_object(forename, surname, email, address, selected_books, shipping_boolean, shipping_address_entry, urgent_boolean):
    global Order_ID
    new_order = Order(orderID=f"I-{Order_ID:08}", firstName=forename.get(), lastName=surname.get(), email=email.get(),address=address.get(), shippingAddress=order_shipping_address(address,shipping_boolean,shipping_address_entry),urgentShipping=urgent_boolean.get(),booksOrdered=list(selected_books.get(0, tk.END)), cartPrice=round(cart_price, 2), totalPrice=round(total_price,2), customerID=Customer_ID)
    orders.append(new_order)
    Order_ID += 1 # after creating a new order object, increase the order ID variable by 1

def show_invoice_details(order_ID): 
    '''This function returns the invoice details of a specific order object'''
    global orders
    for order in orders: # iterate over each order in the orders list
        if order.orderID == order_ID: # if the ID of the current iteration matches the ID of the selected treeview item, return its invoice details
            invoice_details = {
                "Order ID": order.orderID, "Customer name": f"{order.firstName} {order.lastName}", "Customer email": order.email,
                "Customer address": order.address, "Shipping Address": order.shippingAddress, "Urgent shipping": order.urgentShipping,
                "Books Purchased": order.booksOrdered, "Price of purchased books": order.cartPrice, "Total Price": order.totalPrice
            }

            return invoice_details
