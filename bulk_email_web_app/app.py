from flask import Flask, render_template, request, jsonify
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import certifi
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    csv_file = request.files['csv_file']
    sender_email = request.form['sender_email']
    email_subject = request.form['email_subject']
    email_content = request.form['email_content']
    app_password = request.form['app_password']

    # Διάβασμα CSV
    email_list = []
    csv_content = csv_file.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(csv_content)
    for row in csv_reader:
        if row and '@' in row[0]:  # Βασικός έλεγχος εγκυρότητας email
            email_list.append(row[0])

    # Αποστολή emails
    context = ssl.create_default_context(cafile=certifi.where())
    sent_count = 0
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, app_password)
            for i, recipient in enumerate(email_list, 1):
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = email_subject
                msg.attach(MIMEText(email_content, 'plain'))
                
                server.send_message(msg)
                sent_count += 1
                
                if i % 50 == 0:
                    time.sleep(60)
                if i >= 200:
                    break
        return jsonify({"success": True, "message": f"Επιτυχής αποστολή {sent_count} emails"})
    except smtplib.SMTPAuthenticationError:
        return jsonify({"success": False, "message": "Σφάλμα αυθεντικοποίησης. Ελέγξτε το email και τον κωδικό σας."})
    except smtplib.SMTPException as e:
        return jsonify({"success": False, "message": f"Σφάλμα SMTP: {str(e)}"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Απρόσμενο σφάλμα: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
