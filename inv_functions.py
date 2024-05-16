def get_itemname():
    itemname = input("Enter the item's name:\n>")
    return itemname

def get_stock():
    stock = input("How much of this item is in stock?\n>")
    return stock

def get_price():
    price = input("What is this item's price?\n>")
    return price

def list_inventory(cursor):
    cursor.execute("SELECT * FROM Inventory")
    inv_list = cursor.fetchall()
    if(len(inv_list) != 0):
        print("Item ID | Item Name | Stock | Price")
        print(inv_list)
    else:
        print("Inventory list is empty!")

def add_item(cursor):

    item_name=get_itemname()
    stock=get_stock()
    price=get_price()

    data = (item_name, stock, price)

    cursor.execute("INSERT INTO Inventory(item_name, stock, price) VALUES (%s, %s, %s)", data)

def remove_item(cursor):
    cursor.execute("SELECT * FROM Inventory")
    item_list = cursor.fetchall()
    if(len(item_list) != 0):
        id = input("\nPlease note you will not be able to recover deleted item data. Please enter the ID of the item you'd like to delete: \n> ")

        cursor.execute("SELECT * FROM Inventory WHERE ITEM_ID = (%s)", (id,))
        item_list = cursor.fetchall()
        if(len(item_list) != 0):
            cursor.execute("DELETE FROM Inventory WHERE ITEM_ID = (%s)", (id,))
        else:
            print("ID not found!")
    else:
        print("Item list is empty!")
    
def update_item(cursor):
    cursor.execute("SELECT * FROM Inventory")
    inv_list = cursor.fetchall()
    if(len(inv_list) != 0):
        inv_id = input("Enter item ID: \n> ")
        cursor.execute("SELECT * FROM Inventory WHERE ITEM_ID = (%s)", (inv_id,))
        inv_list = cursor.fetchall()
        if(len(inv_list) != 0):
            print("Item with ID", inv_id, "found.")

            attribute = input(f"Enter attribute to update: ITEM_NAME, STOCK, PRICE\n> ")
            
            match attribute.upper():

                case "ITEM_NAME":
                    value = get_itemname()
                    cursor.execute('''UPDATE Inventory
                                   SET ITEM_NAME = (%s)''', (value,))
                case "STOCK":
                    value = get_stock()
                    cursor.execute('''UPDATE Inventory
                                   SET STOCK = (%s)''', (value,))
                case "PRICE":
                    value = get_price()
                    cursor.execute('''UPDATE Inventory
                                   SET PRICE = (%s)''', (value,))
                case _:
                    print("Not a valid attribute!")
        else:
            print("ID not found!")
    else:
        print("Item list is empty!")
