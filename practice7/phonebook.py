import csv
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(file):
    conn = connect()
    cur = conn.cursor()

    with open(file, newline='') as f:
        reader = csv.reader(f)
        for name, phone in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def update_contact(old_name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, old_name)
        )
    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, old_name)
        )

    conn.commit()
    cur.close()
    conn.close()


def query_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def query_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE name=%s", (name,))
    print(cur.fetchall())

    cur.close()
    conn.close()


def query_by_phone_prefix(prefix):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )
    print(cur.fetchall())

    cur.close()
    conn.close()


def delete_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))

    conn.commit()
    cur.close()
    conn.close()


def delete_by_phone(phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))

    conn.commit()
    cur.close()
    conn.close()



def main():
    create_table()

    while True:
        print("\n1.Add(console) 2.Add(CSV) 3.Update 4.Query 5.Delete 0.Exit")
        c = input("> ")

        if c == "1":
            insert_from_console()
        elif c == "2":
            insert_from_csv(r"C:\Users\Admin\Desktop\PP2\practice7\contacts.csv")
        elif c == "3":
            name = input("Old name: ")
            new_name = input("New name (or enter): ")
            new_phone = input("New phone (or enter): ")
            update_contact(name, new_name or None, new_phone or None)
        elif c == "4":
            print("1.All 2.By name 3.By prefix")
            q = input("> ")
            if q == "1":
                query_all()
            elif q == "2":
                query_by_name(input("Name: "))
            elif q == "3":
                query_by_phone_prefix(input("Prefix: "))
        elif c == "5":
            print("1.By name 2.By phone")
            d = input("> ")
            if d == "1":
                delete_by_name(input("Name: "))
            elif d == "2":
                delete_by_phone(input("Phone: "))
        elif c == "0":
            break


if __name__ == "__main__":
    main()