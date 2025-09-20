import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import re

load_dotenv()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "email_templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def generate_otp():
    return str(random.randint(100000, 999999))

def render_template_with_subject(template_name: str, context: dict):
    template = env.get_template(template_name)
    rendered = template.render(context)

    match = re.search(r'<!--\s*Subject:\s*(.*?)\s*-->', rendered)
    if match:
        subject = match.group(1)
        body = re.sub(r'<!--\s*Subject:.*?-->', '', rendered, count=1).strip()
    else:
        subject = "No Subject"
        body = rendered
    return subject, body


def send_mail(receiver_email, subject, message, html=False):
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("EMAIL_PORT", 587))

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        body = MIMEText(message, 'html' if html else 'plain')
        msg.attach(body)

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")