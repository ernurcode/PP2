import psycopg2
from connect import connect


def call_upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def call_search():
    pattern = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    print(cur.fetchall())

    cur.close()
    conn.close()


def call_pagination():
    lim = int(input("Limit: "))
    off = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (lim, off))
    print(cur.fetchall())

    cur.close()
    conn.close()


def call_delete():
    value = input("Name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def call_bulk():
    names = input("Names: ").split()
    phones = input("Phones: ").split()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many(%s, %s)",
        (names, phones)
    )

    conn.commit()
    cur.close()
    conn.close()


def main():
    while True:
        print("\n1.Upsert 2.Search 3.Pagination 4.Delete 5.Bulk 0.Exit")
        c = input("> ")

        if c == "1":
            call_upsert()
        elif c == "2":
            call_search()
        elif c == "3":
            call_pagination()
        elif c == "4":
            call_delete()
        elif c == "5":
            call_bulk()
        elif c == "0":
            break


if __name__ == "__main__":
    main()