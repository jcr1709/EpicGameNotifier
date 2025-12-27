import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# MUST load dotenv here so the Worker sees the secrets!
load_dotenv()

def send_email_task(game_title, recipient_email):
    msg = EmailMessage()
    msg.set_content(f"Go claim {game_title} for free on Epic Games!")
    msg['Subject'] = f"🎮 Free Game Alert: {game_title}"
    msg['From'] = os.getenv("MY_EMAIL_ID")
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("MY_EMAIL_ID"), os.getenv("MY_EMAIL_PASSWORD"))
            smtp.send_message(msg)
            print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send to {recipient_email}: {e}")