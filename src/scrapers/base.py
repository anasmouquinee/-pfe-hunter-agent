"""Base scraper interface with robust HTTP fetching and entity extraction."""

import re
import requests
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.offer import JobOffer


class BaseScraper(ABC):
    """Abstract base scraper with common utilities."""
    name: str = "base"
    
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        """Extract valid email addresses from text."""
        if not text:
            return []
        pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        matches = re.findall(pattern, text)
        clean = []
        for email in matches:
            email_clean = email.rstrip('.,;!?:()[]"\'').lower()
            if not email_clean.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                if email_clean not in clean:
                    clean.append(email_clean)
        return clean

    def extract_linkedin_urls(self, text: str) -> List[str]:
        """Extract LinkedIn profile or post URLs from text."""
        if not text:
            return []
        pattern = r'https?://[a-zA-Z0-9.-]*linkedin\.com/(?:in|posts|jobs|company)/[a-zA-Z0-9_.-]+'
        matches = re.findall(pattern, text)
        clean = []
        for url in matches:
            url_clean = url.rstrip('.,;!?:()[]"\'')
            if url_clean not in clean:
                clean.append(url_clean)
        return clean
