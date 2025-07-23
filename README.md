# Customer-Relationship-Management

🎯 Project Summary:
The CRM and Project Management System is a unified platform designed to manage customer relationship data and project workflows efficiently. The application combines CRM functionalities (contact, account, address, business, etc.) with project management features like employee assignment, budgeting (cost, revenue), and profit calculation.

It enables users to:

Store and view client & contact information

Track business and connectivity details

Manage employees and projects

Automatically calculate project profitability

Display data in a structured UI using Treeviews

🧩 Key Modules:
1. CRM Section:
Account Management: Manage account type, business description, industry, etc.

Contact Management: Maintain client contact details (email, phone, etc.)

Address Handling: Store multiple address types per client

Business & Connectivity Details: Capture sector, market, and lead information

2. Project Management Section:
Employee Module: Store employee data linked with projects

Project Module: Store project name, department, employee, costs, revenue

Profit Calculation: Auto-calculated using SQL stored column logic

3. UI/UX:
Organized using ttk.Notebook tabs

User-friendly forms and dropdowns

Dynamic data display using ttk.Treeview

🛠️ Tech Stack Used
Component	Technology
Frontend (UI)	Python tkinter + ttk widgets
Backend	Python (mysql.connector for DB connection)
Database	MySQL (local server, default or port 8080)
SQL Operations	DDL (CREATE), DML (INSERT, SELECT), calculated columns
Data Display	ttk.Treeview (for structured table view)
Error Handling	try-except, messagebox for user feedback
Local Deployment	Standalone Python application (.py script)
