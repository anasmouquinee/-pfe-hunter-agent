"""State persistence and deduplication manager."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from src.config import config
from src.models.offer import JobOffer


class StateManager:
    """Manages applied offers to prevent duplicate submissions and alerts."""

    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or config.state_file
        self.data: Dict[str, Any] = {"offers": {}, "last_updated": "", "total_applied": 0}
        self.load_state()

    def load_state(self) -> None:
        """Loads state from JSON file or initializes an empty structure."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"offers": {}, "last_updated": "", "total_applied": 0}
        else:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.data = {"offers": {}, "last_updated": "", "total_applied": 0}

    def is_already_seen(self, offer_id: str) -> bool:
        """Returns True if the offer was already scraped or handled."""
        return offer_id in self.data.get("offers", {})

    def is_already_applied(self, offer_id: str) -> bool:
        """Returns True if CV was already sent to this offer."""
        offer_data = self.data.get("offers", {}).get(offer_id)
        return bool(offer_data and offer_data.get("applied"))

    def record_offer(self, offer: JobOffer, applied: bool = False, notified: bool = False) -> None:
        """Records an offer or updates its applied/notified status."""
        now_iso = datetime.now(timezone.utc).isoformat()
        existing = self.data["offers"].get(offer.id, {})

        self.data["offers"][offer.id] = {
            "title": offer.title,
            "company": offer.company,
            "url": offer.url,
            "source": offer.source,
            "contact_email": offer.contact_email,
            "linkedin_url": offer.linkedin_url,
            "hr_name": offer.hr_name,
            "hr_linkedin_url": offer.hr_linkedin_url,
            "is_remunerated": offer.is_remunerated,
            "score": offer.score,
            "matched_skills": offer.matched_skills,
            "first_seen": existing.get("first_seen", now_iso),
            "applied": applied or existing.get("applied", False),
            "applied_at": now_iso if applied else existing.get("applied_at"),
            "notified": notified or existing.get("notified", False),
            "notified_at": now_iso if notified else existing.get("notified_at")
        }

        # Update totals
        self.data["total_applied"] = sum(1 for o in self.data["offers"].values() if o.get("applied"))
        self.data["last_updated"] = now_iso
        self.save_state()

    def save_state(self) -> None:
        """Saves current state to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
