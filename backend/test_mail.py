from app import app
from mail import mail
from flask_mail import Message

with app.app_context():

    msg = Message(
        subject="Placement Portal Test",
        recipients=["student@test.com"],
        body="MailHog is working successfully."
    )

    mail.send(msg)

    print("Email sent successfully!")