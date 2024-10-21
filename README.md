

 Bulk Email Sender Project

This repository contains two main components for sending bulk emails: a Python script (`bulk_email_sender.py`) that is fully functional and ready to send emails, and a web app (`bulk_email_web_app`) which is in development and partially functional.

 Repository Overview

- bulk_email_sender.py: A Python script that automates the process of sending bulk emails using a Gmail SMTP server. The script pulls recipient data from a local SQLite database (`email_database.db`) and personalizes each email using a predefined template.
  
- bulk_email_web_app: An experimental web-based application that aims to provide a user-friendly interface for sending bulk emails. The app is currently functional but not fully finished.

- create_database.py: A helper script that creates the SQLite database (`email_database.db`) and inserts email records for testing purposes.

- email_database.db: A sample SQLite database that stores email addresses and recipient names.

- email_errors.log: A log file that records any errors encountered during the email sending process.

- requirements.txt: A list of required Python packages to run both the script and the web app.

How to Use

Prerequisites
- Python 3.9 or later installed.
- Required Python packages listed in `requirements.txt`:
  bash
  pip install -r requirements.txt
  

Running the Bulk Email Script (`bulk_email_sender.py`)

1. Set up an **app password** for Gmail or use another SMTP server.
2. Edit the email content in `bulk_email_sender.py` as needed.
3. Run the script to send emails:
   bash
   python3 bulk_email_sender.py
   

### Setting Up the Web App (`bulk_email_web_app`)

The web app is still under development but can be used in its current state. To set up the web app:

1. Install the required dependencies from `requirements.txt`.
2. Deploy the app locally or to a cloud platform (such as Heroku).
3. Access the web interface and follow the instructions to send emails (note that the interface is not yet finalized).

Logging and Debugging

- Any errors during the execution of the bulk email sender script will be logged in the `email_errors.log` file.
- You can also review the log to troubleshoot issues like invalid email addresses or SMTP server failures.

Future Development

- Complete the web app: The `bulk_email_web_app` is a work in progress. Upcoming features include a more intuitive interface, better error handling, and improved support for larger email lists.
- Improve email templates: Future updates will allow dynamic HTML email templates.
- Add more SMTP options: Currently, the app is configured to work with Gmail, but future updates will add more SMTP server options.

This project is licensed under the [MIT License](LICENSE).

