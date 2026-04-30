import json
import csv
from connect import get_connection


conn = get_connection()
cur = conn.cursor()


# ---------------- CREATE ----------------
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday: ")
    group = input("Group: ")

    # group id
    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()

    if g:
        group_id = g[0]
    else:
        cur.execute(
            "INSERT INTO groups(name) VALUES (%s) RETURNING id",
            (group,)
        )
        group_id = cur.fetchone()[0]

    # UPSERT CONTACT
    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name)
        DO UPDATE SET
            email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    conn.commit()
    print("Contact added/updated")

# ---------------- ADD PHONE  ----------------
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("SELECT id FROM contacts WHERE name ILIKE %s", (name,))
    c = cur.fetchone()

    if not c:
        print("Contact not found")
        return

    contact_id = c[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, ptype))

    conn.commit()
    print("Phone added")

# ---------------- SEARCH  ----------------
def search():
    q = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)


# ---------------- FILTER BY GROUP ----------------
def filter_group():
    g = input("Group: ")
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (g,))
    print(cur.fetchall())


# ---------------- SEARCH EMAIL ----------------
def search_email():
    e = input("Email part: ")
    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
    """, ('%' + e + '%',))
    print(cur.fetchall())


# ---------------- SORT ----------------
def sort_contacts():
    field = input("Sort by (name/birthday/date): ")

    allowed = {
        "name": "name",
        "birthday": "birthday",
        "date": "created_at"
    }

    order = allowed.get(field, "name")

    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {order}
    """)

    print(cur.fetchall())


# ---------------- PAGINATION ----------------
def pagination():
    page = 0
    limit = 3

    while True:
        cur.execute("""
            SELECT name, email
            FROM contacts
            ORDER BY created_at
            LIMIT %s OFFSET %s
        """, (limit, page * limit))

        rows = cur.fetchall()
        print(rows)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break

# ---------------- IMPORT CSV ----------------
def import_csv():
    filename = input("CSV file: ")

    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            ptype = row["type"]

            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            g = cur.fetchone()

            if g:
                group_id = g[0]
            else:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (group,)
                )
                group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, ptype))

    conn.commit()
    print("CSV imported")

# ---------------- EXPORT JSON ----------------
def export_json():
    cur.execute("SELECT * FROM contacts")
    contacts = cur.fetchall()

    data = []
    for c in contacts:
        data.append({
            "id": c[0],
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]),
            "group_id": str(c[4])
        })

    with open("C:/Users/Admin/Desktop/PP2/TSIS1/contacts.json", "w") as f:
        json.dump(data, f, indent=4)


# ---------------- IMPORT JSON ----------------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            action = input(f"{c['name']} exists (skip/overwrite): ")
            if action == "skip":
                continue
            cur.execute("DELETE FROM contacts WHERE name=%s", (c["name"],))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s,%s,%s,%s)
        """, (c["name"], c["email"], c["birthday"], c["group_id"]))

    conn.commit()


# ---------------- MENU ----------------
def menu():
    while True:
        print("""
1. Add contact
2. Search (DB function)
3. Filter by group
4. Search email
5. Sort
6. Pagination
7. Export JSON
8. Import JSON
9. Add phone
10. Import CSV
0. Exit
        """)

        choice = input("> ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search()
        elif choice == "3":
            filter_group()
        elif choice == "4":
            search_email()
        elif choice == "5":
            sort_contacts()
        elif choice == "6":
            pagination()
        elif choice == "7":
            export_json()
        elif choice == "8":
            import_json()
        elif choice == "0":
            break
        elif choice == "9":
            add_phone()
        elif choice == "10":
            import_csv()


menu()
cur.close()
conn.close()