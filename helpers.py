import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

def send_email(to_email, report_content, smtp_server, smtp_port, smtp_user, smtp_password):


    print("Verzenden van e-mail naar: ", to_email)

    smtp_server = smtp_server
    smtp_port = smtp_port
    smtp_user = smtp_user
    smtp_password = smtp_password

    print("SMTP Server: ", smtp_server)
    print("SMTP Port: ", smtp_port)
    print("SMTP User: ", smtp_user)
    print("SMTP Password: ", smtp_password)

    # Stel de e-mail samen
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['To'] = to_email + ', ' + "info@happy2change.be"
    msg['Subject'] = 'Uw AI Maturiteit Beoordelingsrapport'
    msg.attach(MIMEText(report_content, 'plain'))

    recipients = [to_email, "info@happy2change.be"]

    # Probeer de e-mail te verzenden
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipients, msg.as_string())
        server.quit()
        st.success('Rapport succesvol verzonden per e-mail! Indien je het niet ontvangt controleer dan je spam folder.')
    except Exception as e:
        st.error(f'Er is een fout opgetreden bij het verzenden van de e-mail: {e}')
