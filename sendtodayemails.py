import csv
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from email.mime.application import MIMEApplication
from zipfile import ZipFile

def send_email(sender_email, sender_password, to_email, subject, body, attachments):
    with smtplib.SMTP('your_smtp_server', your_smtp_port) as server:
        server.login(sender_email, sender_password)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        for attachment in attachments:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                message.attach(part)

        server.sendmail(sender_email, to_email, message.as_string())

def send_emails_from_csv(csv_file_path, attachments_folder):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            email_instance_id, from_email, to_email, subject, body = row

            attachments_folder_for_email = os.path.join(attachments_folder, f'{email_instance_id}')
            os.makedirs(attachments_folder_for_email, exist_ok=True)

            send_email(from_email, '', to_email, subject, body, [attachments_folder_for_email])

if __name__ == "__main__":
    csv_file_path = 'outbound_emails.csv'
    attachments_folder = 'attachments'

    os.makedirs(attachments_folder, exist_ok=True)

    send_emails_from_csv(csv_file_path, attachments_folder)
