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
            source="linkedin_guest"
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
