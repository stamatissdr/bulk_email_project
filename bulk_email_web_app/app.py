from flask import Flask, render_template, request, jsonify
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import certifi
import time
import logging
import os
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError

# Load environment variables from .env file
load_dotenv()

# Configure logging to write to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    logging.info("Received request to send emails.")

    # Check if the CSV file is present
    if 'csv_file' not in request.files:
        logging.error("CSV file is missing.")
        return jsonify({"success": False, "message": "Missing CSV file"}), 400

    csv_file = request.files['csv_file']

    # Get sender email from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    if not sender_email or '@' not in sender_email:
        logging.error("Sender email is not configured properly.")
        return jsonify({"success": False, "message": "Sender email is not configured properly."}), 500

    # Get email subject
    email_subject = request.form.get('email_subject')
    if not email_subject:
        logging.error("Email subject is required.")
        return jsonify({"success": False, "message": "Email subject is required"}), 400

    # Get email content
    email_content = request.form.get('email_content')
    if not email_content:
        logging.error("Email content is required.")
        return jsonify({"success": False, "message": "Email content is required"}), 400

    # Get app password from environment variables
    app_password = os.getenv('APP_PASSWORD')
    if not app_password:
        logging.error("App password is not configured.")
        return jsonify({"success": False, "message": "App password is not configured."}), 500

    # Read and validate emails from CSV
    try:
        csv_content = csv_file.read().decode('utf-8-sig').splitlines()
        csv_reader = csv.reader(csv_content)
        email_list = []
        for row in csv_reader:
            if row:
                email = row[0].strip()
                try:
                    valid = validate_email(email)
                    email_list.append(valid.email)
                except EmailNotValidError as e:
                    logging.warning(f"Invalid email {email}: {str(e)}")
        if not email_list:
            logging.error("No valid emails found in CSV.")
            return jsonify({"success": False, "message": "No valid emails found in CSV"}), 400
    except Exception as e:
        logging.error(f"Error reading CSV: {str(e)}")
        return jsonify({"success": False, "message": f"Error reading CSV: {str(e)}"}), 400

    # Send emails
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        sent_emails = []
        failed_emails = []
        sent_count = 0

        batch_size = 50  # Batch size
        delay_between_batches = 60  # Delay between batches in seconds

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, app_password)
            logging.info(f"Logged in as {sender_email}")

            for i in range(0, len(email_list), batch_size):
                batch = email_list[i:i+batch_size]
                for recipient in batch:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = recipient
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_content, 'plain'))

                        server.send_message(msg)
                        sent_emails.append(recipient)
                        sent_count += 1
                        logging.info(f"Email sent to {recipient}")
                    except Exception as e:
                        failed_emails.append({'email': recipient, 'error': str(e)})
                        logging.error(f"Failed to send email to {recipient}: {str(e)}")
                if i + batch_size < len(email_list):
                    logging.info(f"Waiting {delay_between_batches} seconds before sending next batch.")
                    time.sleep(delay_between_batches)

        message = f"Successfully sent {len(sent_emails)} emails."
        if failed_emails:
            message += f" Failed to send {len(failed_emails)} emails."
        logging.info(message)
        return jsonify({"success": True, "message": message, "failed_emails": failed_emails})
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication error. Check your email and app password.")
        return jsonify({"success": False, "message": "Authentication error. Check your email and app password."}), 400
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {str(e)}")
        return jsonify({"success": False, "message": f"SMTP error: {str(e)}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
