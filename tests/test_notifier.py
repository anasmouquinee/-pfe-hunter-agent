"""Unit tests for Telegram and Discord notifiers."""

from unittest.mock import patch, MagicMock
from src.models.offer import JobOffer
from src.notifier.telegram_notifier import TelegramNotifier
from src.notifier.discord_notifier import DiscordNotifier


def test_telegram_formatting():
    offer = JobOffer(
        title="Stage PFE Data & RAG",
        company="AI Casablanca Lab",
        url="https://example.com/pfe",
        source="linkedin_guest",
        linkedin_url="https://linkedin.com/posts/hr-post-123",
        contact_email="rh@ailab.ma",
        is_remunerated=True,
        score=94,
        matched_skills=["Python", "RAG"]
    )

    notifier = TelegramNotifier(bot_token="fake_token", chat_id="12345")
    msg = notifier.format_message(offer, email_sent=True)

    assert "AI Casablanca Lab" in msg
    assert ("Stage PFE Data &amp; RAG" in msg or "Stage PFE Data" in msg)
    assert "<b>Poste :</b>" in msg
    assert "94%" in msg
    assert "🟢 Rémunéré" in msg
    assert "rh@ailab.ma" in msg
    assert "https://linkedin.com/posts/hr-post-123" in msg


@patch("requests.post")
def test_discord_notifier_mock_send(mock_post):
    mock_post.return_value = MagicMock(status_code=204)

    offer = JobOffer(
        title="Stage PFE AI Engineer",
        company="Fintech Maroc",
        url="https://example.com/pfe2",
        source="rekrute",
        linkedin_url="https://linkedin.com/in/hr-profile",
        contact_email="jobs@fintech.ma",
        is_remunerated=True,
        score=90
    )

    notifier = DiscordNotifier(webhook_url="https://discord.com/api/webhooks/mock")
    success = notifier.send_alert(offer, email_sent=True)

    assert success is True
    assert mock_post.called
