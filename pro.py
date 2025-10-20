# db_manager.py
import mysql.connector as m
from mysql.connector import Error
import csv
import sys

# ----- CONFIG: change if needed -----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "demo"
}
# ------------------------------------

try:
    conn = m.connect(**DB_CONFIG)
    c1 = conn.cursor()
except Error as e:
    print("Could not connect to database:", e)
    sys.exit(1)

current_table = None

def safe_execute(query, params=None, fetch=False):
    try:
        if params is not None:
            c1.execute(query, params)
        else:
            c1.execute(query)
        if fetch:
            return c1.fetchall()
        conn.commit()
        return True
    except Error as err:
        if hasattr(err, "errno") and err.errno == 1146:  # table doesn't exist
            print("Error: table does not exist.")
        else:
            print("MySQL Error:", err)
        return None

def set_table():
    global current_table
    t = input("Enter table name to use: ").strip()
    if not t:
        print("No table name entered.")
        return
    current_table = t
    print("Current table set to:", current_table)

def show_tables():
    rows = safe_execute("SHOW TABLES", fetch=True)
    if rows is None:
        return
    print("Tables in database:")
    for r in rows:
        print("-", r[0])

def create_table():
    global current_table
    name = input("Enter new table name: ").strip()
    if not name:
        print("Table name required.")
        return
    try:
        n = int(input("How many columns: "))
    except ValueError:
        print("Enter a valid number.")
        return
    cols = []
    for i in range(n):
        col_name = input(f" Column {i+1} name: ").strip()
        col_type = input(f" Column {i+1} type (e.g., INT, VARCHAR(50)): ").strip()
        if not col_name or not col_type:
            print("Column name and type required.")
            return
        cols.append(f"{col_name} {col_type}")
    q = f"CREATE TABLE {name} ({', '.join(cols)})"
    if safe_execute(q):
        print("Table created:", name)
        current_table = name

def describe_table():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    cols = safe_execute(f"DESCRIBE {current_table}", fetch=True)
    if not cols:
        return
    print("Columns:")
    for row in cols:
        print(row[0], row[1])

def insert_records():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    if not cols:
        return
    col_names = [c[0] for c in cols]
    try:
        rows = int(input("How many records to insert: "))
    except ValueError:
        print("Invalid number.")
        return
    data = []
    for r in range(rows):
        print(f"Record {r+1}:")
        record = []
        for col in col_names:
            v = input(f"  {col} (leave empty for NULL): ")
            if v == "":
                record.append(None)
            else:
                record.append(v)
        data.append(tuple(record))
    placeholders = ", ".join(["%s"] * len(col_names))
    q = f"INSERT INTO {current_table} ({', '.join(col_names)}) VALUES ({placeholders})"
    try:
        c1.executemany(q, data)
        conn.commit()
        print(f"{c1.rowcount} record(s) inserted.")
    except Error as e:
        print("Insert failed:", e)

def display_records():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    rows = safe_execute(f"SELECT * FROM {current_table}", fetch=True)
    if rows is None:
        return
    if not rows:
        print("No records found.")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    col_names = [c[0] for c in cols]
    print("\t".join(col_names))
    for r in rows:
        print("\t".join(str(x) if x is not None else "NULL" for x in r))

def search_records():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    if not cols:
        return
    col_names = [c[0] for c in cols]
    print("Columns:", ", ".join(col_names))
    col = input("Search column: ").strip()
    if col not in col_names:
        print("Invalid column.")
        return
    val = input("Search value (uses LIKE, use % as wildcard): ").strip()
    q = f"SELECT * FROM {current_table} WHERE {col} LIKE %s"
    rows = safe_execute(q, (val,), fetch=True)
    if rows is None:
        return
    if not rows:
        print("No matching rows.")
        return
    print("\t".join(col_names))
    for r in rows:
        print("\t".join(str(x) if x is not None else "NULL" for x in r))

def update_record():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    if not cols:
        return
    col_names = [c[0] for c in cols]
    print("Columns:", ", ".join(col_names))
    upd_col = input("Enter column to update: ").strip()
    if upd_col not in col_names:
        print("Invalid column.")
        return
    new_val = input(f"New value for {upd_col}: ")
    cond_col = input("Condition column (which column to match): ").strip()
    if cond_col not in col_names:
        print("Invalid column.")
        return
    cond_val = input(f"Condition value for {cond_col}: ")
    q = f"UPDATE {current_table} SET {upd_col} = %s WHERE {cond_col} = %s"
    res = safe_execute(q, (new_val, cond_val))
    if res is None:
        return
    if c1.rowcount > 0:
        print(f"{c1.rowcount} record(s) updated.")
    else:
        print("No matching records updated.")

def delete_record():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    if not cols:
        return
    col_names = [c[0] for c in cols]
    print("Columns:", ", ".join(col_names))
    cond_col = input("Condition column: ").strip()
    if cond_col not in col_names:
        print("Invalid column.")
        return
    cond_val = input("Condition value: ")
    q = f"DELETE FROM {current_table} WHERE {cond_col} = %s"
    res = safe_execute(q, (cond_val,))
    if res is None:
        return
    if c1.rowcount > 0:
        print(f"{c1.rowcount} record(s) deleted.")
    else:
        print("No matching records deleted.")

def export_csv():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    rows = safe_execute(f"SELECT * FROM {current_table}", fetch=True)
    if rows is None:
        return
    if not rows:
        print("No data to export.")
        return
    cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
    col_names = [c[0] for c in cols]
    fname = input("Enter filename to export (e.g., out.csv): ").strip()
    if not fname:
        print("Filename required.")
        return
    try:
        with open(fname, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            for r in rows:
                writer.writerow([x if x is not None else "" for x in r])
        print("Exported to", fname)
    except Exception as e:
        print("Export failed:", e)

def import_csv():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    fname = input("Enter CSV filename to import: ").strip()
    if not fname:
        print("Filename required.")
        return
    try:
        with open(fname, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            cols = safe_execute(f"SHOW COLUMNS FROM {current_table}", fetch=True)
            if not cols:
                return
            col_names = [c[0] for c in cols]
            # simple check: headers must match some of table columns
            if not all(h in col_names for h in headers):
                print("CSV headers do not match table columns.")
                return
            placeholders = ", ".join(["%s"] * len(headers))
            q = f"INSERT INTO {current_table} ({', '.join(headers)}) VALUES ({placeholders})"
            data = []
            for row in reader:
                # pad/trim row to headers length
                row = row[:len(headers)] + [""] * max(0, len(headers) - len(row))
                data.append(tuple(row))
            if data:
                c1.executemany(q, data)
                conn.commit()
                print(f"Imported {c1.rowcount} rows from {fname}.")
            else:
                print("No data in CSV.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Import failed:", e)

def drop_table():
    global current_table
    if not current_table:
        print("Set a table first (option 3).")
        return
    confirm = input(f"Type YES to drop table {current_table}: ")
    if confirm == "YES":
        q = f"DROP TABLE {current_table}"
        if safe_execute(q):
            print("Table dropped.")
            current_table = None
    else:
        print("Drop cancelled.")

def exit_program():
    try:
        c1.close()
        conn.close()
    except:
        pass
    print("Goodbye.")
    sys.exit(0)

# ----- Main menu loop -----
def menu():
    while True:
        print("""
1) Create table
2) Show tables
3) Set / Change current table
4) Describe current table
5) Insert records
6) Display records
7) Search records
8) Update record
9) Delete record
10) Export table to CSV
11) Import CSV to table
12) Drop current table
13) Exit
Current table: {}
""".format(current_table))
        choice = input("Enter choice: ").strip()
        if choice == "1":
            create_table()
        elif choice == "2":
            show_tables()
        elif choice == "3":
            set_table()
        elif choice == "4":
            describe_table()
        elif choice == "5":
            insert_records()
        elif choice == "6":
            display_records()
        elif choice == "7":
            search_records()
        elif choice == "8":
            update_record()
        elif choice == "9":
            delete_record()
        elif choice == "10":
            export_csv()
        elif choice == "11":
            import_csv()
        elif choice == "12":
            drop_table()
        elif choice == "13":
            exit_program()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        exit_program()
