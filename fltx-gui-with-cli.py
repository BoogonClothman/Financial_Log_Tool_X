"""
Name | Financial Log Tool X GUI --core CLI --flt
Version | 1.2
Author | Boogon Clothman bgc
"""

import tkinter as tk
from tkinter import messagebox
import subprocess


# define fltx function
def fltx(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output


# define fltx method function
# fltx add
def add():
    path = path_entry.get()
    reason = reason_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()
    counterparty = counterparty_entry.get()
    note = note_entry.get()
    file = file_entry.get()

    command = f"fltx add {path} {reason} {amount} -d {date} -cp {counterparty} -n {note} -f {file}"

    blank = []
    if not path:
        blank.append("path")
    if not reason:
        blank.append("reason")
    if not amount:
        blank.append("amount")
    if not date:
        command = command.replace(f" -d {date}", "")
    if not counterparty:
        command = command.replace(f" -cp {counterparty}", "")
    if not note:
        command = command.replace(f" -n {note}", "")
    if not file:
        command = command.replace(f" -f {file}", "")
    if blank:
        msg = "".join(item + ", " for item in blank)
        messagebox.showerror("Fltx add", msg + "not provided")
        return
    output = fltx(command=command)
    text.insert(tk.END, "ADD\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# delete
def delete():
    transaction_id = transaction_id_entry.get()
    file = file_entry.get()

    command = f"fltx delete {transaction_id} -f {file}"
    if not transaction_id:
        messagebox.showerror("Fltx delete", "id not provided")
        return
    if not file:
        command = command.replace(f" -f {file}", "")
    output = fltx(command=command)
    text.insert(tk.END, "DELETE\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# find
def find():
    keyword = keyword_entry.get()
    file = file_entry.get()

    command = f"fltx find {keyword} -f {file}"

    if not keyword:
        messagebox.showerror("Fltx find", "keyword not provided")
        return
    if not file:
        command = command.replace(f" -f {file}", "")

    output = fltx(command=command)
    text.insert(tk.END, "FIND\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# list
def listing():
    file = file_entry.get()

    command = f"fltx list -f {file}"

    if not file:
        command = command.replace(f" -f {file}", "")

    output = fltx(command=command)
    text.insert(tk.END, "LIST\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# modify
def modify():
    transaction_id = transaction_id_entry.get()
    fields = {
        1: "path",
        2: "reason",
        3: "amount",
        4: "counterparty",
        5: "note",
        6: "date"
    }
    field = fields[field_var.get()]
    new = new_entry.get()
    file = file_entry.get()

    command = f"fltx modify {transaction_id} -fd {field} -n {new} -f {file}"

    if not transaction_id:
        messagebox.showerror("Fltx modify", "id not provided")
        return
    if not file:
        command = command.replace(f" -f {file}", "")

    output = fltx(command=command)
    text.insert(tk.END, "MODIFY\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# statistics
def statistics():
    file = file_entry.get()

    command = f"fltx statistics -f {file}"

    if not file:
        command = command.replace(f" -f {file}", "")

    output = fltx(command=command)
    text.insert(tk.END, "STATISTICS\n", "bold")
    text.insert(tk.END, output+"\n")
    text.see(tk.END)


# define show function
# add
def show_add():
    global state
    state = "add"
    global win, path_entry, reason_entry, amount_entry, date_entry, counterparty_entry, note_entry, file_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    path_label = tk.Label(win, text="path")
    path_label.grid(row=0, column=0)
    path_entry = tk.Entry(win)
    path_entry.grid(row=0, column=1)

    reason_label = tk.Label(win, text="reason")
    reason_label.grid(row=1, column=0)
    reason_entry = tk.Entry(win)
    reason_entry.grid(row=1, column=1)

    amount_label = tk.Label(win, text="amount")
    amount_label.grid(row=2, column=0)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=2, column=1)

    date_label = tk.Label(win, text="date")
    date_label.grid(row=3, column=0)
    date_entry = tk.Entry(win)
    date_entry.grid(row=3, column=1)

    counterparty_label = tk.Label(win, text="counterparty")
    counterparty_label.grid(row=4, column=0)
    counterparty_entry = tk.Entry(win)
    counterparty_entry.grid(row=4, column=1)

    note_label = tk.Label(win, text="note")
    note_label.grid(row=5, column=0)
    note_entry = tk.Entry(win)
    note_entry.grid(row=5, column=1)

    file_label = tk.Label(win, text="file")
    file_label.grid(row=6, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=6, column=1)


# delete
def show_delete():
    global state
    state = "delete"
    global win, transaction_id_entry, file_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    transaction_id_label = tk.Label(win, text="id")
    transaction_id_label.grid(row=0, column=0)
    transaction_id_entry = tk.Entry(win)
    transaction_id_entry.grid(row=0, column=1)

    file_label = tk.Label(win, text="file")
    file_label.grid(row=1, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=1, column=1)


# find
def show_find():
    global state
    state = "find"
    global win, keyword_entry, file_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    keyword_label = tk.Label(win, text="keyword")
    keyword_label.grid(row=0, column=0)
    keyword_entry = tk.Entry(win)
    keyword_entry.grid(row=0, column=1)

    file_label = tk.Label(win, text="file")
    file_label.grid(row=1, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=1, column=1)


# list
def show_list():
    global state
    state = "list"
    global win, file_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    file_label = tk.Label(win, text="file")
    file_label.grid(row=0, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=0, column=1)


# modify
def show_modify():
    global state
    state = "modify"
    global win, transaction_id_entry, file_entry, field_var, new_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    transaction_id_label = tk.Label(win, text="id")
    transaction_id_label.grid(row=0, column=0)
    transaction_id_entry = tk.Entry(win)
    transaction_id_entry.grid(row=0, column=1)

    file_label = tk.Label(win, text="file")
    file_label.grid(row=3, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=3, column=1)

    win2 = tk.Frame(win)
    win2.grid(row=1, column=1)
    field_label = tk.Label(win, text="field")
    field_label.grid(row=1, column=0)
    field_var = tk.IntVar(value=1)
    field_1 = tk.Radiobutton(win2, text="path", variable=field_var, value=1)
    field_1.grid(row=0, column=1)
    field_2 = tk.Radiobutton(win2, text="reason", variable=field_var, value=2)
    field_2.grid(row=0, column=2)
    field_3 = tk.Radiobutton(win2, text="amount", variable=field_var, value=3)
    field_3.grid(row=0, column=3)
    field_4 = tk.Radiobutton(win2, text="counterparty", variable=field_var, value=4)
    field_4.grid(row=0, column=4)
    field_5 = tk.Radiobutton(win2, text="note", variable=field_var, value=5)
    field_5.grid(row=0, column=5)
    field_6 = tk.Radiobutton(win2, text="date", variable=field_var, value=6)
    field_6.grid(row=0, column=6)

    new_label = tk.Label(win, text="new")
    new_label.grid(row=2, column=0)
    new_entry = tk.Entry(win)
    new_entry.grid(row=2, column=1)


# statistics
def show_statistics():
    global state
    state = "statistics"
    global win, file_entry
    if win.winfo_exists:
        win.destroy()
    win = tk.Frame(arg_frame)
    win.pack()

    file_label = tk.Label(win, text="file")
    file_label.grid(row=0, column=0)
    file_entry = tk.Entry(win)
    file_entry.grid(row=0, column=1)


# define submit function
def submit():
    global state
    if state == "add":
        add()
    elif state == "delete":
        delete()
    elif state == "find":
        find()
    elif state == "list":
        listing()
    elif state == "modify":
        modify()
    elif state == "statistics":
        statistics()
    else:
        messagebox.showerror("Fltx submit", message="method not chosen")


# set root window
root = tk.Tk()
root.title("Financial Log Tool GUI --core CLI v1.2.01")
root.resizable(False, False)

# set frame
command_frame = tk.Frame(root)
command_frame.grid(row=0)
arg_frame = tk.Frame(root)
arg_frame.grid(row=1)
win = tk.Frame(arg_frame)
win.pack()
out = tk.Frame(root)
out.grid(row=2)

# set button
add_button = tk.Button(command_frame, text="ADD", command=show_add)
add_button.grid(row=0, column=0)
delete_button = tk.Button(command_frame, text="DELETE", command=show_delete)
delete_button.grid(row=0, column=1)
find_button = tk.Button(command_frame, text="FIND", command=show_find)
find_button.grid(row=0, column=2)
list_button = tk.Button(command_frame, text="LIST", command=show_list)
list_button.grid(row=0, column=3)
modify_button = tk.Button(command_frame, text="MODIFY", command=show_modify)
modify_button.grid(row=0, column=4)
statistics_button = tk.Button(command_frame, text="STATISTICS", command=show_statistics)
statistics_button.grid(row=0, column=5)
state = None
submit_button = tk.Button(command_frame, text="SUBMIT", command=submit)
submit_button.grid(row=0, column=6)

# set output line
text = tk.Text(out, height=20, width=80)
text.tag_configure("bold", font=("Consolas", 10, "bold"))
text.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(out)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=text.yview)

# mainloop
root.mainloop()
