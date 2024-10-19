from flask import Flask, render_template, request, jsonify
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import certifi
import time
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Έλεγχος αν το αρχείο CSV υπάρχει
    if 'csv_file' not in request.files:
        return jsonify({"success": False, "message": "Missing CSV file"}), 400

    csv_file = request.files['csv_file']
    
    # Έλεγχος αν το email του αποστολέα είναι έγκυρο
    sender_email = request.form.get('sender_email')
    if not sender_email or '@' not in sender_email:
        return jsonify({"success": False, "message": "Invalid sender email format"}), 400

    # Έλεγχος αν το θέμα του email είναι παρόν
    email_subject = request.form.get('email_subject')
    if not email_subject:
        return jsonify({"success": False, "message": "Email subject is required"}), 400

    # Έλεγχος αν το περιεχόμενο του email είναι παρόν
    email_content = request.form.get('email_content')
    if not email_content:
        return jsonify({"success": False, "message": "Email content is required"}), 400

    # Έλεγχος αν ο κωδικός εφαρμογής είναι παρών
    app_password = request.form.get('app_password')
    if not app_password:
        return jsonify({"success": False, "message": "App password is required"}), 400

    # Έλεγχος αν το CSV είναι έγκυρο
    try:
        csv_content = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_content)
        email_list = [row[0] for row in csv_reader if row and '@' in row[0]]
        if not email_list:
            return jsonify({"success": False, "message": "No valid emails found in CSV"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Error reading CSV: {str(e)}"}), 400

    # Αν όλα τα δεδομένα είναι έγκυρα, προχωρήστε στην αποστολή emails
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        sent_count = 0
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, app_password)
            for recipient in email_list:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = email_subject
                msg.attach(MIMEText(email_content, 'plain'))
                
                server.send_message(msg)
                sent_count += 1

        return jsonify({"success": True, "message": f"Successfully sent {sent_count} emails"})
    except smtplib.SMTPAuthenticationError:
        return jsonify({"success": False, "message": "Authentication error. Check your email and password."}), 400
    except smtplib.SMTPException as e:
        return jsonify({"success": False, "message": f"SMTP error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
