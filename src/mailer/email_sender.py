"""SMTP Email dispatcher with multipart HTML/plain text, PDF CV attachment, and dry-run safety."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional
from src.config import config
from src.models.offer import JobOffer
from src.mailer.cover_letter_generator import CoverLetterGenerator
from src.utils.logger import logger


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
        """
        Sends application email for the given offer to recruiter.
        Supports both plain text and HTML rendering with professional PDF CV attachment.
        """
        recipient = to_email or offer.contact_email
        if not recipient:
            logger.warning("No recipient email found for offer '%s'", offer.title)
            return False

        subject = CoverLetterGenerator.generate_subject(offer)
        plain_body = CoverLetterGenerator.generate_body(offer)
        html_body = CoverLetterGenerator.generate_html_body(offer)

        # Simulation Mode
        if self.dry_run:
            logger.info(
                "[DRY-RUN] Simulating email send to: %s | Subject: '%s' | CV: %s (exists=%s)",
                recipient, subject, self.cv_path.name, self.cv_path.exists()
            )
            return True

        if not self.app_password:
            logger.error("Cannot send email to %s: GMAIL_APP_PASSWORD is not set!", recipient)
            return False

        try:
            # Root message container (multipart/mixed to allow attachments)
            msg = MIMEMultipart("mixed")
            msg["From"] = f"{config.candidate.full_name} <{self.sender_email}>"
            msg["To"] = recipient
            msg["Subject"] = subject

            # Alternative container for plain text and HTML
            alt_container = MIMEMultipart("alternative")
            alt_container.attach(MIMEText(plain_body, "plain", "utf-8"))
            alt_container.attach(MIMEText(html_body, "html", "utf-8"))
            msg.attach(alt_container)

            # Attach CV PDF if it exists
            if self.cv_path.exists():
                with open(self.cv_path, "rb") as f:
                    part = MIMEApplication(f.read(), _subtype="pdf")
                    # Clean filename format e.g. CV_Anas_Mouqine_PFE.pdf
                    cand_slug = config.candidate.full_name.replace(" ", "_")
                    part.add_header("Content-Disposition", "attachment", filename=f"CV_{cand_slug}_PFE.pdf")
                    msg.attach(part)
            else:
                logger.warning("CV file %s not found for attachment!", self.cv_path)

            # Secure SSL SMTP dispatch
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=20) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            logger.info("Application email successfully sent to %s for '%s'!", recipient, offer.title)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", recipient, e)
            return False
