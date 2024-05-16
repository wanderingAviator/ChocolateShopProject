# first and last name functions
def get_fname():
    fname = input("Enter your first name:\n>")
    return fname

def get_lname():
    lname = input("Enter your last name:\n>")
    return lname

def get_address():
    address = input("Enter your address:\n>")
    return address

def get_number():
    number = input("Enter your phone number:\n>")
    return number

def list_customers(cursor):
    cursor.execute("SELECT * FROM Customer")
    cust_list = cursor.fetchall()
    if(len(cust_list) != 0):
        print("Customer ID | First Name | Last Name | Address | Phone #")
        print(cust_list)
    else:
        print("Customer list is empty!")

def add_customer(cursor):

    first_name=get_fname()
    last_name=get_lname()
    address=get_address()
    number=get_number()

    data = (first_name, last_name, address, number)

    cursor.execute("INSERT INTO Customer(first_name, last_name, address, number) VALUES (%s, %s, %s, %s)", data)

def remove_customer(cursor):
    cursor.execute("SELECT * FROM Customer")
    cust_list = cursor.fetchall()
    if(len(cust_list) != 0):
        id = input("\nPlease note you will not be able to recover deleted customer data. Please enter the ID of the customer you'd like to delete: \n> ")

        cursor.execute("SELECT * FROM Customer WHERE CUSTOMER_ID = (%s)", (id,))
        cust_list = cursor.fetchall()
        if(len(cust_list) != 0):
            cursor.execute("DELETE FROM Customer WHERE CUSTOMER_ID = (%s)", (id,))
        else:
            print("ID not found!")
    else:
        print("Customer list is empty!")
    
def update_customer(cursor):
    cursor.execute("SELECT * FROM Customer")
    cust_list = cursor.fetchall()
    if(len(cust_list) != 0):
        cust_id = input("Enter customer ID: \n> ")
        cursor.execute("SELECT * FROM Customer WHERE CUSTOMER_ID = (%s)", (cust_id,))
        cust_list = cursor.fetchall()
        if(len(cust_list) != 0):
            print("Customer with ID", cust_id, "found.")

            attribute = input(f"Enter attribute to update: FIRST_NAME, LAST_NAME, ADDRESS, NUMBER \n> ")
            
            match attribute.upper():

                case "FIRST_NAME":
                    value = get_fname()
                    cursor.execute('''UPDATE Customer
                                   SET FIRST_NAME = (%s)''', (value,))
                case "LAST_NAME":
                    value = get_lname()
                    cursor.execute('''UPDATE Customer
                                   SET LAST_NAME = (%s)''', (value,))
                case "ADDRESS":
                    value = get_address()
                    cursor.execute('''UPDATE Customer
                                   SET ADDRESS = (%s)''', (value,))
                case "NUMBER":
                    value = get_number()
                    cursor.execute('''UPDATE Customer
                                   SET NUMBER = (%s)''', (value,))
                case _:
                    print("Not a valid attribute!")
        else:
            print("ID not found!")
    else:
        print("Customer list is empty!")
