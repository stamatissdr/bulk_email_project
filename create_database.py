import sqlite3

# Δημιουργία σύνδεσης με τη βάση δεδομένων
conn = sqlite3.connect('email_database.db')
cursor = conn.cursor()

# Δημιουργία του πίνακα email_list
cursor.execute('''
CREATE TABLE IF NOT EXISTS email_list (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
)
''')

# Νέα λίστα με πλασματικά email
fake_data = [
    ('user1@example.com',),
    ('user2@example.com',),
    ('user3@example.com',),
    ('user4@example.com',),
    ('user5@example.com',),
    ('user6@example.com',),
    ('user7@example.com',),
    ('user8@example.com',),
    ('user9@example.com',),
    ('user10@example.com',),
    ('test1@test.com',),
    ('test2@test.com',),
    ('test3@test.com',),
    ('test4@test.com',),
    ('test5@test.com',),
]

# Εισαγωγή των νέων δεδομένων
for email in fake_data:
    try:
        cursor.execute('INSERT INTO email_list (email) VALUES (?)', email)
    except sqlite3.IntegrityError:
        print(f"Duplicate email found: {email[0]}. Skipping.")

# Αποθήκευση των αλλαγών και κλείσιμο της σύνδεσης
conn.commit()
conn.close()

print("Η βάση δεδομένων ενημερώθηκε με τις πλασματικές διευθύνσεις email.")
