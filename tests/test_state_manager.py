"""Unit tests for StateManager."""

import tempfile
from pathlib import Path
from src.models.offer import JobOffer
from src.storage.state_manager import StateManager


def test_state_manager_record_and_idempotency():
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "test_applied.json"
        sm = StateManager(state_file=state_file)

        offer = JobOffer(
            title="Stage PFE Data & IA",
            company="Morocco AI Hub",
            url="https://example.com/pfe",
            source="linkedin_guest",
        )

        assert sm.is_already_seen(offer.id) is False
        assert sm.is_already_applied(offer.id) is False

        # Record offer as seen and applied
        sm.record_offer(offer, applied=True, notified=True)

        assert sm.is_already_seen(offer.id) is True
        assert sm.is_already_applied(offer.id) is True
        assert sm.data["total_applied"] == 1

        # Re-load in a new instance and verify persistence
        sm2 = StateManager(state_file=state_file)
        assert sm2.is_already_seen(offer.id) is True
        assert sm2.is_already_applied(offer.id) is True


def test_state_manager_dry_run_simulation_separation():
    """Verifies dry-run records do NOT mark offers as genuinely applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "test_applied.json"
        sm = StateManager(state_file=state_file)

        offer = JobOffer(
            title="Stage PFE Machine Learning",
            company="Tech Lab",
            url="https://example.com/ml",
            source="rekrute",
            contact_email="rh@techlab.ma",
        )

        # Simulation in dry run mode
        sm.record_offer(offer, applied=False, notified=True, simulated=True)

        assert sm.is_already_seen(offer.id) is True
        assert sm.is_already_notified(offer.id) is True
        assert sm.is_already_applied(offer.id) is False
        assert sm.data["total_applied"] == 0
        assert sm.data["total_simulated"] == 1

        # Now when live mode executes and actually applies
        sm.record_offer(offer, applied=True, notified=True, simulated=False)
        assert sm.is_already_applied(offer.id) is True
        assert sm.data["total_applied"] == 1


def test_state_manager_statistics():
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "test_applied.json"
        sm = StateManager(state_file=state_file)

        offer1 = JobOffer(title="Offer 1", company="A", url="https://a.com", source="rekrute", is_remunerated=True)
        offer2 = JobOffer(title="Offer 2", company="B", url="https://b.com", source="linkedin_guest", is_remunerated=False)

        sm.record_offer(offer1, applied=True, notified=True)
        sm.record_offer(offer2, applied=False, notified=True, simulated=True)

        stats = sm.get_statistics()
        assert stats["total_offers"] == 2
        assert stats["applied"] == 1
        assert stats["simulated"] == 1
        assert stats["notified"] == 2
        assert stats["remunerated"] == 1
        assert stats["sources"]["rekrute"] == 1
        assert stats["sources"]["linkedin_guest"] == 1
