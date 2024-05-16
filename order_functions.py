def get_custid():
    id = input("Enter your ID:\n>")
    return id

def get_orderlist():
    orderlist = input("Enter your order: item, quantity; item, quantity; etc\n>")
    return orderlist

def get_price():
    price = input("Enter your total price:\n>")
    return price

def list_orders(cursor):
    cursor.execute("SELECT * FROM Orders")
    inv_list = cursor.fetchall()
    if(len(inv_list) != 0):
        print("Order ID | Customer ID | Order List | Price")
        print(inv_list)
    else:
        print("Order list is empty!")

def add_order(cursor):

    cust_id=get_custid()
    orderlist=get_orderlist()
    price= get_price()

    data = (cust_id, orderlist, price)

    try:
        cursor.execute("INSERT INTO Orders(customer_id, order_list, price) VALUES (%s, %s, %s)", data)
    except Exception:
        print("Invalid ID!")

def remove_order(cursor):
    cursor.execute("SELECT * FROM Orders")
    order_list = cursor.fetchall()
    if(len(order_list) != 0):
        id = input("\nPlease note you will not be able to recover deleted order data. Please enter the ID of the order you'd like to delete: \n> ")

        cursor.execute("SELECT * FROM Orders WHERE order_ID = (%s)", (id,))
        order_list = cursor.fetchall()
        if(len(order_list) != 0):
            cursor.execute("DELETE FROM Orders WHERE order_ID = (%s)", (id,))
        else:
            print("ID not found!")
    else:
        print("Order list is empty!")
    
def update_order(cursor):
    cursor.execute("SELECT * FROM Orders")
    order_list = cursor.fetchall()
    if(len(order_list) != 0):
        order_id = input("Enter order ID: \n> ")
        cursor.execute("SELECT * FROM Orders WHERE ORDER_ID = (%s)", (order_id,))
        order_list = cursor.fetchall()
        if(len(order_list) != 0):
            print("Order with ID", order_id, "found.")

            value = get_orderlist()
            cursor.execute('''UPDATE Orders
                            SET ORDER_LIST = (%s)''', (value,))

        else:
            print("ID not found!")
    else:
        print("Order list is empty!")
