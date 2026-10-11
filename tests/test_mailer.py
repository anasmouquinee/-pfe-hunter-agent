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


def test_cover_letter_html_generation():
    offer = JobOffer(
        title="Stage PFE Data & Intelligence Artificielle",
        company="Capgemini Engineering",
        url="https://example.com/capgemini",
        source="linkedin_guest",
        matched_skills=["Python", "Apache Airflow", "Kafka"]
    )

    html_body = CoverLetterGenerator.generate_html_body(offer)
    assert "<!DOCTYPE html>" in html_body
    assert "Capgemini Engineering" in html_body
    assert "EMSI Casablanca" in html_body
    assert "COSUMAR" in html_body
    assert "SEWS-CABINET" in html_body
    assert "Enterprise Media Lakehouse" in html_body
    assert "anasmouqine@gmail.com" in html_body
