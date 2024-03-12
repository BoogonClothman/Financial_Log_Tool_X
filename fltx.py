"""
Name | Financial Log Tool X --fltx
Version | 1.2
Author | Boogon Clothman
"""

import json
import argparse
import os
import datetime
from pprint import pprint
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
    amount = Decimal(amount).quantize(Decimal("0.01"))

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
    print(f"Added transaction with ID {transaction_id}.")


def delete_transaction(file_name, transaction_id):
    bills = load_bills(file_name)
    bills = [bill for bill in bills if bill['id'] != int(transaction_id)]
    for bill in bills:
        if bill['id'] > int(transaction_id):
            bill['id'] -= 1
    save_bills(file_name, bills)
    print(f"Deleted transaction with ID {transaction_id}.")


def find_transactions(file_name, keyword):
    bills = load_bills(file_name)
    keyword = keyword.lower()
    found_bills = [bill for bill in bills if keyword in bill['reason'].lower() or
                   keyword in (bill['counterparty'] or '').lower() or
                   str(bill['amount']).lower() == keyword or
                   str(bill['id']).lower() == keyword or
                   keyword in (bill['note'] or '').lower() or
                   keyword in bill["path"].lower()]
    if found_bills:
        print("Found transactions:")
        for bill in found_bills:
            pprint(bill)
    else:
        print(f"No transactions found for keyword '{keyword}'.")


def modify_transaction(file_name, transaction_id, field, new):
    bills = load_bills(file_name)
    for bill in bills:
        if bill['id'] == int(transaction_id):
            if field == 'amount':
                new = str(Decimal(new).quantize(Decimal("0.01")))
            else:
                new = str(new)
            bill[field] = new
            print(f"Modified transaction with ID {transaction_id}. New {field}: {new}")
            save_bills(file_name, bills)
            return
    print(f"Transaction with ID {transaction_id} not found.")


def list_transactions(file_name):
    bills = load_bills(file_name)
    if bills:
        print("Transactions:")
        for bill in bills:
            pprint(bill)
    else:
        print("No transactions.")


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

    for wallet_id, wallet_data in wallet_sta.items():
        print(f"Wallet:{wallet_id}")
        print(f"    Total Income: {wallet_data['income']}")
        print(f"    Total Expense: {wallet_data['expense']}\n")

    print("Overall")
    print(f"    Total Income: {total_income}")
    print(f"    Total Expense: {total_expense}")
    print(f"    Net Income: {net}")


if __name__ == "__main__":
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    DEFAULT_BILL_FILE = f"sheet-{year}-{month}.json"

    parser = argparse.ArgumentParser(description="Financial Log Management Tool.")
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser('add', help='Add a new transaction.')
    add_parser.add_argument('path', help='Transaction path.')
    add_parser.add_argument('reason', help='Transaction reason.')
    add_parser.add_argument('amount', help='Transaction amount.')
    add_parser.add_argument('-d', '--date', help='Transaction date (YYYY-MM-DD-HH:MM:SS).',
                            default=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    add_parser.add_argument('-cp', '--counterparty', help='Transaction counterparty.')
    add_parser.add_argument('-n', '--note', help='Transaction note.')
    add_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    add_parser.set_defaults(
        func=lambda args: add_transaction(args.file, args.reason, args.amount, args.date, args.path, args.counterparty,
                                          args.note))

    delete_parser = subparsers.add_parser('delete', help='Delete a transaction.')
    delete_parser.add_argument('transaction_id', type=int, help='ID of the transaction to delete.')
    delete_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    delete_parser.set_defaults(func=lambda args: delete_transaction(args.file, args.transaction_id))

    find_parser = subparsers.add_parser('find', help='Find transactions by keyword.')
    find_parser.add_argument('keyword', help='Keyword to search for.')
    find_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    find_parser.set_defaults(func=lambda args: find_transactions(args.file, args.keyword))

    modify_parser = subparsers.add_parser('modify', help='Modify a transaction.')
    modify_parser.add_argument('transaction_id', type=int, help='ID of the transaction to modify.')
    modify_parser.add_argument('-fd', '--field', choices=['path', 'reason', 'amount', 'date', 'counterparty', 'note'],
                               required=True, help='Field to modify.')
    modify_parser.add_argument('-n', '--new', required=True, help='New value for the field.', default=None)
    modify_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    modify_parser.set_defaults(
        func=lambda args: modify_transaction(args.file, args.transaction_id, args.field, args.new))

    list_parser = subparsers.add_parser('list', help='List all transactions.')
    list_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    list_parser.set_defaults(func=lambda args: list_transactions(args.file))

    statistics_parser = subparsers.add_parser('statistics', help='Show financial statistics.')
    statistics_parser.add_argument('-f', '--file', help='Path to the sheet file(.json).', default=DEFAULT_BILL_FILE)
    statistics_parser.set_defaults(func=lambda args: statistics(args.file))

    args = parser.parse_args()
    args.func(args)
