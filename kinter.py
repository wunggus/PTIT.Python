import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import csv
from datetime import datetime
import os
import pandas as pd

root = tk.Tk()
root.title("Save Data with Options and Age")
root.geometry("500x800")

CSV_FILE = "DATANew.csv"
EXCEL_FILE = "SortbyAge.xlsx"

fields = ["Mã", "Tên", "Đơn vị", "Chức danh", "Số CMND", "Nơi cấp", "Sinh", "Age", "Type", "Gender"]
entries = {}

for i, field in enumerate(fields[:6]):
    label = tk.Label(root, text=f"Enter {field}:")
    label.pack(pady=5)
    
    entry = tk.Entry(root)
    entry.pack(pady=5)
    entries[field] = entry

birthday_label = tk.Label(root, text="Select Sinh (Birthday):")
birthday_label.pack(pady=10)

birthday_calendar = Calendar(root, selectmode='day', year=2000, month=1, day=1)
birthday_calendar.pack(pady=10)

type_label = tk.Label(root, text="Type:")
type_label.pack(pady=10)

type_var = tk.IntVar()
type_var.set(0)

R1 = tk.Radiobutton(root, text="Khách hàng", variable=type_var, value=1)
R1.pack(pady=5)
R2 = tk.Radiobutton(root, text="Cung cấp", variable=type_var, value=2)
R2.pack(pady=5)

gender_label = tk.Label(root, text="Gender:")
gender_label.pack(pady=10)

gender_var = tk.IntVar()
gender_var.set(0)

R3 = tk.Radiobutton(root, text="Nam", variable=gender_var, value=3)
R3.pack(pady=5)
R4 = tk.Radiobutton(root, text="Nữ", variable=gender_var, value=4)
R4.pack(pady=5)

def calculate_age(birthday_str):
    birth_date = datetime.strptime(birthday_str, "%m/%d/%y")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def save_to_csv():
    user_data = {}
    for field, entry in entries.items():
        value = entry.get().strip()
        if not value:
            messagebox.showerror("Input Error", f"The '{field}' field is required!")
            return
        user_data[field] = value
    
    birthday = birthday_calendar.get_date()
    user_data["Sinh"] = birthday

    try:
        age = calculate_age(birthday)
        user_data["Age"] = age
    except Exception as e:
        messagebox.showerror("Error", f"Could not calculate age: {e}")
        return

    type_value = type_var.get()
    gender_value = gender_var.get()

    if type_value == 0:
        messagebox.showerror("Input Error", "Please select a Type (Khách hàng or Cung cấp)!")
        return
    if gender_value == 0:
        messagebox.showerror("Input Error", "Please select a Gender (Nam or Nữ)!")
        return

    type_mapping = {1: "Khách hàng", 2: "Cung cấp"}
    gender_mapping = {3: "Nam", 4: "Nữ"}
    user_data["Type"] = type_mapping[type_value]
    user_data["Gender"] = gender_mapping[gender_value]

    try:
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(fields)

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_data[field] for field in fields])
        
        messagebox.showinfo("Success", f"Data saved to {CSV_FILE}!")
        
        for entry in entries.values():
            entry.delete(0, tk.END)
        birthday_calendar.selection_set("2000-01-01")
        type_var.set(0)
        gender_var.set(0)
    except Exception as e:
        messagebox.showerror("Error", f"error: {e}")


def sortbirthday():
    if not os.path.exists(CSV_FILE):
        messagebox.showerror("Error", "No data")
        return

    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        
        df_sorted = df.sort_values(by="Age", ascending=False)
        
        df_sorted.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        
        messagebox.showinfo("Success", f"done")
    except Exception as e:
        messagebox.showerror("Error", f"failed")

def display_current_birthdays():
    if not os.path.exists(CSV_FILE):
        messagebox.showerror("Error", "No data")
        return

    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        today = datetime.today().strftime("%m/%d")
        
        current_birthdays = df[df['Sinh'].str.startswith(today)]
        
        if current_birthdays.empty:
            messagebox.showinfo("No Birthdays", "No birthdays today.")
        else:
            birthday_list = current_birthdays[['Tên', 'Sinh']] 
            birthday_text = "\n".join(f"{row['Tên']} - {row['Sinh']}" for _, row in birthday_list.iterrows())
            messagebox.showinfo("Snhat", birthday_text)
    except Exception as e:
        messagebox.showerror("Error", f"error")

save_button = tk.Button(root, text="Lưu", command=save_to_csv)
save_button.pack(pady=20)

xds_button = tk.Button(root, text="Xuất danh sách", command=sortbirthday)
xds_button.pack(pady=20)

birthday_button = tk.Button(root, text="Sinh nhat hom nay", command=display_current_birthdays)
birthday_button.pack(pady=20)

root.mainloop()
