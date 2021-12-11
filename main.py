import datetime

from Product_ID import products
from Unit import Unit
from BrandsID import BrandsId


dbname = input("Database name: ")
user = input("User name: ")
password = input("password: ")
port = int(input("port, Default[5432]: "))

cond = True
while cond:

    # Stage one
    start_time = datetime.datetime.now()
    start_time = start_time.strftime("%H:%M:%S")

    print("Start product class")
    op_one = products(dbname, user, password, port)
    print("End product class")

    # Stage two
    print("Start brand class")
    op_two = BrandsId(dbname, user, password, port)
    print("End brand class")

    # Stage three
    print("Start unit class")
    op_three = Unit(dbname, user, password, port)
    print("End unit class")

    end_time = datetime.datetime.now()
    end_time = end_time.strftime("%H:%M:%S")
    print(f"The process start at:{start_time}\nfinish at:{end_time}")

    exit()
