import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Main Window
root = tk.Tk()
root.title("CRM and Project Management System")
root.geometry("1000x700")

# Connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="crm_db"  # Ensure this database exists
    )

# Create tables if they do not exist
def create_tables():
    db = connect_to_db()
    cursor = db.cursor()

    # Create CRM tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_code VARCHAR(50),
        entity_type VARCHAR(50),
        account_type VARCHAR(50),
        business_description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business (
        id INT AUTO_INCREMENT PRIMARY KEY,
        industry VARCHAR(50),
        sector VARCHAR(50),
        market VARCHAR(50),
        region VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connectivity (
        id INT AUTO_INCREMENT PRIMARY KEY,
        board_line VARCHAR(50),
        relationship_partner_manager VARCHAR(50),
        account_manager VARCHAR(50),
        lead_category VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS address (
        id INT AUTO_INCREMENT PRIMARY KEY,
        address_type VARCHAR(50),
        address1 VARCHAR(100),
        address2 VARCHAR(100),
        city VARCHAR(50),
        state_province VARCHAR(50),
        zip_postal_code VARCHAR(20)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact (
        id INT AUTO_INCREMENT PRIMARY KEY,
        contact_code VARCHAR(50),
        contact_person VARCHAR(100),
        designation VARCHAR(100),
        account_name VARCHAR(100),
        contact_partner VARCHAR(100),
        email_id VARCHAR(100),
        mobile_no VARCHAR(15),
        city VARCHAR(50)
    )
    """)

    # Create Project tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        employee_name VARCHAR(255) NOT NULL,
        department VARCHAR(255) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Project (
        project_id INT AUTO_INCREMENT PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        employee_id INT NOT NULL,
        department VARCHAR(255) NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CostRevenue (
    project_id INT NOT NULL,
    estimated_cost DECIMAL(10, 2) NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    profit DECIMAL(10, 2) AS (revenue - estimated_cost) STORED,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProjectDetails (
        project_id INT AUTO_INCREMENT PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        employee_id INT NOT NULL,
        department VARCHAR(255) NOT NULL,
        estimated_cost DECIMAL(10, 2) NOT NULL,
        revenue DECIMAL(10, 2) NOT NULL,
        profit DECIMAL(10, 2) AS (revenue - estimated_cost) STORED,
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
    )
    ''')

    db.commit()
    cursor.close()
    db.close()

# Function to validate numeric input for cost and revenue
def validate_float(entry_value, entry_name):
    try:
        return float(entry_value)
    except ValueError:
        messagebox.showerror("Input Error", f"Please enter a valid number for {entry_name}.")
        return None

# Function to save data to database
def save_data():
    db = connect_to_db()
    cursor = db.cursor()

    try:
        # Insert Account Details
        cursor.execute("""
        INSERT INTO account (account_code, entity_type, account_type, business_description)
        VALUES (%s, %s, %s, %s)
        """, (entry_account_code.get(), entity_type.get(), account_type.get(), entry_business_description.get()))

        # Insert Business Details
        cursor.execute("""
        INSERT INTO business (industry, sector, market, region)
        VALUES (%s, %s, %s, %s)
        """, (industry.get(), sector.get(), market.get(), region.get()))

        # Insert Connectivity Details
        cursor.execute("""
        INSERT INTO connectivity (board_line, relationship_partner_manager, account_manager, lead_category)
        VALUES (%s, %s, %s, %s)
        """, (entry_board_line.get(), entry_relationship_partner_manager.get(), entry_account_manager.get(), lead_category.get()))

        # Insert Address Details
        cursor.execute("""
        INSERT INTO address (address_type, address1, address2, city, state_province, zip_postal_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (address_type.get(), entry_address1.get(), entry_address2.get(), entry_city.get(), entry_state_province.get(), entry_zip_postal_code.get()))

        # Insert Contact Details
        cursor.execute("""
        INSERT INTO contact (contact_code, contact_person, designation, account_name, contact_partner, email_id, mobile_no, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (entry_contact_code.get(), entry_contact_person.get(), entry_designation.get(), entry_account_name.get(), entry_contact_partner.get(), entry_email_id.get(), entry_mobile_no.get(), entry_contact_city.get()))

        # Insert Employee Details
        cursor.execute("""
        INSERT INTO Employee (employee_name, department)
        VALUES (%s, %s)
        """, (entry_employee_name.get(), entry_role.get()))  # Assuming role is the department

        # Get the employee_id of the newly inserted employee
        cursor.execute("SELECT employee_id FROM Employee WHERE employee_name = %s", (entry_employee_name.get(),))
        employee_id = cursor.fetchone()[0]

        # Insert Project Details with the fetched employee_id
        cursor.execute("""
        INSERT INTO ProjectDetails (project_name, employee_id, department, estimated_cost, revenue)
        VALUES (%s, %s, %s, %s, %s)
        """, (entry_project_name.get(), employee_id, entry_role.get(), float(entry_estimated_cost.get()), float(entry_revenue.get())))

        db.commit()
        messagebox.showinfo("Success", "Data saved successfully")
        display_data()  # Call the function to display data after saving

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        db.rollback()

    cursor.close()
    db.close()
# Function to reset all fields
def reset_fields():
    # Reset Contact Details
    entry_contact_code.delete(0, tk.END)
    entry_contact_person.delete(0, tk.END)
    entry_designation.delete(0, tk.END)
    entry_account_name.delete(0, tk.END)
    entry_contact_partner.delete(0, tk.END)
    entry_email_id.delete(0, tk.END)
    entry_mobile_no.delete(0, tk.END)
    entry_contact_city.delete(0, tk.END)

    # Reset Account & Other Details
    entry_account_code.delete(0, tk.END)
    entity_type.set('')
    account_type.set('')
    entry_business_description.delete(0, tk.END)
    industry.set('')
    sector.set('')
    market.set('')
    region.set('')
    entry_board_line.delete(0, tk.END)
    entry_relationship_partner_manager.delete(0, tk.END)
    entry_account_manager.delete(0, tk.END)
    lead_category.set('')
    address_type.set('')
    entry_address1.delete(0, tk.END)
    entry_address2.delete(0, tk.END)
    entry_city.delete(0, tk.END)
    entry_state_province.delete(0, tk.END)
    entry_zip_postal_code.delete(0, tk.END)

    # Clear Treeview
    for tree in [account_tree, contact_tree, project_tree]:
        for item in tree.get_children():
            tree.delete(item)

# Function to display data in Treeview format
def display_data():
    db = connect_to_db()
    cursor = db.cursor()

    # Clear Treeview
    for tree in [account_tree, contact_tree, project_tree]:
        for item in tree.get_children():
            tree.delete(item)

    try:
        # Display Account Details
        cursor.execute("SELECT * FROM account")
        for row in cursor.fetchall():
            account_tree.insert("", tk.END, values=row[1:])

        # Display Contact Details
        cursor.execute("SELECT * FROM contact")
        for row in cursor.fetchall():
            contact_tree.insert("", tk.END, values=row[1:])

        # Display Project Details with Cost and Revenue
        cursor.execute("""
        SELECT P.project_name, E.employee_name, P.department, P.estimated_cost, P.revenue, P.profit
        FROM ProjectDetails P
        LEFT JOIN Employee E ON P.employee_id = E.employee_id
        """)
        for row in cursor.fetchall():
            project_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    cursor.close()
    db.close()
# Create tables initially
create_tables()

# Create a main frame for the canvas and scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas and scrollbar
canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a horizontal scrollbar
hsb = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
hsb.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(xscrollcommand=hsb.set)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Notebook for organizing the different frames (tabs)
notebook = ttk.Notebook(scrollable_frame)
notebook.pack(expand=True, fill='both')

contact_frame = ttk.Frame(notebook)
notebook.add(contact_frame, text="Contact Details")


# Labels and Entries for Contact Details
tk.Label(contact_frame, text="Contact Code:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_contact_code = tk.Entry(contact_frame)
entry_contact_code.grid(row=0, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Contact Person:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_contact_person = tk.Entry(contact_frame)
entry_contact_person.grid(row=1, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Designation:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_designation = tk.Entry(contact_frame)
entry_designation.grid(row=2, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Account Name:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_account_name = tk.Entry(contact_frame)
entry_account_name.grid(row=3, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Contact Partner:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
entry_contact_partner = tk.Entry(contact_frame)
entry_contact_partner.grid(row=4, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Email ID:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
entry_email_id = tk.Entry(contact_frame)
entry_email_id.grid(row=5, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="Mobile No.:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
entry_mobile_no = tk.Entry(contact_frame)
entry_mobile_no.grid(row=6, column=1, padx=5, pady=5)

tk.Label(contact_frame, text="City:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
entry_contact_city = tk.Entry(contact_frame)
entry_contact_city.grid(row=7, column=1, padx=5, pady=5)

# Treeview to display saved Contact Details
columns = ("Contact Code", "Contact Person", "Designation", "Account Name", "Contact Partner", "Email ID", "Mobile No", "City")

# Creating the Treeview widget
contact_tree = ttk.Treeview(contact_frame, columns=columns, show='headings')

# Define headings and set column width
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=120, anchor=tk.W)  # Adjust width as per need

# Place Treeview in the grid
contact_tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Add scrollbar for Treeview
contact_tree_scrollbar = ttk.Scrollbar(contact_frame, orient="vertical", command=contact_tree.yview)
contact_tree.configure(yscrollcommand=contact_tree_scrollbar.set)
contact_tree_scrollbar.grid(row=8, column=2, sticky='ns')

# Configure grid layout to allow resizing
contact_frame.grid_rowconfigure(8, weight=1)
contact_frame.grid_columnconfigure(1, weight=1)


# Tab 2: Account & Business Details Frame
account_frame = ttk.Frame(notebook)
notebook.add(account_frame, text="Account & Business Details")

tk.Label(account_frame, text="Account Code:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_account_code = tk.Entry(account_frame)
entry_account_code.grid(row=0, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Entity Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entity_type = ttk.Combobox(account_frame, values=["Individual", "Company"])
entity_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Account Type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
account_type = ttk.Combobox(account_frame, values=["Client", "Vendor", "Partner"])
account_type.grid(row=2, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Business Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_business_description = tk.Entry(account_frame)
entry_business_description.grid(row=3, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Industry:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
industry = ttk.Combobox(account_frame, values=["Technology", "Healthcare", "Finance"])
industry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Sector:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
sector = ttk.Combobox(account_frame, values=["Public", "Private"])
sector.grid(row=5, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Market:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
market = ttk.Combobox(account_frame, values=["Local", "International"])
market.grid(row=6, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Region:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
region = ttk.Combobox(account_frame, values=["North", "South", "East", "West"])
region.grid(row=7, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Board Line:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
entry_board_line = tk.Entry(account_frame)
entry_board_line.grid(row=8, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Relationship Partner Manager:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
entry_relationship_partner_manager = tk.Entry(account_frame)
entry_relationship_partner_manager.grid(row=9, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Account Manager:").grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
entry_account_manager = tk.Entry(account_frame)
entry_account_manager.grid(row=10, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Lead Category:").grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)
lead_category = ttk.Combobox(account_frame, values=["Cold", "Warm", "Hot"])
lead_category.grid(row=11, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Address Type:").grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)
address_type = ttk.Combobox(account_frame, values=["Office", "Home"])
address_type.grid(row=12, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Address 1:").grid(row=13, column=0, padx=5, pady=5, sticky=tk.W)
entry_address1 = tk.Entry(account_frame)
entry_address1.grid(row=13, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Address 2:").grid(row=14, column=0, padx=5, pady=5, sticky=tk.W)
entry_address2 = tk.Entry(account_frame)
entry_address2.grid(row=14, column=1, padx=5, pady=5)

tk.Label(account_frame, text="City:").grid(row=15, column=0, padx=5, pady=5, sticky=tk.W)
entry_city = tk.Entry(account_frame)
entry_city.grid(row=15, column=1, padx=5, pady=5)

tk.Label(account_frame, text="State/Province:").grid(row=16, column=0, padx=5, pady=5, sticky=tk.W)
entry_state_province = tk.Entry(account_frame)
entry_state_province.grid(row=16, column=1, padx=5, pady=5)

tk.Label(account_frame, text="Zip/Postal Code:").grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
entry_zip_postal_code = tk.Entry(account_frame)
entry_zip_postal_code.grid(row=17, column=1, padx=5, pady=5)

# Account Treeview
account_tree = ttk.Treeview(account_frame, columns=("Account Code", "Entity Type", "Account Type", "Business Description", "Industry", "Sector", "Market", "Region", "Board Line", "Relationship Partner Manager", "Account Manager", "Lead Category", "Address Type", "Address 1", "Address 2", "City", "State/Province", "Zip/Postal Code"), show='headings')
account_tree.grid(row=18, column=0, columnspan=2, padx=5, pady=5)

for col in ("Account Code", "Entity Type", "Account Type", "Business Description", "Industry", "Sector", "Market", "Region", "Board Line", "Relationship Partner Manager", "Account Manager", "Lead Category", "Address Type", "Address 1", "Address 2", "City", "State/Province", "Zip/Postal Code"):
    account_tree.heading(col, text=col.replace("_", " ").title())
    account_tree.column(col, width=100)

project_frame = ttk.Frame(notebook)
notebook.add(project_frame, text="Project Management")

# Labels and Entry fields for project details
tk.Label(project_frame, text="Project Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_project_name = tk.Entry(project_frame)
entry_project_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(project_frame, text="Employee Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_employee_name = tk.Entry(project_frame)
entry_employee_name.grid(row=1, column=1, padx=5, pady=5)

tk.Label(project_frame, text="Role/Department:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_role = tk.Entry(project_frame)
entry_role.grid(row=2, column=1, padx=5, pady=5)

tk.Label(project_frame, text="Estimated Cost:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_estimated_cost = tk.Entry(project_frame)
entry_estimated_cost.grid(row=3, column=1, padx=5, pady=5)

tk.Label(project_frame, text="Revenue:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
entry_revenue = tk.Entry(project_frame)
entry_revenue.grid(row=4, column=1, padx=5, pady=5)

# Treeview for displaying projects

project_tree = ttk.Treeview(project_frame, columns=("Project Name", "Employee", "Department", "Cost", "Revenue", "Profit"), show='headings')
project_tree.grid(row=6, column=0,columnspan=2, padx=5, pady=5,sticky="nsew")



for col in ("Project Name", "Employee", "Department", "Cost", "Revenue", "Profit"):
    project_tree.heading(col, text=col.replace("_", " ").title())
    project_tree.column(col, width=230)
    project_frame.grid_rowconfigure(6, weight=1)
    project_frame.grid_columnconfigure(0, weight=0)
    project_frame.grid_columnconfigure(0, weight=0)




tk.Button(root, text="Save", command=save_data).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(root, text="Reset", command=reset_fields).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(root, text="Display Data", command=display_data).pack(side=tk.LEFT, padx=5, pady=5)



root.mainloop()
 
