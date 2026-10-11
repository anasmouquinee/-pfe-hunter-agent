"""Base scraper interface with robust HTTP fetching and entity extraction."""

import requests
from abc import ABC, abstractmethod
from typing import List
from src.models.offer import JobOffer
from src.utils.text_extractor import extract_emails as util_extract_emails, extract_linkedin_urls as util_extract_linkedin_urls
from src.utils.logger import logger


class BaseScraper(ABC):
    """Abstract base scraper with common utilities and standardized browser headers."""
    name: str = "base"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    @abstractmethod
    def scrape(self, keyword: str = "stage pfe", location: str = "Casablanca") -> List[JobOffer]:
        """Scrape offers matching the keyword and location."""
        pass

    def extract_emails(self, text: str) -> List[str]:
        """Extract valid email addresses from text (delegates to centralized utility)."""
        return util_extract_emails(text)

    def extract_linkedin_urls(self, text: str) -> List[str]:
        """Extract LinkedIn profile or post URLs from text (delegates to centralized utility)."""
        return util_extract_linkedin_urls(text)
