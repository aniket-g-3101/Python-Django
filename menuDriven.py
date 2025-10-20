import mysql.connector as m
from mysql.connector import Error

while True :
    try :
         p = input("Enter Password Of System: ")
         conn = m.connect(host="localhost",user="root",password=p,database=None)
         print("Connected successfully ..!")
         break
    except :
        print("Wrong Password >> Try Again .... ")
c1 = conn.cursor()
q1="show databases"
c1.execute(q1)
print("DataBases On System : ")
for i in c1.fetchall():
    print(i[0])

db=input("Choose Database To Use :")
q2=f"use {db} "
c1.execute(q2)
print("Current Database ---> ",db)
conn=m.connect(host="localhost", user="root", password=p, database=db)
c1 = conn.cursor()

print("Available Tables On DataBase : ")
q="show tables"
c1.execute(q)
for i in c1.fetchall():
    print(i[0])


table = input("Enter Table Name to Use/Create: ")


def safe_execute(query, params=None, fetch=False):
    try:
        if params:
            c1.execute(query, params)
        else:
            c1.execute(query)
        if fetch:
            return c1.fetchall()
        conn.commit()
        return True
    except Error as err:
        if err.errno == 1146:  # Table does not exist
            print(f"Error: Table '{table}' does not exist.")
        return None


def create():
    global table  
    n = int(input("How Many Fields/Columns You Want In Table: "))
    attribute = []
    for i in range(n):
        fname = input(f"Enter Name for Field {i+1}: ")
        dtype = input(f"Enter Data Type for {fname} (e.g., int , char(10)): ")
        attribute.append(f"{fname} {dtype}")
    column_definitions = ", ".join(attribute)
    q1 = f"CREATE TABLE {table} ({column_definitions})"
    if safe_execute(q1):
        print(f"Table '{table}' created successfully.")


def insert():
    global table
    columns = safe_execute(f"SHOW COLUMNS FROM {table}", fetch=True)
    if not columns:
        return
    col_names = [col[0] for col in columns]
    num_records = int(input("How Many Records to Insert: "))
    data = []
    for _ in range(num_records):
        record = [input(f"Enter value for {col}: ") for col in col_names]
        data.append(tuple(record))
    placeholders = ", ".join(["%s"] * len(col_names))
    q2 = f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({placeholders})"
    if safe_execute(q2, data[0] if len(data) == 1 else None):
        c1.executemany(q2, data)
        conn.commit()
        print(f"{num_records} record(s) inserted successfully.")


def display():
    global table
    rows = safe_execute(f"SELECT * FROM {table}", fetch=True)
    if not rows:
        print("No records found or table does not exist.")
        return
    columns = safe_execute(f"SHOW COLUMNS FROM {table}", fetch=True)
    if columns:
        col_names = [col[0] for col in columns]
        print("\t".join(col_names))
        for row in rows:
            print("\t".join(str(val) for val in row))

def update():
    global table
    columns = safe_execute(f"SHOW COLUMNS FROM {table}", fetch=True)
    if not columns:
        return
    col_names = [col[0] for col in columns]
    print("Columns:", ", ".join(col_names))
    update_col = input("Enter column name to update: ")
    if update_col not in col_names:
        print("Invalid column name.")
        return
    condition_col = input("Enter column name for condition: ")
    if condition_col not in col_names:
        print("Invalid column name.")
        return
    condition_val = input(f"Enter target value from {condition_col}: ")
    new_val = input(f"Enter new value for {update_col}: ")
    query = f"UPDATE {table} SET {update_col} = %s WHERE {condition_col} = %s"
    if safe_execute(query, (new_val, condition_val)):
        if c1.rowcount > 0:
            print("Record updated successfully!")
        else:
            print("No matching record found.")


def delete():
    global table
    columns = safe_execute(f"SHOW COLUMNS FROM {table}", fetch=True)
    if not columns:
        return
    col_names = [col[0] for col in columns]
    print("Columns:", ", ".join(col_names))
    condition_col = input("Enter column name: ")
    if condition_col not in col_names:
        print("Invalid column name.")
        return
    condition_val = input("Enter value to delete: ")
    query = f"DELETE FROM {table} WHERE {condition_col} = %s"
    if safe_execute(query, (condition_val,)):
        if c1.rowcount > 0:
            print("Record deleted successfully!")
        else:
            print("No matching record found.")


def del_table():
    global table
    q1 = f"DROP TABLE {table}"
    if safe_execute(q1):
        print("Table Deleted Successfully.")

def show_tables():
    rows = safe_execute("SHOW TABLES", fetch=True)
    if rows is None:
        return
    print("Tables in database:")
    for r in rows:
        print("---", r[0])


while True:
    ch= input("\n1.Create Table\n2. Insert Records\n3. Display Records\n4. Update Record\n5. Delete Record\n6. Delete Whole Table\n7. Show All Tables From Database \n8.Exit\nEnter your choice: ")
    if ch == "1":
        create()
    elif ch == "2":
        insert()
    elif ch == "3":
        display()
    elif ch == "4":
        update()
    elif ch == "5":
        delete()
    elif ch == "6":
        del_table()
    elif ch == "7":
        show_tables()
    elif ch=="8":
        break
    else:
        print("Invalid choice!")

conn.close()
