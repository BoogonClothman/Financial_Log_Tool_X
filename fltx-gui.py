"""
Name | Financial Log Tool X GUI --fltx
Version | 1.3
Author | Boogon Clothman --bgc
"""
import decimal
import tkinter
from tkinter import messagebox
import json
import os
import datetime
import pprint
from decimal import Decimal


def load_bills(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file=file_name, mode='r', encoding="utf-8") as f:
        return json.load(f)


def save_bills(file_name, bills):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(bills, f, indent=4, ensure_ascii=False)


def get_next_transaction_id(bills):
    if not bills:
        return 1
    return max(bill['id'] for bill in bills) + 1


def add_transaction(file_name, reason, amount, date, path, counterparty, note):
    bills = load_bills(file_name)
    transaction_id = get_next_transaction_id(bills)
    try:
        amount = Decimal(amount).quantize(Decimal("0.01"))
    except decimal.InvalidOperation:
        messagebox.showerror(title="ADD",
                             message="Argument Error:\nAmount Argument only supports number.")
        return "[Argument Error] Amount Argument only supports number."

    transaction = {
        'id': transaction_id,
        'date': date,
        'reason': reason,
        'amount': str(amount),
        'path': path,
        'counterparty': counterparty,
        'note': note
    }
    bills.append(transaction)
    save_bills(file_name, bills)
    return f"Added transaction with ID {transaction_id}.\n"


def delete_transaction(file_name, transaction_id):
    bills = load_bills(file_name)
    bills = [bill for bill in bills if bill['id'] != int(transaction_id)]
    for bill in bills:
        if bill['id'] > int(transaction_id):
            bill['id'] -= 1
    save_bills(file_name, bills)
    return f"Deleted transaction with ID {transaction_id}.\n"


def find_transactions(file_name, keyword):
    bills = load_bills(file_name)
    keyword = keyword.lower()
    found_bills = [bill for bill in bills if keyword in bill['reason'].lower() or
                   keyword in (bill['counterparty'] or '').lower() or
                   str(bill['amount']).lower() == keyword or
                   str(bill['id']).lower() == keyword or
                   keyword in (bill['note'] or '').lower() or
                   keyword in bill["path"].lower()]

    text = ""
    if found_bills:
        text += "Found transactions:\n"
        for bill in found_bills:
            formatted_bill = pprint.pformat(bill)
            text += formatted_bill + "\n\n"
    else:
        text += f"No transactions found for keyword '{keyword}'\n."

    return text


def modify_transaction(file_name, transaction_id, field, new):
    bills = load_bills(file_name)
    for bill in bills:
        if bill['id'] == int(transaction_id):
            if field == 'amount':
                new = str(Decimal(new).quantize(Decimal("0.01")))
            else:
                new = str(new)
            bill[field] = new
            save_bills(file_name, bills)
            return f"Modified transaction with ID {transaction_id}. New {field}: {new}"
    return f"Transaction with ID {transaction_id} not found."


def list_transactions(file_name):
    bills = load_bills(file_name)
    text = ""
    if bills:
        text += "Transactions:\n\n"
        for bill in bills:
            text += pprint.pformat(bill)+"\n\n"
    else:
        text += "No transactions.\n"

    return text


def statistics(file_name):
    wallet_sta = {}
    bills = load_bills(file_name)
    total_income = Decimal("0")
    total_expense = Decimal("0")

    for bill in bills:
        wallet_id = bill["path"]
        if wallet_id not in wallet_sta:
            wallet_sta[wallet_id] = {"income": Decimal("0"), "expense": Decimal("0")}

        amount = Decimal(bill["amount"]).quantize(Decimal("0.00"))

        if amount > Decimal("0"):
            wallet_sta[wallet_id]["income"] += amount
            total_income += amount
        else:
            wallet_sta[wallet_id]["expense"] += amount
            total_expense += amount

    net = total_income + total_expense
    text = ""
    for wallet_id, wallet_data in wallet_sta.items():
        text += f"Wallet:{wallet_id}\n"
        text += f"    Total Income: {wallet_data['income']}\n"
        text += f"    Total Expense: {wallet_data['expense']}\n\n"

    text += "Overall\n"
    text += f"    Total Income: {total_income}\n"
    text += f"    Total Expense: {total_expense}\n"
    text += f"    Net Income: {net}\n"

    return text


def show_add():
    global state, arg_frame
    state = "add"
    global path_entry, reason_entry, amount_entry, date_entry, cp_entry, note_entry, year_entry, month_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # path
    path_label = tkinter.Label(arg_frame, text="Path")
    path_label.grid(row=0, column=0)
    path_entry = tkinter.Entry(arg_frame)
    path_entry.grid(row=0, column=1)
    # reason
    reason_label = tkinter.Label(arg_frame, text="Reason")
    reason_label.grid(row=1, column=0)
    reason_entry = tkinter.Entry(arg_frame)
    reason_entry.grid(row=1, column=1)
    # amount
    amount_label = tkinter.Label(arg_frame, text="Amount")
    amount_label.grid(row=2, column=0)
    amount_entry = tkinter.Entry(arg_frame)
    amount_entry.grid(row=2, column=1)
    # date
    date_label = tkinter.Label(arg_frame, text="Date")
    date_label.grid(row=3, column=0)
    date_entry = tkinter.Entry(arg_frame)
    date_entry.grid(row=3, column=1)
    # counterparty
    cp_label = tkinter.Label(arg_frame, text="Counterparty")
    cp_label.grid(row=4, column=0)
    cp_entry = tkinter.Entry(arg_frame)
    cp_entry.grid(row=4, column=1)
    # note
    note_label = tkinter.Label(arg_frame, text="Note")
    note_label.grid(row=5, column=0)
    note_entry = tkinter.Entry(arg_frame)
    note_entry.grid(row=5, column=1)
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=6, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=6, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)


def show_delete():
    global state, arg_frame
    state = "delete"
    global id_entry, year_entry, month_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # transaction id
    id_label = tkinter.Label(arg_frame, text="Transaction ID")
    id_label.grid(row=0, column=0)
    id_entry = tkinter.Entry(arg_frame, width=6)
    id_entry.grid(row=0, column=1)
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=1, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=1, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)


def show_find():
    global arg_frame, state
    state = "find"
    global kw_entry, year_entry, month_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # keyword
    kw_label = tkinter.Label(arg_frame, text="Keyword")
    kw_label.grid(row=0, column=0)
    kw_entry = tkinter.Entry(arg_frame)
    kw_entry.grid(row=0, column=1)
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=1, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=1, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)


def show_list():
    global arg_frame, state
    state = "list"
    global year_entry, month_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=0, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=0, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)


def show_modify():
    global arg_frame, state
    state = "modify"
    global id_entry, year_entry, month_entry, field_var, new_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # transaction id
    id_label = tkinter.Label(arg_frame, text="Transaction Id")
    id_label.grid(row=0, column=0)
    id_entry = tkinter.Entry(arg_frame, width=6)
    id_entry.grid(row=0, column=1)
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=1, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=1, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)
    # field
    field_label = tkinter.Label(arg_frame, text="Field")
    field_label.grid(row=2, column=0)
    field_frame = tkinter.Frame(arg_frame)
    field_frame.grid(row=2, column=1)
    field_var = tkinter.StringVar(value="path")
    field_path = tkinter.Radiobutton(field_frame, text="Path", variable=field_var, value="path")
    field_path.grid(row=0, column=0)
    field_reason = tkinter.Radiobutton(field_frame, text="Reason", variable=field_var, value="reason")
    field_reason.grid(row=0, column=1)
    field_amount = tkinter.Radiobutton(field_frame, text="Amount", variable=field_var, value="amount")
    field_amount.grid(row=0, column=2)
    field_date = tkinter.Radiobutton(field_frame, text="Date", variable=field_var, value="time")
    field_date.grid(row=0, column=3)
    field_cp = tkinter.Radiobutton(field_frame, text="Counterparty", variable=field_var, value="counterparty")
    field_cp.grid(row=0, column=4)
    field_note = tkinter.Radiobutton(field_frame, text="Note", variable=field_var, value="note")
    field_note.grid(row=0, column=5)
    # new
    new_label = tkinter.Label(arg_frame, text="New")
    new_label.grid(row=3, column=0)
    new_entry = tkinter.Entry(arg_frame)
    new_entry.grid(row=3, column=1)


def show_statistics():
    global arg_frame, state
    state = "statistics"
    global year_entry, month_entry
    # If arg_frame exists?
    if arg_frame.winfo_exists():
        arg_frame.destroy()
    arg_frame = tkinter.Frame(arg_area)
    arg_frame.pack()

    # label and entry
    # file
    file_label = tkinter.Label(arg_frame, text="File")
    file_label.grid(row=0, column=0)
    file_frame = tkinter.Frame(arg_frame)
    file_frame.grid(row=0, column=1)
    year_entry = tkinter.Entry(file_frame, width=6)
    year_entry.grid(row=0, column=0)
    month_entry = tkinter.Entry(file_frame, width=6)
    month_entry.grid(row=0, column=1)


def add():
    path = path_entry.get()
    reason = reason_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()
    counterparty = cp_entry.get()
    note = note_entry.get()
    year = year_entry.get()
    month = month_entry.get()

    blank_arguments = []
    # path
    if not path:
        blank_arguments.append("path")
    # reason
    elif not reason:
        blank_arguments.append("reason")
    # amount
    elif not amount:
        blank_arguments.append("amount")
    # date
    elif not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    # counterparty
    elif not counterparty:
        counterparty = None
    # note
    elif not note:
        note = None
    # blank arguments
    if blank_arguments:
        msg = "".join(item + ", " for item in blank_arguments)
        messagebox.showerror(title="ADD",
                             message="Argument Error:\n" + msg + "will be expected.\nThese arguments are necessary.")
        return f"[Argument Error] {msg} will be expected."

    # year and month
    if (not year) and month:
        messagebox.showerror(title="ADD",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="ADD",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return add_transaction(
        file_name=file_name,
        path=path,
        reason=reason,
        amount=amount,
        date=date,
        counterparty=counterparty,
        note=note
    )


def delete():
    transaction_id = id_entry.get()
    year = year_entry.get()
    month = month_entry.get()

    # transaction id
    if not transaction_id:
        messagebox.showerror(title="DELETE",
                             message="Argument Error:\nId Argument is expected.\nThis argument is necessary.")
        return "[Argument Error] Id Argument is expected."
    # year and month
    if (not year) and month:
        messagebox.showerror(title="DELETE",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="DELETE",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return delete_transaction(
        file_name=file_name,
        transaction_id=transaction_id
    )


def find():
    kw = kw_entry.get()
    year = year_entry.get()
    month = month_entry.get()

    # keyword
    if not kw:
        messagebox.showerror(title="FIND",
                             message="Argument Error:\nKeyword Argument is expected.")
        return "[Argument Error] Keyword Argument is expected."
    # year and month
    if (not year) and month:
        messagebox.showerror(title="FIND",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="FIND",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return find_transactions(
        file_name=file_name,
        keyword=kw
    )


def modify():
    transaction_id = id_entry.get()
    field = field_var.get()
    new = new_entry.get()
    year = year_entry.get()
    month = month_entry.get()

    # transaction id
    if not transaction_id:
        messagebox.showerror(title="MODIFY",
                             message="Argument Error:\nId Argument is expected.")
        return "[Argument Error] Id Argument is expected."
    # new
    elif not new:
        new = None
    # year and month
    if (not year) and month:
        messagebox.showerror(title="MODIFY",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="MODIFY",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return modify_transaction(
        file_name=file_name,
        transaction_id=transaction_id,
        field=field,
        new=new
    )


def listall():
    year = year_entry.get()
    month = month_entry.get()

    # year and month
    if (not year) and month:
        messagebox.showerror(title="LIST",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="LIST",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return list_transactions(
        file_name=file_name
    )


def statistic():
    year = year_entry.get()
    month = month_entry.get()

    # year and month
    if (not year) and month:
        messagebox.showerror(title="STATISTICS",
                             message="Argument Error:\nYear Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Year Argument is expected.\nDouble blanks mean the time now."
    elif year and (not month):
        messagebox.showerror(title="STATISTICS",
                             message="Argument Error:\nMonth Argument is expected.\nDouble blanks mean the time now.")
        return "[Argument Error] Month Argument is expected.\nDouble blanks mean the time now."
    if not year:
        year = datetime.datetime.now().year
    if not month:
        month = datetime.datetime.now().month

    file_name = f"sheet-{year}-{month}.json"
    return statistics(
        file_name=file_name
    )


def submit():
    global state
    command_dict = {
        "add": add,
        "delete": delete,
        "find": find,
        "modify": modify,
        "list": listall,
        "statistics": statistic
    }
    if not state:
        messagebox.showerror(title="SUBMIT",
                             message="Method Error:\nNo method was selected.")
        return
    output.delete("1.0", tkinter.END)
    output.insert(tkinter.END, state+"\n", "bold")
    out_text = command_dict[state]() + "\n"
    output.insert(tkinter.END, out_text)
    output.see(tkinter.END)


if __name__ == "__main__":
    state = ""

    # root
    root = tkinter.Tk()
    root.title("Financial Log Tool GUI v1.3")
    root.resizable(False, False)

    # frame
    command_frame = tkinter.Frame(root)
    command_frame.grid(row=0, column=0)
    arg_area = tkinter.Frame(root)
    arg_area.grid(row=1, column=0)
    arg_frame = tkinter.Frame(arg_area)  # set a frame for "destroy"
    arg_frame.pack()
    output_frame = tkinter.Frame(root)
    output_frame.grid(row=2, column=0)

    # button
    add_button = tkinter.Button(command_frame, text="ADD", command=show_add)
    add_button.grid(row=0, column=0)
    delete_button = tkinter.Button(command_frame, text="DELETE", command=show_delete)
    delete_button.grid(row=0, column=1)
    find_button = tkinter.Button(command_frame, text="FIND", command=show_find)
    find_button.grid(row=0, column=2)
    list_button = tkinter.Button(command_frame, text="LIST", command=show_list)
    list_button.grid(row=0, column=3)
    modify_button = tkinter.Button(command_frame, text="MODIFY", command=show_modify)
    modify_button.grid(row=0, column=4)
    statistics_button = tkinter.Button(command_frame, text="STATISTICS", command=show_statistics)
    statistics_button.grid(row=0, column=5)

    submit_button = tkinter.Button(command_frame, text="Submit", command=lambda: submit(), foreground="#ff0000")
    submit_button.grid(row=0, column=6)

    # output
    output = tkinter.Text(output_frame, width=80, height=20)
    output.grid(row=2, column=0)
    output.tag_configure("bold", font=("Consolas", 12, "bold"))

    # mainloop
    tkinter.mainloop(0)
