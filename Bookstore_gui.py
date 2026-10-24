"""
Program: Book ordering system
Author: Reem Elsaadany
Date: December 2025
Description:
This program allows the user to manage a bookstore by adding customers, books, and creating orders
"""

'''
this file will contain all the code for the bookstore's GUI
'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Bookstore_core as core


def create_lists_tab(notebook, tab_header ,tab_title):
    '''This function creates the lists tab for all the records in the program'''
    frame = ttk.Frame(notebook)
    frame.rowconfigure(2, weight=1)

    tk.Label(frame, text=tab_header, font=("Arial", 20, "bold"), fg= "#6C2A0E",padx=5, pady=10).grid(row=0,column=0, columnspan=999, sticky='w')
    notebook.add(frame, text=tab_title) 

    return frame

def create_treelist(frame, treeview_columns):
    '''this function creates the treeview list for the corresponding tab'''
    treeview_frame = tk.Frame(frame) # create a new frame for the treeview list
    treeview_frame.grid(row=2, column=0, rowspan=20, columnspan=4, sticky='nsew')
    treeview_frame.columnconfigure(0, weight=1)
    treeview_frame.rowconfigure(0, weight= 1)

    list_treeview = ttk.Treeview(treeview_frame, columns=treeview_columns, show="headings") # add headings to the list
    list_treeview.grid(row=0, column=0, sticky='nsew')

    for column in treeview_columns:
        list_treeview.heading(column, text=column)
        list_treeview.column(column, stretch=True)
    
    framex_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL, command=list_treeview.xview) # Add a horizontal scrollbar
    list_treeview.configure(xscrollcommand=framex_scrollbar.set)
    framex_scrollbar.grid(row=1, column=0, sticky='ew')

    framey_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=list_treeview.yview) # Add a vertical scrollbar
    list_treeview.configure(yscrollcommand=framey_scrollbar.set)
    framey_scrollbar.grid(row=0, column=1, sticky='ns')

    return list_treeview

def clear_treeview(treeview):
    '''This function delets the current items in the provided Treeview list'''
    for item in treeview.get_children():
        treeview.delete(item)

def clear_listbox(listbox):
    '''This function deletes the current items in the provided listbox'''
    listbox.delete(0, tk.END)

def update_price_label(cart_price_label, shipping_price_label,total_price_label):
    '''This function updates the labels displaying the prices during the making of an order'''
    core.total_price = core.cart_price + core.shipping_price
    cart_price_label.config(text=f"Price of items in cart: £{core.cart_price}")
    shipping_price_label.config(text=f"Shipping: £{core.shipping_price}")
    total_price_label.config(text=f"\nTotal Price: £{core.total_price}")


    
def main():
# create a window
    window = tk.Tk()
    window.title('Bookstore Ordering System')
    window.geometry('1500x1000')
    bookstoreIcon = tk.PhotoImage(file='Book_icon.png') # to be changed
    window.iconphoto(True, bookstoreIcon)

    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)

    menu = tk.Menu(window)
    window.config(menu= menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='File', menu=file_menu)

    def clear_all_data():
        clear_treeview(book_treeview)
        clear_treeview(customers_treeview)
        clear_treeview(orders_treeview)
        buy_book_list.delete(0, tk.END)
        clear_book_cart()
        invoice_order_id.config(text='')
        invoice_customer_name.config(text='')
        invoice_customer_email.config(text='')
        invoice_customer_address.config(text='')
        invoice_shipping_address.config(text='')
        invoice_urgent_shipping.config(text='')
        invoice_books_purchased.config(text='')
        invoice_price_of_books.config(text='')
        invoice_shipping_price.config(text='')
        invoice_total_price.config(text='')

    def create_new_record_menu():
        '''this function discards previous data and allows the user to start creating new records.'''
        user_selection = messagebox.askokcancel("Unsaved Data", "The current records could be unsaved, would you like to create new records?")
        if user_selection:
            core.create_new_record()
            clear_all_data()
    
    file_menu.add_command(label='Create new records', command=lambda:create_new_record_menu())
    
    def load_records_menu():
        '''this function loads an old save of the bookstore's record if it exists, and raises an error if there's no previous save'''
        try:
            core.load_lists()
            clear_all_data()

            for book in core.books:
                book_treeview.insert('', 'end', values=(book.bookID, book.bookName.title(), book.year, book.genre.capitalize(), book.author.capitalize(), book.type, f"£{book.price}"))
                buy_book_list.insert(tk.END, f"{book.bookID}, {book.bookName.title()}, {book.year}, {book.genre.capitalize()}, {book.author.capitalize()}, {book.type}, £{book.price}")

            for customer in core.customers:
                customers_treeview.insert('', "end", values=(customer.customerID, f"{customer.firstName.capitalize()} {customer.lastName.capitalize()}", customer.email, customer.address.capitalize()))

            for order in core.orders:
                orders_treeview.insert('', "end", values=(order.orderID, f"{order.firstName} {order.lastName}", order.shippingAddress, order.booksOrdered, order.urgentShipping, order.totalPrice))
            messagebox.showinfo("Records loaded", "Loaded previous save file successfully.")
        except:
            messagebox.showerror("No previous save", "No previous save file found.")
    
    
    file_menu.add_command(label='Load previous records...', command=lambda:load_records_menu())

    def save_records_menu():
        '''This function saves the current records followed by a message confirming the success of the operation'''
        core.save_lists()
        messagebox.showinfo("Success", "Saved current records successfully.")
    
    file_menu.add_command(label='Save current records...', command=lambda:save_records_menu())

    def exit_menu():
        '''This function asks the user to confirm quitting before they decide to quit'''
        user_selection = messagebox.askokcancel("Quitting", "Your data might not be saved,\nAre you sure you want to exit the program?")
        if user_selection:
            window.quit()
            
    file_menu.add_command(label='Exit', command=lambda:exit_menu())
    

    help_menu = tk.Menu(menu, tearoff= 0)
    menu.add_cascade(label='Help', menu=help_menu)
    def show_program_help():
        '''This function briefly explains to the user how to use this program'''
        messagebox.showinfo("Getting started","Quick guide to get started:\n\n1. If this is your first time using the software, start by adding books to the system. After a book has been created, you can add orders to the system.\n\n2. You can save the current records in the file menu, which will overwrite any previous save file.\n\n3. If you have previous saves, you can load them from the file menu.\n\n4. You can create new records to clear previous data and start afresh. Keep in mind that your old data can still be loaded back unless you save your new records.")
    help_menu.add_command(label="Getting started", command=lambda:show_program_help())
    
    def show_about_program():
        '''This function shows a messagebox that informs the user about the program'''
        messagebox.showinfo("About Bookstore Ordering system", "Welcome to the Bookstore Ordering system (BOS)!\nThis program was developed to assist with managing customer and book records, orders and invoices\n\n• Version: BOS-1.0.0\n• Released on: 22nd of January 2026.\n\n• Developer: Reem Elsaadany\n• Developer student ID: 22851131\n• Student at The University of Northampton\n\n\n© 2026 Reem Elsaadany. Built with Tkinter")
    help_menu.add_command(label="About Bookstore Ordering System...", command=lambda:show_about_program())
    
    
    # create navigation frame
    navigation = tk.Frame(window, bg="#6C2A0E")
    navigation.grid(row=0, column=0, sticky= 'ns')
    tk.Button(navigation, text= "Home", font=("Arial", 14),command=lambda:core.show_frame(home_page),fg="white" ,bg="#6C2A0E", padx=20).pack(fill= 'x')
    tk.Button(navigation, text= "Books", font=("Arial", 14),command= lambda: core.show_frame(books_page), fg="white",bg="#6C2A0E", padx=20).pack(fill='x')
    tk.Button(navigation, text= "Customers", font=("Arial", 14),command=lambda:core.show_frame(customers_page),fg="white" ,bg="#6C2A0E", padx=20).pack(fill= 'x')
    tk.Button(navigation, text="Orders",font=("Arial", 14), command=lambda:core.show_frame(orders_page),fg="white" ,bg="#6C2A0E", padx=20).pack(fill='x')
    

    #create main working area
    main_working_area = tk.Frame(window)
    main_working_area.grid(row=0, column=1, sticky= 'nsew')
    main_working_area.rowconfigure(0, weight=1)
    main_working_area.columnconfigure(0, weight=1)

    home_page = tk.Frame(main_working_area) # Home page
    home_page.grid(row=0, column=0, sticky= 'nsew')
    tk.Label(home_page, text="Welcome to the Bookstore Ordering System!", font=("Arial", 20, 'bold'),fg="#6C2A0E").grid(row=0, column=0, sticky='w')
    home_bg = tk.PhotoImage(file="Welcome_page_bg.png")
    tk.Label(home_page, image=home_bg).grid(row=1, column=0, sticky='nsew')
    
    home_page.rowconfigure(1, weight=2)
    home_page.columnconfigure(0, weight= 1)

    books_page = tk.Frame(main_working_area) # Books page
    books_page.grid(row=0, column=0, sticky='nsew')
    books_page.rowconfigure(0, weight=1)
    books_page.columnconfigure(0, weight=1)

    books_page_notebook = ttk.Notebook(books_page) # Notebook inside Books page for book records, adding books, etc.
    books_page_notebook.pack(expand= True, fill='both')

    book_list_frame = create_lists_tab(books_page_notebook, "List of all available books at the Bookstore","Books List") # create a list of books at the bookstore as a tab in notebook
    book_treeview = create_treelist(book_list_frame, ("Book ID", "Book Name", "Book Year", "Book Author", "Book Genre", "Book Type", "Book Price"))

    add_book_tab = ttk.Frame(books_page_notebook) # create a tab to add books to the list
    add_book_tab.grid(row=0, column=0, sticky='nsew')
    tk.Label(add_book_tab, text="Add a book to the Bookstore's records", font=("Arial",20,"bold"), fg="#6C2A0E", padx= 5, pady=10).grid(row=0, column=0, columnspan= 4, sticky='w')
    
    book_name_frame = tk.Frame(add_book_tab) # create entry field for the book's name
    book_name_frame.grid(row=1, column=0)
    tk.Label(book_name_frame, text="Book's name:").pack()
    new_book_name = tk.Entry(book_name_frame)
    new_book_name.pack(fill='x')

    book_year_frame = tk.Frame(add_book_tab) # create entry field for the book's year of release
    book_year_frame.grid(row=1, column=1)
    tk.Label(book_year_frame, text="Year of release:").pack()
    new_book_year = tk.Entry(book_year_frame)
    new_book_year.pack(fill='x')
    
    book_author_frame = tk.Frame(add_book_tab) # create entry field for the book's author
    book_author_frame.grid(row=1, column=2)
    tk.Label(book_author_frame, text="Book's Author: ").pack()
    new_book_author = tk.Entry(book_author_frame)
    new_book_author.pack()

    book_genre_frame = tk.Frame(add_book_tab) # create a combobox for the book's genre
    book_genre_frame.grid(row=2, column=0)
    tk.Label(book_genre_frame, text="Book's Genre:").pack()
    genre_combobox = ttk.Combobox(book_genre_frame, values=core.genre)
    genre_combobox.current(0)
    genre_combobox.pack()
    other_genre_label = tk.Label(book_genre_frame, text="Other Genre:")
    other_genre_entry = tk.Entry(book_genre_frame)
    
    def combobox_selection(event=None):
        '''This function will pack a new entry field if the user chose "other" in the combobox'''
        if genre_combobox.get() == "Other": 
            other_genre_label.pack()
            other_genre_entry.pack()

        else:
            other_genre_label.pack_forget()
            other_genre_entry.pack_forget()

    genre_combobox.bind("<<ComboboxSelected>>", combobox_selection) # show an entry field for other genres only if other is selected

    book_type_frame = tk.Frame(add_book_tab) # create radio buttons for the book's type (physical, electronic, both)
    book_type_frame.grid(row= 2, column=1)
    tk.Label(book_type_frame, text="Book's type:").grid(sticky='w')
    new_book_type_selected = tk.StringVar(value="")
    tk.Radiobutton(book_type_frame, text="Physical", variable=new_book_type_selected, value="Physical").grid(row=1, sticky='w')
    tk.Radiobutton(book_type_frame, text="Electronic", variable=new_book_type_selected, value="Electronic").grid(row=2,sticky='w')
    tk.Radiobutton(book_type_frame, text="Both", variable=new_book_type_selected, value="Both").grid(row=3,sticky='w')

    book_price_frame = tk.Frame(add_book_tab) # create entry field for the book's price
    book_price_frame.grid(row=2, column=2)
    tk.Label(book_price_frame, text="Book's price:").pack()
    tk.Label(book_price_frame, text="£").pack(side="left")
    new_book_price = tk.Entry(book_price_frame)
    new_book_price.pack(fill='x')

    book_buttons_frame = tk.Frame(add_book_tab)
    book_buttons_frame.grid(row=3, column=1)

    def book_clear_button_functions():
        '''this function resets or clears all the data input by the user in the "Add Book" tab'''
        core.clear_entry_fields([new_book_name,new_book_year,new_book_author,other_genre_entry,new_book_price])
        genre_combobox.current(0)
        combobox_selection(event=None)
        new_book_type_selected.set("")
    
    def add_book_button_functions():
        '''this function checks the user's input for error and adds the book to the record if it passed the check'''
        book_errors_list = core.check_book_attributes(new_book_name, new_book_year, new_book_author,genre_combobox, other_genre_entry, new_book_type_selected, new_book_price)
        if not book_errors_list:
            new_book_genre = core.other_genre(genre_combobox, other_genre_entry)
            core.add_book_object(new_book_name, new_book_year, new_book_author, new_book_genre, new_book_type_selected, new_book_price)
            clear_treeview(book_treeview)
            clear_listbox(buy_book_list)
            for book in core.books:
                book_treeview.insert('', 'end', values=(book.bookID, book.bookName.title(), book.year, book.author.capitalize(), book.genre.capitalize(), book.type, f"£{book.price}"))
                buy_book_list.insert(tk.END, f"{book.bookID}, {book.bookName.title()}, {book.year}, {book.author.capitalize()}, {book.genre.capitalize()}, {book.type}, £{book.price}")
            book_clear_button_functions()
            messagebox.showinfo("Success", "The book has been successfully added to the list.")
        else:
            messagebox.showerror("Incorrect or missing input!", "Please check your input for the following errors:\n\n" + "\n".join(f"{i +1}. {error}" for i, error in enumerate(book_errors_list)))

    tk.Button(book_buttons_frame, text="Clear All Fields", command=lambda:book_clear_button_functions()).pack(side='left')
    tk.Button(book_buttons_frame, text="Add book", command=lambda:add_book_button_functions()).pack(side='right')
    books_page_notebook.add(add_book_tab, text="Add Book")


    customers_page = tk.Frame(main_working_area) # create new page for adding customers, keeping customer records, and deleting customers
    customers_page.grid(row=0, column=0, sticky="nsew")
    customers_notebook = ttk.Notebook(customers_page)
    customers_notebook.pack(expand=True, fill="both")

    customers_list_frame = create_lists_tab(customers_notebook, "List of all the customers of the Bookstore","Customers List") # create a tab to keep a list of all customer records
    customers_treeview = create_treelist(customers_list_frame, ["Customer ID", "Full Name", "Email", "Address"])

    orders_page = tk.Frame(main_working_area) # create a page for managing and adding orders
    orders_page.grid(row=0, column=0, sticky='nsew')
    orders_page.rowconfigure(0, weight=1)
    orders_page.columnconfigure(0, weight=1)

    orders_notebook = ttk.Notebook(orders_page)
    orders_notebook.pack(expand=True, fill="both")

    orders_list_tab = create_lists_tab(orders_notebook, "Search for an invoice:", "Invoice Search") # create a tab for the orders list
    orders_treeview = create_treelist(orders_list_tab, ["Order ID", "Customer Name", "Shipping address", "Books Ordered", "Urgent shipping", "Total Price"])
    tk.Label(orders_list_tab, text="Search invoice ID:").grid(row=1, column=0)
    search_entry = tk.Entry(orders_list_tab, width=50)
    search_entry.grid(row=1, column=1)
    def search_button():
        '''This function searches for Order ID matches and shows them in the treeview'''
        search_matches = core.find_search_matches(search_entry)
        clear_treeview(orders_treeview)
        for order in search_matches:
            orders_treeview.insert('', "end", values=(order.orderID, f"{order.firstName} {order.lastName}", order.shippingAddress, order.booksOrdered, order.urgentShipping, order.totalPrice))

    tk.Button(orders_list_tab, text="Search", command=lambda:search_button()).grid(row=1, column=2)
    invoice_frame = tk.Frame(orders_list_tab)
    invoice_frame.grid(row=0, column=4, rowspan=3)
    tk.Label(invoice_frame, text="Invoice details:", font=("Arial", 20, "bold"), fg= "#6C2A0E",padx=5, pady=10).grid(row=0, column=0, columnspan=2)
    tk.Label(invoice_frame, text="Order ID: ", fg= "#6C2A0E").grid(row=1, column=0, sticky="e")
    tk.Label(invoice_frame, text="Customer Name: ", fg= "#6C2A0E").grid(row=2, column=0, sticky="e")
    tk.Label(invoice_frame, text="Customer Email: ", fg= "#6C2A0E").grid(row=3, column=0, sticky="e")
    tk.Label(invoice_frame, text="Customer Address: ", fg= "#6C2A0E").grid(row=4, column=0, sticky="e")
    tk.Label(invoice_frame, text="Shipping Address: ", fg= "#6C2A0E").grid(row=5, column=0, sticky="e")
    tk.Label(invoice_frame, text="Urgent shipping: ", fg= "#6C2A0E").grid(row=6, column=0, sticky="e")
    tk.Label(invoice_frame, text="Books Purchased: ", fg= "#6C2A0E").grid(row=7, column=0, sticky="en")
    tk.Label(invoice_frame, text="Price of Purchased Books: ", fg= "#6C2A0E").grid(row=8, column=0, sticky="e")
    tk.Label(invoice_frame, text="Shipping Price: ", fg= "#6C2A0E").grid(row=9, column=0, sticky="e")
    tk.Label(invoice_frame, text="Total Price: ", fg= "#6C2A0E").grid(row=10, column=0, sticky="e")

    invoice_order_id = tk.Label(invoice_frame, text='')
    invoice_order_id. grid(row=1, column=1, sticky="w")
    invoice_customer_name = tk.Label(invoice_frame, text='')
    invoice_customer_name. grid(row=2, column=1, sticky="w")
    invoice_customer_email = tk.Label(invoice_frame, text='')
    invoice_customer_email. grid(row=3, column=1, sticky="w")
    invoice_customer_address = tk.Label(invoice_frame, text='')
    invoice_customer_address. grid(row=4, column=1, sticky="w")
    invoice_shipping_address = tk.Label(invoice_frame, text='')
    invoice_shipping_address. grid(row=5, column=1, sticky="w")
    invoice_urgent_shipping = tk.Label(invoice_frame, text='')
    invoice_urgent_shipping. grid(row=6, column=1, sticky="w")
    invoice_books_purchased = tk.Label(invoice_frame, text='')
    invoice_books_purchased. grid(row=7, column=1, sticky="w")
    invoice_price_of_books = tk.Label(invoice_frame, text='')
    invoice_price_of_books. grid(row=8, column=1, sticky="w")
    invoice_shipping_price = tk.Label(invoice_frame, text='')
    invoice_shipping_price. grid(row=9, column=1, sticky="w")
    invoice_total_price = tk.Label(invoice_frame, text='')
    invoice_total_price. grid(row=10, column=1, sticky="w")

    def selected_order_in_treeview(event):
        '''This function changes the invoice details when the user selects an item in the order list'''
        order_selection = orders_treeview.selection()
        if not order_selection:
            return
        
        order = order_selection[0]
        order_values = orders_treeview.item(order, "values")
        order_ID = order_values[0]

        invoice_details = core.show_invoice_details(order_ID)

        if not invoice_details:
            return

        invoice_order_id.config(text=invoice_details["Order ID"])
        invoice_customer_name.config(text=invoice_details["Customer name"])
        invoice_customer_email.config(text=invoice_details["Customer email"])
        invoice_customer_address.config(text=invoice_details["Customer address"])
        invoice_shipping_address.config(text=invoice_details["Shipping Address"])
        if invoice_details["Urgent shipping"]:
            invoice_urgent_shipping.config(text="Yes")
        else:
            invoice_urgent_shipping.config(text="No")
        invoice_books_purchased.config(text="\n".join(f"{i +1}. {book}" for i, book in enumerate(invoice_details["Books Purchased"])))
        invoice_price_of_books.config(text=f"£{invoice_details["Price of purchased books"]}")
        if invoice_details["Urgent shipping"]:
            invoice_shipping_price.config(text=f"£{urgent_price}")
        else:
            invoice_shipping_price.config(text="£0.0")
        invoice_total_price.config(text=f"£{invoice_details["Total Price"]}")

    orders_treeview.bind("<<TreeviewSelect>>", selected_order_in_treeview)


    add_order_tab = tk.Frame(orders_notebook) # create a tab for adding orders and customers
    add_order_tab.grid(row=0, column=0)

    tk.Label(add_order_tab, text="Create an order", font=("Arial",20,"bold"), fg="#6C2A0E", padx= 5, pady=10).grid(row=0, column=0, columnspan= 4, sticky='w')
    tk.Label(add_order_tab, text="Customer details:", font=("Arial", 12)).grid(row=1, column=0, columnspan= 4, sticky='w')

    tk.Label(add_order_tab, text="First name: ").grid(row=2, column=0)
    customer_forename = tk.Entry(add_order_tab, width=50)
    customer_forename.grid(row=2, column=1)
    tk.Label(add_order_tab, text="Last Name: ").grid(row=3, column=0)
    customer_surname = tk.Entry(add_order_tab, width= 50)
    customer_surname.grid(row=3, column=1)
    tk.Label(add_order_tab, text="Email: ").grid(row=4, column=0)
    customer_email = tk.Entry(add_order_tab, width=50)
    customer_email.grid(row=4, column=1)
    tk.Label(add_order_tab, text="Address: ").grid(row=5, column=0)
    customer_address = tk.Entry(add_order_tab, width=50)
    customer_address.grid(row=5, column=1)
    shipping_boolean = tk.BooleanVar(value=True)

    def shipping_checkbutton_false():
        '''This function shows the user an entry field if they choose to have a different shipping address'''
        if not shipping_boolean.get():
            shipping_address_label.grid(row=3, column=2, sticky="w")
            shipping_address_entry.grid(row=4, column=2)
        else:
            shipping_address_label.grid_forget()
            shipping_address_entry.grid_forget()
    
    shipping_checkbutton = tk.Checkbutton(add_order_tab, text="Shipping address is the same as the customer's address", variable=shipping_boolean, command=lambda:shipping_checkbutton_false())
    shipping_checkbutton.grid(row=2, column=2)
    shipping_address_label = tk.Label(add_order_tab, text="Shipping address: ")
    shipping_address_entry = tk.Entry(add_order_tab, width=50)

    urgent_boolean = tk.BooleanVar(value=False)

    def urgent_boolean_true():
        '''This function adds the price of urgent shipping to the total price if the user chooses urgent shipping'''
        if urgent_boolean.get():
            core.shipping_price = urgent_price
            update_price_label(cart_price_label, shipping_price_label,total_price_label)
        else:
            core.shipping_price = 0.0
            update_price_label(cart_price_label, shipping_price_label,total_price_label)

    urgent_checkbutton = tk.Checkbutton(add_order_tab, text="Urgent Shipping", variable=urgent_boolean, command=lambda:urgent_boolean_true())
    urgent_checkbutton.grid(row=5, column=2, sticky="w")
    urgent_price = 3.75
    tk.Label(add_order_tab, text=f"+ £{urgent_price}").grid(row=5, column=2, sticky="e")

    order_details_frame = tk.Frame(add_order_tab)
    order_details_frame.grid(row=6, column=0, columnspan=10)
    tk.Label(order_details_frame, text="Order details:", font=("Arial",12)).grid(row=0, column=0, columnspan= 4, sticky='w')
    tk.Label(order_details_frame, text="Please select the books you would like to purchase:").grid(row=1, column=0)
    buy_book_list = tk.Listbox(order_details_frame, width= 100, height=20)
    buy_book_list.grid(row=2, column=0)
    tk.Label(order_details_frame, text="Books Cart:").grid(row=1, column=1)
    selected_books = tk.Listbox(order_details_frame, height=20, width=100)
    selected_books.grid(row=2, column=1)

    def add_selected_book():
        '''This function adds the selected book in the books list to the user's cart upon pressing the button, which updates the price labels'''
        index = buy_book_list.curselection()

        if not index:
            return
        
        i = index[0]
        book = buy_book_list.get(i)
        selected_books.insert(tk.END, book)
        core.increase_cart_price(i)
        update_price_label(cart_price_label, shipping_price_label,total_price_label)

    def clear_book_cart():
        '''This function clears the user's cart, which resets the cart price'''
        selected_books.delete(0, tk.END)
        core.cart_price = 0.0
        update_price_label(cart_price_label, shipping_price_label,total_price_label)

    tk.Button(order_details_frame, text="Add book to cart", command=lambda:add_selected_book()).grid(row=3, column=0, sticky="ew")
    tk.Button(order_details_frame, text="Clear Cart", command=lambda:clear_book_cart()).grid(row=3, column=1, sticky="ew")

    cart_price_label = tk.Label(order_details_frame, text=f"Price of items in cart: £{core.cart_price}")
    cart_price_label.grid(row=4, column=1, sticky="w")
    shipping_price_label = tk.Label(order_details_frame, text=f"Shipping: £{core.shipping_price}")
    shipping_price_label.grid(row=5, column=1, sticky="w")
    total_price_label = tk.Label(order_details_frame, text=f"\nTotal Price: £{core.total_price}")
    total_price_label.grid(row=6, column=1, sticky="w")

    def clear_order_details_button():
        '''This function clears all the entries and lists in the add order tab'''
        core.clear_entry_fields([customer_forename, customer_surname, customer_email, customer_address, shipping_address_entry])
        shipping_boolean.set(True)
        shipping_checkbutton_false()
        urgent_boolean.set(False)
        urgent_boolean_true()
        clear_book_cart()

    tk.Button(add_order_tab, text="Clear All Fields",command=lambda:clear_order_details_button()).grid(row=7, column=1)

    def create_order_button():
        '''This function checks the customer and order input, showing an error if there are errors, or affirming the success of the operation'''
        customer_error_list = core.check_customer_attributes(customer_forename, customer_surname, customer_email, customer_address)
        order_error_list = core.check_order_attributes(selected_books, shipping_boolean, shipping_address_entry)
        errors_list = customer_error_list + order_error_list
        if not errors_list:
            core.add_customer_object(customer_forename, customer_surname, customer_email, customer_address)
            core.add_order_object(customer_forename, customer_surname, customer_email, customer_address, selected_books, shipping_boolean, shipping_address_entry, urgent_boolean)
            clear_treeview(customers_treeview)
            clear_treeview(orders_treeview)
            for customer in core.customers:
                customers_treeview.insert('', "end", values=(customer.customerID, f"{customer.firstName.capitalize()} {customer.lastName.capitalize()}", customer.email, customer.address.capitalize(), ))
            for order in core.orders:
                orders_treeview.insert('', "end", values=(order.orderID, f"{order.firstName} {order.lastName}", order.shippingAddress, ", ".join(order.booksOrdered), order.urgentShipping, order.totalPrice))
            clear_order_details_button()
            messagebox.showinfo("Success", "Order and customer successfully added.")
        else:
            messagebox.showerror("Incorrect or missing input!", "Please check your input for the following errors:\n\n" + "\n".join(f"{i +1}. {error}" for i, error in enumerate(errors_list)))

    tk.Button(add_order_tab, text="Create Order", command=lambda:create_order_button()).grid(row=7, column=2)

    orders_notebook.add(add_order_tab, text="Add Order")

    core.show_frame(home_page)
    window.mainloop()

if __name__ == "__main__":
    main()