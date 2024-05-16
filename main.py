import cust_functions as cust
import mysql.connector as sql
import inv_functions as inv
import order_functions as ord

def crud_menu(which, cursor, db):

    while True:
        try:
            choice = input(
                "Please enter 'C' for Creating Entries, 'R' for Reading Entries, 'U' for Updating Entries, 'D' for Deleting Entries, "
                "'B' for Back to category select, 'Q' to exit app: \n> ").upper()
            if choice == 'C':
                match(which):
                    case "C":
                        cust.add_customer(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "I":
                        inv.add_item(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "O":
                        ord.add_order(cursor)
                        db.commit()
                        print("Operation completed!")
            elif choice == 'R':
                match(which):
                    case "C":
                        cust.list_customers(cursor)
                    case "I":
                        inv.list_inventory(cursor)
                    case "O":
                        ord.list_orders(cursor)
            elif choice == 'U':
                match(which):
                    case "C":
                        cust.update_customer(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "I":
                        inv.update_item(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "O":
                        ord.update_order(cursor)
                        db.commit()
                        print("Operation completed!")
            elif choice == 'D':
                match(which):
                    case "C":
                        cust.remove_customer(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "I":
                        inv.remove_item(cursor)
                        db.commit()
                        print("Operation completed!")
                    case "O":
                        ord.remove_order(cursor)
                        db.commit()
                        print("Operation completed!")
            elif choice == 'B':
                category_menu(cursor, db)
            elif choice == 'Q':
                quit()
            else:
                raise CrudInputException()
        except CrudInputException:
            pass

def category_menu(cursor, db):
    while True:
        try:
            choice = input(
                "Please enter 'C' for Customer, 'I' for Inventory, 'O' for Orders, 'S' for the Weekly Stats, 'Q' to exit app: \n> ").upper()
            if choice == 'C':
                crud_menu("C", cursor, db)
            elif choice == 'I':
                crud_menu("I", cursor, db)
            elif choice == 'O':
                crud_menu("O", cursor, db)
            elif choice == 'S':
                printstats(cursor)
            elif choice == 'Q':
                # Exit Application
                quit()
            else:
                raise CategoryInputException()
        except CategoryInputException:
            pass

class CategoryInputException(Exception):
    def __init__(self):
        print("Please enter a valid input: 'C', 'I', 'O', 'Q'")

class CrudInputException(Exception):
    def __init__(self):
        print("Please enter a valid input: 'C', 'R', 'U', 'D', 'Q'")

def printstats(cursor):

    print()

    cursor.execute("SELECT * FROM Inventory")
    item_list = cursor.fetchall()
    if(len(item_list) != 0):
        cursor.execute("SELECT ITEM_NAME, PRICE FROM Inventory ORDER BY PRICE DESC LIMIT 5 ")
        value = cursor.fetchall()
        print("Top 5 most expensive stock + their price:")
        print(value)

        cursor.execute("SELECT ITEM_NAME, STOCK FROM Inventory ORDER BY STOCK ASC LIMIT 5 ")
        value = cursor.fetchall()
        print("Top 5 best selling items + their remaining stock:")
        print(value)

        cursor.execute('''SELECT ITEM_NAME, STOCK, PRICE, CASE WHEN ROW_NUMBER() OVER (ORDER BY PRICE) = COUNT(*) OVER () THEN
                        SUM(STOCK) OVER (ORDER BY PRICE) ELSE NULL END AS cumul_stock FROM Inventory ''')
        value = cursor.fetchall()
        print("Total inventory, ordered by price, with the aggregate sum of our weekly inventory stock:")
        print(value)
    else:
        print("Stock is empty! Check back for Stock statistics when new shipments arrive!")

    print()

    cursor.execute("SELECT * FROM Customer")
    cust_list = cursor.fetchall()
    if(len(cust_list) != 0):
        cursor.execute('''SELECT cust.FIRST_NAME, cust.LAST_NAME, top_cust.ORDER_COUNT FROM Customer cust JOIN 
                       (SELECT CUSTOMER_ID, COUNT(*) AS ORDER_COUNT FROM Orders GROUP BY CUSTOMER_ID ORDER BY COUNT(*) DESC LIMIT 3 ) AS top_cust 
                       ON cust.CUSTOMER_ID = top_cust.CUSTOMER_ID''')
        value = cursor.fetchall()
        print("Top 3 most frequent shoppers + their number of outstanding orders:")
        print(value)

        cursor.execute('''SELECT FIRST_NAME, LAST_NAME, TOTAL_SPENDING FROM 
                       (SELECT C.FIRST_NAME, C.LAST_NAME, COALESCE(SUM(O.PRICE), 0) AS TOTAL_SPENDING FROM 
                       Customer C JOIN Orders O ON C.CUSTOMER_ID = O.CUSTOMER_ID GROUP BY C.CUSTOMER_ID, C.FIRST_NAME, C.LAST_NAME) AS ALIAS''')
        value = cursor.fetchall()
        print("Total outstanding bills per customer with an outstanding bill:")
        print(value)

        cursor.execute('''WITH CUST_SPEND AS (SELECT CUSTOMER_ID, SUM(PRICE) AS TOT_SPENDING FROM Orders GROUP BY CUSTOMER_ID) 
                       SELECT C.FIRST_NAME,C.LAST_NAME,CS.TOT_SPENDING FROM Customer C JOIN CUST_SPEND CS ON C.CUSTOMER_ID = CS.CUSTOMER_ID WHERE CS.TOT_SPENDING > 100''')
        value = cursor.fetchall()
        print("Big spenders! These customers spent over $100 across outstanding orders:")
        print(value)

    else:
        print("No customers available. Be the first to register!")

    print()

    cursor.execute("SELECT * FROM Orders")
    order_list = cursor.fetchall()
    if(len(order_list) != 0):
        cursor.execute("SELECT SUM(PRICE) FROM Orders")
        value = cursor.fetchall()
        print("Total revenue over the past week:")
        print(value)
    else:
        print("No orders available. Be the first to place one!")

def main():

    db = sql.connect(
    host="localhost",
    user="root",
    password="root"
    )

    cursor = db.cursor(buffered=True)
    cursor.execute ("CREATE DATABASE IF NOT EXISTS ChocolateShop")
    cursor.execute ("USE ChocolateShop")

    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer(
    CUSTOMER_ID INT NOT NULL AUTO_INCREMENT,
    FIRST_NAME VARCHAR(20) NOT NULL,
    LAST_NAME VARCHAR(20) NOT NULL,
    ADDRESS VARCHAR(20),
    NUMBER VARCHAR(12),
    PRIMARY KEY (CUSTOMER_ID)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders(
    ORDER_ID INT NOT NULL AUTO_INCREMENT,
    CUSTOMER_ID INT,
    ORDER_LIST VARCHAR(255),
    PRICE DECIMAL(7,2),
    PRIMARY KEY (ORDER_ID),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES Customer(CUSTOMER_ID)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory(
    ITEM_ID INT NOT NULL AUTO_INCREMENT,
    ITEM_NAME VARCHAR(50) NOT NULL,
    STOCK INT,
    PRICE DECIMAL(4,2),
    PRIMARY KEY (ITEM_ID)
    )''')

    category_menu(cursor, db)
main()
