import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
DASHBOARD_URL = os.getenv("DASHBOARD_URL")


def send_sales_reminder(name, email):

    week_no = datetime.now().isocalendar()[1]

    body = f"""
Hi {name},

Please update your weekly sales projections.

Dashboard:
{DASHBOARD_URL}

Kindly complete it before EOD Monday.

Regards,
Sales Team
"""

    msg = MIMEText(body)

msg["Subject"] = f"Week {week_no} Sales Projection Reminder"
msg["From"] = SMTP_EMAIL
msg["To"] = email

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
