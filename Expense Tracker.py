import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
import sqlite3

class ExpenseListWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("List of Expenses")
        self.window.configure(bg="#1C1C1C")

        self.listbox = Listbox(self.window, width=80, height=10, bg="#363636", fg="white")
        self.listbox.pack(padx=10, pady=10)

        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.load_expenses()

    def load_expenses(self):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM expenses''')
        rows = c.fetchall()
        conn.close()

        for row in rows:
            expense_info = f"{row[1]} | {row[2]} | ${row[3]} | {row[4]}"
            self.listbox.insert(tk.END, expense_info)

def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()

    if date and category and amount:
        try:
            amount = float(amount)
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            c.execute('''INSERT INTO expenses (date, category, amount, description)
                         VALUES (?, ?, ?, ?)''', (date, category, amount, description))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Expense added successfully!")
            clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Amount should be a number.")
    else:
        messagebox.showerror("Error", "Please fill in all required fields.")

def clear_entries():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# Initialize Tkinter window
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg="#1C1C1C")

# GUI elements
label_date = tk.Label(root, text="Date (YYYY-MM-DD):", bg="#1C1C1C", fg="white")
label_date.pack(pady=(10, 0))
entry_date = tk.Entry(root, bg="#363636", fg="white", insertbackground="white")
entry_date.pack(ipady=4)

label_category = tk.Label(root, text="Category:", bg="#1C1C1C", fg="white")
label_category.pack(pady=(10, 0))
entry_category = tk.Entry(root, bg="#363636", fg="white", insertbackground="white")
entry_category.pack(ipady=4)

label_amount = tk.Label(root, text="Amount:", bg="#1C1C1C", fg="white")
label_amount.pack(pady=(10, 0))
entry_amount = tk.Entry(root, bg="#363636", fg="white", insertbackground="white")
entry_amount.pack(ipady=4)

label_description = tk.Label(root, text="Description:", bg="#1C1C1C", fg="white")
label_description.pack(pady=(10, 0))
entry_description = tk.Entry(root, bg="#363636", fg="white", insertbackground="white")
entry_description.pack(ipady=4)

button_add = tk.Button(root, text="Add Expense", bg="#006400", fg="white", command=add_expense)
button_add.pack(pady=(20, 10), ipadx=10, ipady=5)

button_clear = tk.Button(root, text="Clear Entries", bg="#8B0000", fg="white", command=clear_entries)
button_clear.pack(ipadx=10, ipady=5)

button_show = tk.Button(root, text="Show Expenses", bg="#1E90FF", fg="white", command=lambda: ExpenseListWindow(root))
button_show.pack(ipadx=10, ipady=5)

# Run the Tkinter main loop
root.mainloop()
