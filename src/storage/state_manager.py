"""State persistence and deduplication manager."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from src.config import config
from src.models.offer import JobOffer
from src.utils.logger import logger


class StateManager:
    """Manages applied offers to prevent duplicate submissions and alerts."""

    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or config.state_file
        self.data: Dict[str, Any] = {
            "offers": {},
            "last_updated": "",
            "total_applied": 0,
            "total_simulated": 0,
        }
        self.load_state()

    def load_state(self) -> None:
        """Loads state from JSON file or initializes an empty structure."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.error("Failed to parse state file %s: %s", self.state_file, e)
                self.data = {
                    "offers": {},
                    "last_updated": "",
                    "total_applied": 0,
                    "total_simulated": 0,
                }
        else:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.data = {
                "offers": {},
                "last_updated": "",
                "total_applied": 0,
                "total_simulated": 0,
            }

    def is_already_seen(self, offer_id: str) -> bool:
        """Returns True if the offer was already scraped or handled."""
        return offer_id in self.data.get("offers", {})

    def is_already_applied(self, offer_id: str) -> bool:
        """Returns True if CV was genuinely sent via email to this offer."""
        offer_data = self.data.get("offers", {}).get(offer_id)
        return bool(offer_data and offer_data.get("applied"))

    def is_already_notified(self, offer_id: str) -> bool:
        """Returns True if Telegram or Discord alert has already been dispatched."""
        offer_data = self.data.get("offers", {}).get(offer_id)
        return bool(offer_data and offer_data.get("notified"))

    def record_offer(
        self,
        offer: JobOffer,
        applied: bool = False,
        notified: bool = False,
        simulated: bool = False,
    ) -> None:
        """
        Records an offer or updates its applied/notified/simulated status.
        Crucially separates real applications ('applied') from dry-run simulations ('simulated').
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        existing = self.data["offers"].get(offer.id, {})

        # An offer remains 'applied' once applied in live mode
        is_applied = applied or existing.get("applied", False)
        is_notified = notified or existing.get("notified", False)
        is_simulated = simulated or existing.get("simulated", False)

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
            "applied": is_applied,
            "applied_at": now_iso if applied else existing.get("applied_at"),
            "simulated": is_simulated,
            "simulated_at": now_iso if simulated else existing.get("simulated_at"),
            "notified": is_notified,
            "notified_at": now_iso if notified else existing.get("notified_at"),
        }

        # Update totals
        self.data["total_applied"] = sum(
            1 for o in self.data["offers"].values() if o.get("applied")
        )
        self.data["total_simulated"] = sum(
            1 for o in self.data["offers"].values() if o.get("simulated")
        )
        self.data["last_updated"] = now_iso
        self.save_state()

    def get_statistics(self) -> Dict[str, Any]:
        """Returns high-level statistics for reporting and CLI display."""
        offers = self.data.get("offers", {})
        total_offers = len(offers)
        applied_count = sum(1 for o in offers.values() if o.get("applied"))
        simulated_count = sum(1 for o in offers.values() if o.get("simulated"))
        notified_count = sum(1 for o in offers.values() if o.get("notified"))
        remunerated_count = sum(1 for o in offers.values() if o.get("is_remunerated"))

        sources_breakdown: Dict[str, int] = {}
        for o in offers.values():
            src = o.get("source", "unknown")
            sources_breakdown[src] = sources_breakdown.get(src, 0) + 1

        return {
            "total_offers": total_offers,
            "applied": applied_count,
            "simulated": simulated_count,
            "notified": notified_count,
            "remunerated": remunerated_count,
            "sources": sources_breakdown,
            "last_updated": self.data.get("last_updated", ""),
        }

    def save_state(self) -> None:
        """Saves current state to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
