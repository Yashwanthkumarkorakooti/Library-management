# Library-management
How to run
1.	Copy .env.example to .env and update credentials.
2.	Create a Python virtualenv and install requirements:
pip install -r requirements.txt
3.	Run the app:
python main.py


This project is a medium-level rewrite of your console Library management app. It includes:
•	OOP (dataclasses for models)
•	Exception handling
•	MS SQL Server integration using pyodbc
•	SQL table creation and advanced SQL (joins, filters)
•	Search/filter implementation
•	Data mapping between SQL rows and Python objects
•	Database utility and connection management (context managers, basic retry)
•	Console-based user interface


Files

Library_management/
├─ .env.example
├─ requirements.txt
├─ database.py
├─ models.py
├─ repositories.py
├─ services.py
├─ utils.py
└─ main.py
