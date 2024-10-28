import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import re

# Initialize main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x550")
root.configure(bg="#f0f8ff")

# Database setup
connection = sqlite3.connect('management.db')
TABLE_NAME = "management_table"
STUDENT_ID = "student_id"
STUDENT_NAME = "student_name"
STUDENT_COLLEGE = "student_college"
STUDENT_ADDRESS = "student_address"
STUDENT_PHONE = "student_phone"
STUDENT_EMAIL = "student_email"
STUDENT_DOB = "student_dob"

# Add new columns if they don't exist
try:
    connection.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {STUDENT_EMAIL} TEXT")
    connection.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {STUDENT_DOB} TEXT")
except sqlite3.OperationalError:
    pass  # Columns already exist

connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {STUDENT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
        {STUDENT_NAME} TEXT,
        {STUDENT_COLLEGE} TEXT,
        {STUDENT_ADDRESS} TEXT,
        {STUDENT_PHONE} TEXT,
        {STUDENT_EMAIL} TEXT,
        {STUDENT_DOB} TEXT
    );
""")

# Header label
appLabel = tk.Label(
    root, text="Student Management System",
    fg="#00688b", bg="#f0f8ff", font=("Arial", 24, "bold")
)
appLabel.pack(pady=(20, 0))

# Input Frame
input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=10)

# Input labels and entry fields
fields = ["Name", "College", "Phone", "Address", "Email", "Date of Birth"]
entries = {}

for i, field in enumerate(fields):
    label = tk.Label(input_frame, text=f"Enter your {field.lower()}:", bg="#f0f8ff", font=("Arial", 12), anchor="w")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    
    # Date of Birth uses DateEntry widget
    if field == "Date of Birth":
        entry = DateEntry(input_frame, width=28, background="darkblue", foreground="white", date_pattern='dd/mm/yyyy')
    else:
        entry = tk.Entry(input_frame, width=30)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[field] = entry

# Functions to handle database operations
def validate_phone(phone):
    # Check if the phone number contains exactly 10 digits
    return bool(re.fullmatch(r'\d{10}', phone))

def add_student():
    try:
        data = {field: entry.get() for field, entry in entries.items()}
        
        # Validate phone number
        if not validate_phone(data["Phone"]):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits.")
            return
        
        # Insert data into database
        connection.execute(f"""
            INSERT INTO {TABLE_NAME} ({STUDENT_NAME}, {STUDENT_COLLEGE}, {STUDENT_PHONE}, {STUDENT_ADDRESS}, {STUDENT_EMAIL}, {STUDENT_DOB})
            VALUES ('{data["Name"]}', '{data["College"]}', '{data["Phone"]}', '{data["Address"]}', '{data["Email"]}', '{data["Date of Birth"]}')
        """)
        connection.commit()
        
        # Clear input fields
        for entry in entries.values():
            entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Data saved successfully.")
        display_data()
    except Exception as e:
        messagebox.showerror("Error", f"Could not add student: {e}")

def delete_student():
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item)["values"][0]
        connection.execute(f"DELETE FROM {TABLE_NAME} WHERE {STUDENT_ID} = ?", (student_id,))
        connection.commit()
        display_data()
        messagebox.showinfo("Success", "Student deleted successfully.")
    else:
        messagebox.showwarning("Warning", "Select a student to delete.")

def display_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor = connection.execute(f"SELECT * FROM {TABLE_NAME}")
    for row in cursor:
        tree.insert("", tk.END, values=row)

# Buttons for submitting, displaying, and deleting data
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Student", command=add_student, width=15, bg="#00688b", fg="white", font=("Arial", 12, "bold"))
add_button.grid(row=0, column=0, padx=5, pady=10)

delete_button = tk.Button(button_frame, text="Delete Student", command=delete_student, width=15, bg="#ff6347", fg="white", font=("Arial", 12, "bold"))
delete_button.grid(row=0, column=1, padx=5, pady=10)

# Treeview for displaying student data
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "College", "Phone", "Address", "Email", "DOB"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("College", text="College")
tree.heading("Phone", text="Phone")
tree.heading("Address", text="Address")
tree.heading("Email", text="Email")
tree.heading("DOB", text="DOB")

tree.column("ID", width=30)
tree.column("Name", width=100)
tree.column("College", width=100)
tree.column("Phone", width=80)
tree.column("Address", width=100)
tree.column("Email", width=100)
tree.column("DOB", width=80)

tree.pack()

display_data()

# Start the main loop
root.mainloop()
