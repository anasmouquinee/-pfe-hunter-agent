"""Unit tests for CoverLetterGenerator and EmailSender."""

from src.models.offer import JobOffer
from src.mailer.cover_letter_generator import CoverLetterGenerator
from src.mailer.email_sender import EmailSender


def test_cover_letter_generator():
    offer = JobOffer(
        title="Stage PFE Data & IA",
        company="Orange Maroc",
        url="https://example.com/orange-pfe",
        source="rekrute",
        contact_email="recrutement@orange.com",
        matched_skills=["Python", "Apache Airflow"]
    )

    subject = CoverLetterGenerator.generate_subject(offer)
    body = CoverLetterGenerator.generate_body(offer)

    assert "Anas Mouqine" in subject
    assert "Orange Maroc" in body
    assert "EMSI Casablanca" in body
    assert "COSUMAR" in body
    assert "SEWS-CABINET" in body
    assert "cv_ats_pfe" not in body  # It should mention CV cleanly, not raw filename
    assert "Curriculum Vitae" in body


def test_email_sender_dry_run():
    offer = JobOffer(
        title="Stage PFE Data Engineering",
        company="Inwi",
        url="https://example.com/inwi",
        source="rekrute",
        contact_email="rh@inwi.ma"
    )

    sender = EmailSender()
    sender.dry_run = True  # Ensure dry-run
    success = sender.send_application(offer)

    assert success is True
