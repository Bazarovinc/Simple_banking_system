import random
from collections import namedtuple
import sqlite3


def generate_n_nums(n):
    number = []
    for i in range(n):
        number.append(random.randint(0, 9))
    return number


def luhn(card_n):
    len_of_card_n = len(card_n)
    copy_card_n = card_n.copy()
    for i in range(2):
        for j in range(len_of_card_n):
            if i == 0 and (j + 1) % 2 != 0:
                copy_card_n[j] *= 2
            elif i == 1:
                if copy_card_n[j] > 9:
                    copy_card_n[j] -= 9
    sum_of_n = sum(copy_card_n)
    last_n = 10 - (sum_of_n % 10)
    card_n.append(last_n)
    str_card_n = ''
    for n in card_n:
        str_card_n += str(n)
    return str_card_n


def create_account(cur, table, conn):
    while True:
        id = len(table)
        card_n = generate_n_nums(9)
        card_n = [4, 0, 0, 0, 0, 0] + card_n
        card_n = luhn(card_n)
        count = 0
        for cards in table:
            if card_n != cards[1]:
                count += 1
        if count == id:
            pin = generate_n_nums(4)
            pin_s = ''
            for n in pin:
                pin_s += str(n)
            table.append((id + 1, card_n, pin_s, 0))
            break
    print(f"\nYour card has been created\nYour card number:\n{table[id][1]}\nYour card PIN:\n{table[id][2]}")
    cur.execute(f"INSERT INTO card VALUES ({table[id][0]}, {table[id][1]}, {table[id][2]}, 0)")
    conn.commit()


def transfer(card, cur, conn):
    for_card = input("Enter card number:")
    card_n = []
    for i in for_card:
        card_n.append(int(i))
    card_n.pop(-1)
    if for_card == luhn(card_n):
        cur.execute(f"SELECT * FROM card WHERE number = {for_card}")
        card_info = cur.fetchall()
        if len(card_info) == 0:
            print("Such a card does not exist.")
        else:
            card_info = card_info[0]
            transf = int(input('Enter how much money you want to transfer:'))
            balance_1 = card[3]
            balance_2 = card_info[3]
            if balance_1 - transf < 0:
                print("Not enough money!")
            else:
                balance_1 -= transf
                balance_2 += transf
                cur.execute(f"UPDATE card SET balance = {balance_1} WHERE number = {card[1]};")
                cur.execute(f"UPDATE card SET balance = {balance_2} WHERE number = {card_info[1]};")
                conn.commit()
                print("Success!")
    else:
        print('Probably you made mistake in card number. Please try again!')


def card_menu(card, cur, conn):
    to_return = 1
    while True:
        cur.execute(f"SELECT * FROM card WHERE number = {card[1]}")
        card = cur.fetchall()[0]
        print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        n = input()
        if n == "1":
            print(f"\nBalance: {card[3]}")
        elif n == "5":
            to_return = 5
            print("\nYou have successfully logged out!")
            break
        elif n == "2":
            to_return = 2
            balance = card[3]
            income = int(input("\nEnter income:"))
            balance += income
            cur.execute(f"UPDATE card SET balance = {balance} WHERE number = {card[1]};")
            conn.commit()
            print("Income was added!")
        elif n == '4':
            to_return = 4
            cur.execute(f"DELETE FROM card WHERE number = {card[1]}")
            print("\nThe account has been closed!")
            break
        elif n == '3':
            to_return = 3
            print("\nTransfer")
            transfer(card, cur, conn)
        elif n == "0":
            to_return = 0
            break
    return to_return


def log_into(cur, conn):
    to_return = 1
    card_n = input("\nEnter your card number:\n")
    cur.execute(f"SELECT * FROM card WHERE number = {card_n}")
    card = cur.fetchall()
    pin = input("Enter your PIN:\n")
    if len(card) != 0:
        if card[0][2] == pin:
            print("\nYou have successfully logged in!")
            to_return = card_menu(card[0], cur, conn)
        else:
            print("\nWrong card number or PIN!")
            to_return = 1
    else:
        print("\nWrong card number or PIN!")
        to_return = 1
    return to_return


def menu(conn, cur):
    try:
        cur.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
        conn.commit()
        table = []
    except sqlite3.OperationalError:
        cur.execute("SELECT * FROM card")
        conn.commit()
        table = cur.fetchall()
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    n_input = input()
    while n_input != '0':
        if n_input == '1':
            create_account(cur, table, conn)
        elif n_input == '2':
            if log_into(cur, conn) == 0:
                n_input = 0
                break
            conn.commit()
        print("\n1. Create an account\n2. Log into account\n0. Exit")
        n_input = input()
    if n_input == '0':
        print("\nBye!")


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
menu(conn, cur)
