from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk
import sqlite3
import random
import matplotlib.pyplot as plt


def init_db():
    con = None
    try:
        con = sqlite3.connect("Employee.db")
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL
            )
        ''')
        con.commit()
    except Exception as e:
        showerror("Database Error", e)
    finally:
        if con:
            con.close()

init_db()

root = Tk()
root.title("Welcome to WorkVista!")
root.geometry("600x600")


def add_employee():
    form_window = Toplevel(root)
    form_window.title("Add Employees")
    form_window.geometry("500x500")

    f = ("Arial", 14, "bold")

    lbl_id = Label(form_window, text="ID (Auto-generated)", font=f)
    lbl_id.pack(pady=5)

    lbl_name = Label(form_window, text="Enter Name", font=f)
    lbl_name.pack(pady=5)
    ent_name = Entry(form_window, font=f, bd=4)
    ent_name.pack(pady=5)

    lbl_age = Label(form_window, text="Enter Age", font=f)
    lbl_age.pack(pady=5)
    ent_age = Entry(form_window, font=f, bd=4)
    ent_age.pack(pady=5)

    lbl_position = Label(form_window, text="Enter Position", font=f)
    lbl_position.pack(pady=5)
    ent_position = Entry(form_window, font=f, bd=4)
    ent_position.pack(pady=5)

    lbl_salary = Label(form_window, text="Enter Salary", font=f)
    lbl_salary.pack(pady=5)
    ent_salary = Entry(form_window, font=f, bd=4)
    ent_salary.pack(pady=5)

    
    def save_employee():
        name = ent_name.get()
        age = ent_age.get()
        position = ent_position.get()
        salary = ent_salary.get()

        if not name or not age.isdigit() or not position or not salary.replace('.', '', 1).isdigit():
            showerror("Validation Error", "Please enter valid data")
            return

        con = None
        try:
            con = sqlite3.connect("Employee.db")
            cursor = con.cursor()
            sql = "INSERT INTO employees (name, age, position, salary) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (name, age, position, salary))
            con.commit()
            showinfo("Success", "Employee added successfully")
            form_window.destroy()
        except Exception as e:
            showerror("Database Error", e)
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

    btn_save = Button(form_window, text="Save", font=f, command=save_employee)
    btn_save.pack(pady=20)


f = ("Arial", 20, "bold")

btn_add = Button(root, text="Add Employee", font=f, command=add_employee)

def view_employees():
    view_window = Toplevel(root)
    view_window.title("View Employees")
    view_window.geometry("1000x400")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Age", "Position", "Salary"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Position", text="Position")
    tree.heading("Salary", text="Salary")
    tree.pack(fill=BOTH, expand=True)

    con = None
    try:
        con = sqlite3.connect("employee.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", END, values=row)
    except Exception as e:
        showerror("Database Error", e)
    finally:
        if con:
            con.close()

btn_view = Button(root, text="View Employees", font=f, command=view_employees)

def update_employee():
    update_window = Toplevel(root)
    update_window.title("Update Employee")
    update_window.geometry("600x600")

    f = ("Arial", 14, "bold")

    lbl_id = Label(update_window, text="Enter ID to Update", font=f)
    ent_id = Entry(update_window, font=f, bd=4)
    lbl_id.pack(pady=5)
    ent_id.pack(pady=5)

    lbl_name = Label(update_window, text="Enter Name", font=f)
    ent_name = Entry(update_window, font=f, bd=4)
    lbl_name.pack(pady=5)
    ent_name.pack(pady=5)

    lbl_age = Label(update_window, text="Enter Age", font=f)
    ent_age = Entry(update_window, font=f, bd=4)
    lbl_age.pack(pady=5)
    ent_age.pack(pady=5)

    lbl_position = Label(update_window, text="Enter Position", font=f)
    ent_position = Entry(update_window, font=f, bd=4)
    lbl_position.pack(pady=5)
    ent_position.pack(pady=5)

    lbl_salary = Label(update_window, text="Enter Salary", font=f)
    ent_salary = Entry(update_window, font=f, bd=4)
    lbl_salary.pack(pady=5)
    ent_salary.pack(pady=5)

    def update():
        emp_id = ent_id.get()
        name = ent_name.get()
        age = ent_age.get()
        position = ent_position.get()
        salary = ent_salary.get()

        if not emp_id.isdigit() or not name or not age.isdigit() or not position or not salary.replace('.', '', 1).isdigit():
            showerror("Validation Error", "Please enter valid data")
            return

        con = None
        try:
            con = sqlite3.connect("Employee.db")
            cursor = con.cursor()
            sql = "UPDATE employees SET name=?, age=?, position=?, salary=? WHERE id=?"
            cursor.execute(sql, (name, age, position, salary, emp_id))
            con.commit()
            showinfo("Success", "Employee updated successfully")
        except Exception as e:
            showerror("Database Error", e)
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

    btn_update = Button(update_window, text="Update", font=f, command=update)
    btn_update.pack(pady=20)

btn_update = Button(root, text="Update Employee", font=f, command=update_employee)


def delete_employee():
    delete_window = Toplevel(root)
    delete_window.title("Delete Employee")
    delete_window.geometry("400x200")

    f = ("Arial", 14, "bold")

    lbl_id = Label(delete_window, text="Enter ID to Delete", font=f)
    ent_id = Entry(delete_window, font=f, bd=4)
    lbl_id.pack(pady=5)
    ent_id.pack(pady=5)

    def delete():
        emp_id = ent_id.get()

        if not emp_id.isdigit():
            showerror("Validation Error", "Please enter valid ID")
            return

        con = None
        try:
            con = sqlite3.connect("Employee.db")
            cursor = con.cursor()
            sql = "DELETE FROM employees WHERE id=?"
            cursor.execute(sql, (emp_id,))
            con.commit()
            showinfo("Success", "Employee deleted successfully")
        except Exception as e:
            showerror("Database Error", e)
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

    btn_delete = Button(delete_window, text="Delete", font=f, command=delete)
    btn_delete.pack(pady=20)

btn_delete = Button(root, text="Delete Employee", font=f, command=delete_employee)

import seaborn as sns

def show_charts():
    con = None
    try:
        con = sqlite3.connect("Employee.db")
        cursor = con.cursor()

        cursor.execute("SELECT salary FROM employees")
        data = cursor.fetchall()
        salaries = [row[0] for row in data]

        plt.figure(figsize=(10, 6))
        sns.kdeplot(salaries, fill=True, color="blue")
        plt.xlabel('Salary')
        plt.ylabel('Density')
        plt.title('Density Plot of Salary Distribution')
        plt.grid(True)
        plt.show()

    except Exception as e:
        showerror("Database Error", e)
    finally:
        if con:
            con.close()


btn_charts = Button(root, text="Show Charts", font=f, command=show_charts)

btn_add.pack(pady=20)
btn_view.pack(pady=20)
btn_update.pack(pady=20)
btn_delete.pack(pady=20)
btn_charts.pack(pady=20)

quotes = [
    "Keep pushing forward!",
    "Strive for excellence.",
    "Believe in yourself.",
    "Winners never quit, and quitters never win.",
    "When the going gets tough, the tough get going.",
    "The best way to predict the future is to create it."
]

qotd = Label(root, text="Quote of the Day:", font=("Arial", 20, "bold"))
qotd.pack(pady=20)
quote_label = Label(root, text="", font=("Arial", 14), fg="blue")
quote_label.pack(pady=0)

def change_quote():
    quote_label.config(text=random.choice(quotes))
    root.after(10000, change_quote)

change_quote()

root.mainloop()
