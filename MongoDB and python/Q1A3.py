# Question question 1 ASSIGNMENT 3
import sqlite3
import matplotlib.pyplot as plt
import time
import random

connection = None
cursor = None


def bar_chart(y1, y2, y3, a1, a2, a3, b1, b2, b3, title, x_label, y_label):
    x = ['Small']
    n = ['Medium']
    m = ['Large']
    plt.bar(x, y1, color='b')
    plt.bar(x, y2, bottom=y1, color='r')
    plt.bar(x, y3, bottom=y1 + y2, color='y')
    plt.bar(n, a1, color='b')
    plt.bar(n, a2, bottom=a1, color='r')
    plt.bar(n, a3, bottom=a1 + a2, color='y')
    plt.bar(m, b1, color='b')
    plt.bar(m, b2, bottom=b1, color='r')
    plt.bar(m, b3, bottom=b1 + b2, color='y')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(["Uninformed", "Self-optimized ", "User-optimized"])
    path = './{}_barchart2.png'.format(title)
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    plt.close()
    return

def main():
    global connection
    # connecting to small data base
    db_path = './A3Small.db'
    global connection, cursor
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    ##################### Setting scenario “Uninformed”###################################################################
    cursor.execute(' PRAGMA automatic_index=False;')
    cursor.execute(' PRAGMA foreign_keys=OFF; ')
    cursor.execute("DROP TABLE IF EXISTS NEW_Customers")
    cursor.execute('''CREATE TABLE "NEW_Customers" ( "customer_id"	TEXT,"customer_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Customers SELECT customer_id,customer_postal_code FROM Customers;''')
    cursor.execute(''' ALTER TABLE Customers RENAME TO CustomersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Customers RENAME TO Customers;''')
    cursor.execute(''' CREATE TABLE "NEW_Sellers" ("seller_id"	TEXT,"seller_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Sellers SELECT seller_id,seller_postal_code FROM Sellers;''')
    cursor.execute(''' ALTER TABLE  Sellers RENAME TO SellersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Sellers RENAME TO Sellers ;''')
    cursor.execute('''CREATE TABLE "NEW_Orders" ("order_id"	TEXT,"customer_id"	TEXT);''')
    cursor.execute('''INSERT INTO NEW_Orders SELECT order_id,customer_id FROM Orders ;''')
    cursor.execute('''ALTER TABLE Orders  RENAME TO OrdersOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Orders RENAME TO Orders ;''')
    cursor.execute('''CREATE TABLE "NEW_Order_items" ("order_id"	TEXT,"order_item_id"	INTEGER,
        "product_id"	TEXT,"seller_id"	TEXT); ''')
    cursor.execute('''INSERT INTO NEW_Order_items SELECT order_id, order_item_id,product_id,seller_id FROM 
        Order_items ;''')
    cursor.execute('''ALTER TABLE Order_items  RENAME TO Order_itemsOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Order_items RENAME TO Order_items ;''')
    small_uninformed_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                FROM Customers c, Orders o
                WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        small_uninformed_runtime.append(end - start)
        connection.commit()
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute('''DROP TABLE Sellers;''')
    cursor.execute('''ALTER TABLE SellersOriginal RENAME TO Sellers;''')
    cursor.execute('''DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    cursor.execute('''DROP TABLE Order_items;''')
    cursor.execute('''ALTER TABLE Order_itemsOriginal RENAME TO Order_items;''')
    connection.close()
    # Self-optimization for small - changes to constraints
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    small_self_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                FROM Customers c, Orders o
                WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        small_self_runtime.append(end - start)
        connection.commit()
    connection.close()

    # user- optimized for small database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    cursor.execute("DROP INDEX IF EXISTS c;")
    # cursor.execute("DROP INDEX c")
    cursor.execute("CREATE INDEX c ON Customers ( customer_postal_code );")
    cursor.execute("DROP INDEX IF EXISTS o")
    cursor.execute("CREATE INDEX o ON Orders ( customer_id );")
    connection.commit()
    small_user_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                        FROM Customers c, Orders o
                        WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        small_user_runtime.append(end - start)
        connection.commit()
    connection.close()
    print(small_uninformed_runtime)
    print(small_self_runtime)
    print(small_user_runtime)

    # using medium database
    # connecting to medium
    db_path = './A3Medium.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # Setting scenario “Uninformed” for medium
    cursor.execute(' PRAGMA automatic_index=False;')
    cursor.execute(' PRAGMA foreign_keys=OFF; ')
    cursor.execute("DROP TABLE IF EXISTS NEW_Customers")
    cursor.execute('''CREATE TABLE "NEW_Customers" ( "customer_id"	TEXT,"customer_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Customers SELECT customer_id,customer_postal_code FROM Customers;''')
    cursor.execute(''' ALTER TABLE Customers RENAME TO CustomersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Customers RENAME TO Customers;''')
    cursor.execute(''' CREATE TABLE "NEW_Sellers" ("seller_id"	TEXT,"seller_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Sellers SELECT seller_id,seller_postal_code FROM Sellers;''')
    cursor.execute(''' ALTER TABLE  Sellers RENAME TO SellersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Sellers RENAME TO Sellers ;''')
    cursor.execute('''CREATE TABLE "NEW_Orders" ("order_id"	TEXT,"customer_id"	TEXT);''')
    cursor.execute('''INSERT INTO NEW_Orders SELECT order_id,customer_id FROM Orders ;''')
    cursor.execute('''ALTER TABLE Orders  RENAME TO OrdersOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Orders RENAME TO Orders ;''')
    cursor.execute('''CREATE TABLE "NEW_Order_items" ("order_id"	TEXT,"order_item_id"	INTEGER,
                "product_id"	TEXT,"seller_id"	TEXT); ''')
    cursor.execute('''INSERT INTO NEW_Order_items SELECT order_id, order_item_id,product_id,seller_id FROM 
                Order_items ;''')
    cursor.execute('''ALTER TABLE Order_items  RENAME TO Order_itemsOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Order_items RENAME TO Order_items ;''')
    med_uninformed_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                        FROM Customers c, Orders o
                        WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        med_uninformed_runtime.append(end - start)
        connection.commit()
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute('''DROP TABLE Sellers;''')
    cursor.execute('''ALTER TABLE SellersOriginal RENAME TO Sellers;''')
    cursor.execute('''DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    cursor.execute('''DROP TABLE Order_items;''')
    cursor.execute('''ALTER TABLE Order_itemsOriginal RENAME TO Order_items;''')
    connection.close()
    # Self-optimization - changes to constraints for medium database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    med_self_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                        FROM Customers c, Orders o
                        WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        med_self_runtime.append(end - start)
        connection.commit()
    connection.close()

    # user- optimized for medium database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    cursor.execute("DROP INDEX IF EXISTS c;")
    # cursor.execute("DROP INDEX c")
    cursor.execute("CREATE INDEX c ON Customers ( customer_postal_code );")
    cursor.execute("DROP INDEX IF EXISTS o")
    cursor.execute("CREATE INDEX o ON Orders ( customer_id );")
    connection.commit()
    med_user_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                                FROM Customers c, Orders o
                                WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        med_user_runtime.append(end - start)
        connection.commit()
    connection.close()
    print(med_uninformed_runtime)
    print(med_self_runtime)
    print(med_user_runtime)

    # connecting to A3LARGE
    db_path = './A3Large.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # Setting scenario “Uninformed” for large database
    cursor.execute(' PRAGMA automatic_index=False;')
    cursor.execute(' PRAGMA foreign_keys=OFF; ')
    cursor.execute("DROP TABLE IF EXISTS NEW_Customers")
    cursor.execute('''CREATE TABLE "NEW_Customers" ( "customer_id"	TEXT,"customer_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Customers SELECT customer_id,customer_postal_code FROM Customers;''')
    cursor.execute(''' ALTER TABLE Customers RENAME TO CustomersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Customers RENAME TO Customers;''')
    cursor.execute(''' CREATE TABLE "NEW_Sellers" ("seller_id"	TEXT,"seller_postal_code"	INTEGER);''')
    cursor.execute(''' INSERT INTO NEW_Sellers SELECT seller_id,seller_postal_code FROM Sellers;''')
    cursor.execute(''' ALTER TABLE  Sellers RENAME TO SellersOriginal; ''')
    cursor.execute(''' ALTER TABLE NEW_Sellers RENAME TO Sellers ;''')
    cursor.execute('''CREATE TABLE "NEW_Orders" ("order_id"	TEXT,"customer_id"	TEXT);''')
    cursor.execute('''INSERT INTO NEW_Orders SELECT order_id,customer_id FROM Orders ;''')
    cursor.execute('''ALTER TABLE Orders  RENAME TO OrdersOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Orders RENAME TO Orders ;''')
    cursor.execute('''CREATE TABLE "NEW_Order_items" ("order_id"	TEXT,"order_item_id"	INTEGER,
                "product_id"	TEXT,"seller_id"	TEXT); ''')
    cursor.execute('''INSERT INTO NEW_Order_items SELECT order_id, order_item_id,product_id,seller_id FROM 
                Order_items ;''')
    cursor.execute('''ALTER TABLE Order_items  RENAME TO Order_itemsOriginal; ''')
    cursor.execute('''ALTER TABLE NEW_Order_items RENAME TO Order_items ;''')
    lar_uninformed_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                        FROM Customers c, Orders o
                        WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        lar_uninformed_runtime.append(end - start)
        connection.commit()
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute('''DROP TABLE Sellers;''')
    cursor.execute('''ALTER TABLE SellersOriginal RENAME TO Sellers;''')
    cursor.execute('''DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    cursor.execute('''DROP TABLE Order_items;''')
    cursor.execute('''ALTER TABLE Order_itemsOriginal RENAME TO Order_items;''')
    connection.close()
    # Self-optimization - changes to constraints for large database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    lar_self_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                        FROM Customers c, Orders o
                        WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        lar_self_runtime.append(end - start)
        connection.commit()
    connection.close()

    # user- optimized for large database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE;')
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    cursor.execute("DROP INDEX IF EXISTS c;")
    # cursor.execute("DROP INDEX c")
    cursor.execute("CREATE INDEX c ON Customers ( customer_postal_code );")
    cursor.execute("DROP INDEX IF EXISTS o")
    cursor.execute("CREATE INDEX o ON Orders ( customer_id );")
    connection.commit()
    lar_user_runtime = []
    for i in range(50):
        start = time.perf_counter()
        cursor.execute("SELECT customer_postal_code FROM Customers Order by random() limit 1")
        rows = cursor.fetchone()
        ra = rows[0]
        q = '''SELECT COUNT(*)
                                FROM Customers c, Orders o
                                WHERE c.customer_id= o.customer_id AND customer_postal_code= :random_postal_code;'''
        cursor.execute(q, {'random_postal_code': ra})
        rows = cursor.fetchall()
        print(rows[0])
        end = time.perf_counter()
        lar_user_runtime.append(end - start)
        connection.commit()
    connection.close()
    print(lar_uninformed_runtime)
    print(lar_self_runtime)
    print(lar_user_runtime)
    n = 1000
    bar_chart((sum(small_uninformed_runtime)) * n / 50, (sum(small_self_runtime)) * n / 50,
              (sum(small_user_runtime)) * n / 50, (sum(med_uninformed_runtime)) * n / 50,
              (sum(med_self_runtime)) * n / 50,
              (sum(med_user_runtime)) * n / 50, (sum(lar_uninformed_runtime)) * n / 50,
              (sum(lar_self_runtime)) * n / 50,
              (sum(lar_user_runtime)) * n / 50, "Running time for Query 1", "Different Databases",
              "Running time in milli-second")


if __name__ == "__main__":
    main()
