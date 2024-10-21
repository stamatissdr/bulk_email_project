import sqlite3

# Δημιουργία σύνδεσης με τη βάση δεδομένων
conn = sqlite3.connect('email_database.db')
cursor = conn.cursor()

# Διαγραφή του πίνακα email_list αν υπάρχει
cursor.execute('DROP TABLE IF EXISTS email_list')

# Δημιουργία του πίνακα email_list
cursor.execute('''
CREATE TABLE email_list (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
)
''')

# Εδώ μπορείτε να προσθέσετε τις πραγματικές διευθύνσεις email
real_data = [
    ('mvrek@chemistry.uch.gr',),
    ('office@chiosonline.gr',),
    # Προσθέστε εδώ τις υπόλοιπες διευθύνσεις email
]

# Εισαγωγή των νέων δεδομένων
for email in real_data:
    try:
        cursor.execute('INSERT INTO email_list (email) VALUES (?)', email)
    except sqlite3.IntegrityError:
        print(f"Duplicate email found: {email[0]}. Skipping.")

# Αποθήκευση των αλλαγών και κλείσιμο της σύνδεσης
conn.commit()
conn.close()

print("Ο πίνακας email_list έχει καθαριστεί και ενημερωθεί με τις νέες διευθύνσεις email.")