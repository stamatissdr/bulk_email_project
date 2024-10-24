import sqlite3
import smtplib
import ssl
from email.mime.text import MIMEText
import logging
import getpass
import time
import certifi
import os

# Set up logging to log errors to a file
logging.basicConfig(
    filename='email_errors.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# SMTP server configuration for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Sender's email address
SENDER_EMAIL = 'southwest.questionnaire@gmail.com'  # Replace with your email

# Email content templates
EMAIL_SUBJECT = 'Πρόσκληση συμμετοχής σε έρευνα διδακτορικής διατριβής'
EMAIL_BODY_TEMPLATE = '''ΔΙΑΧΕΙΡΙΣΗ ΑΝΘΡΩΠΙΝΟΥ ΔΥΝΑΜΙΚΟΥ ΣΤΟΝ ΙΔΙΩΤΙΚΟ ΚΑΙ ΔΗΜΟΣΙΟ ΤΟΜΕΑ ΣΤΗΝ ΕΛΛΑΔΑ

Η παρούσα έρευνα, λαμβάνει χώρα στα πλαίσια της έρευνας για τον διδακτορικό μου τίτλο, με σκοπό τη διερεύνηση της διαχείρισης του ανθρώπινου δυναμικού στον ιδιωτικό και δημόσιο τομέα της Ελλάδας. Στο ερευνητικό αυτό πλαίσιο σας ζητείται να απαντήσετε σε μια σειρά ερωτήσεων που αφορούν την διαχείριση του ανθρώπινου δυναμικού. Η συμμετοχή σας στη μελέτη είνι εθελοντική και ανώνυμη.

Παρακαλώ συμπληρώστε τη φόρμα στον ακόλουθο σύνδεσμο:
https://docs.google.com/forms/d/e/1FAIpQLScnOum3tAaYiHaPrYaE_lCUTYNPfp93R2JhXgTMy399QSAFww/viewform

Σας ευχαριστώ εκ των προτέρων για τη συμμετοχή σας.

Με εκτίμηση
'''

def connect_to_smtp(sender_password):
    """
    Connects to the SMTP server and returns the server object.
    """
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, sender_password)
        return server
    except Exception as e:
        logging.error(f"SMTP connection error: {e}")
        return None

def send_email(server, recipient_email):
    """
    Sends an email to a single recipient.
    """
    try:
        message = MIMEText(EMAIL_BODY_TEMPLATE)
        message['Subject'] = EMAIL_SUBJECT
        message['From'] = SENDER_EMAIL
        message['To'] = recipient_email

        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Error sending email to {recipient_email}: {e}")
        print(f"Failed to send email to {recipient_email}. Error logged.")

def main():
    sender_password = getpass.getpass("Enter your email password (or app password): ")

    # Connect to the SQLite database
    try:
        conn = sqlite3.connect('email_database.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        print("Failed to connect to the database. Check the error log for details.")
        return

    # Connect to the SMTP server
    server = connect_to_smtp(sender_password)
    if server is None:
        print("Failed to connect to the SMTP server. Exiting.")
        return

    try:
        cursor.execute('SELECT email FROM email_list')
        for i, (recipient_email,) in enumerate(cursor, 1):
            send_email(server, recipient_email)
            print(f"Email {i} sent to {recipient_email}")
            time.sleep(3)  # Delay between emails
            if i % 20 == 0:
                print("Παύση για 60 δευτερόλεπτα...")
                time.sleep(60)
            if i >= 200:
                print("Έχουν σταλεί 200 emails. Διακοπή της διαδικασίας.")
                break
    except Exception as e:
        logging.error(f"Error during email sending: {e}")
    finally:
        server.quit()  # Ensure the server is closed
        conn.close()

if __name__ == '__main__':
    main()
