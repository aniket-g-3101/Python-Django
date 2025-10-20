🐍 MySQL Python Database Manager

A collection of Python scripts for managing MySQL databases — from simple demos to a full-featured menu-driven system.

⚙️ Requirements

Python 3.x

MySQL Server (running)

MySQL Connector (pip install mysql-connector-python)

🗄️ Default Config
Host: localhost  
User: root  
Password: password  
Database: demo  


📂 Scripts Overview
File	Description	Key Features
demo.py	Basic table creation	Simple emp table demo
mutliple_records.py	Batch record insert	Uses executemany()
dynamic.py	User input insertion	Interactive, dynamic data
first.py	Delete & display data	Basic CRUD example
menuDriven.py	Menu-based DB manager	Full CRUD, table ops, error handling
pro.py	Advanced DB manager	CSV import/export, search, schema view, safe queries
🔒 Security Notes

Avoid hardcoding passwords — use environment variables

Use parameterized queries to prevent SQL injection

Prefer limited-access MySQL users over root

🧠 Learning Path

1️⃣ demo.py → 2️⃣ mutliple_records.py → 3️⃣ dynamic.py → 4️⃣ first.py → 5️⃣ menuDriven.py → 6️⃣ pro.py

💡 Best Practices

Always commit after changes (INSERT, UPDATE, DELETE)

Close DB connections properly

Validate user input

Handle exceptions gracefully

📜 License

Free to use and modify for educational purposes.
