"""SMTP Email dispatcher with PDF CV attachment and dry-run safety."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Optional
from src.config import config
from src.models.offer import JobOffer
from src.mailer.cover_letter_generator import CoverLetterGenerator


class EmailSender:
    """Dispatches application emails with attached CV."""

    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 465
        self.sender_email = config.gmail_user
        self.app_password = config.gmail_app_password
        self.dry_run = config.dry_run
        self.cv_path = config.candidate.cv_path

    def send_application(self, offer: JobOffer, to_email: Optional[str] = None) -> bool:
        """Sends application email for the given offer to recruiter."""
        recipient = to_email or offer.contact_email
        if not recipient:
            return False

        subject = CoverLetterGenerator.generate_subject(offer)
        body = CoverLetterGenerator.generate_body(offer)

        if self.dry_run:
            print(f"[DRY-RUN] Simulating email send to: {recipient}")
            print(f"[DRY-RUN] Subject: {subject}")
            print(f"[DRY-RUN] Attachment: {self.cv_path.name} (exists={self.cv_path.exists()})")
            return True

        if not self.app_password:
            print(f"[ERROR] Cannot send email to {recipient}: GMAIL_APP_PASSWORD is not set!")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = f"{config.candidate.full_name} <{self.sender_email}>"
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # Attach CV PDF if it exists
            if self.cv_path.exists():
                with open(self.cv_path, "rb") as f:
                    part = MIMEApplication(f.read(), _subtype="pdf")
                    part.add_header("Content-Disposition", "attachment", filename=self.cv_path.name)
                    msg.attach(part)
            else:
                print(f"[WARNING] CV file {self.cv_path} not found for attachment!")

            # Secure SSL SMTP dispatch
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=20) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            print(f"[SUCCESS] Application email successfully sent to {recipient}!")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send email to {recipient}: {e}")
            return False
