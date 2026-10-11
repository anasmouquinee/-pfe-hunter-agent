"""DreamJob.ma scraper for Moroccan PFE and pre-employment internship campaigns."""

import re
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer
from src.utils.text_extractor import clean_url, extract_emails, extract_linkedin_urls, extract_recruiter_profile
from src.utils.logger import logger


class DreamJobScraper(BaseScraper):
    """
    Scrapes DreamJob.ma, Morocco's leading recruitment portal for corporate
    PFE campaigns (Capgemini, Orange, SQORUS, DATAPROTECT, etc.).
    Extracts direct recruiter emails and LinkedIn post links from campaign detail pages.
    """
    name: str = "dreamjob"
    BASE_URL = "https://www.dreamjob.ma"

    RELEVANT_PATTERNS = [
        r'\bstage\b',
        r'\bpfe\b',
        r'\bdata\b',
        r'\bia\b',
        r'\bai\b',
        r'intelligence artificielle',
        r'machine learning',
        r'python',
        r'stagiaire',
        r'ingénieur',
        r'ingenieur',
        r'engineer',
        r'développeur',
        r'developpeur',
        r'informatique',
        r'pré-embauche',
        r'pre-embauche',
        r'consultant',
        r'cloud',
    ]

    def _is_relevant_title(self, title: str) -> bool:
        """Determines if campaign title is relevant to engineering/internships before fetching details."""
        title_lower = title.lower()
        return any(re.search(pat, title_lower) for pat in self.RELEVANT_PATTERNS)

    def scrape(self, keyword: str = "stage pfe data", location: str = "Casablanca", max_pages: int = 2) -> List[JobOffer]:
        offers: List[JobOffer] = []
        search_query = quote_plus(keyword)

        for page in range(1, max_pages + 1):
            if page == 1:
                url = f"{self.BASE_URL}/?s={search_query}"
            else:
                url = f"{self.BASE_URL}/page/{page}/?s={search_query}"

            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code != 200:
                    if page == 1:
                        logger.warning("DreamJob returned HTTP %s for query '%s'", response.status_code, keyword)
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                parsed = self.parse_html(soup)
                offers.extend(parsed)
            except Exception as e:
                logger.error("Error scraping DreamJob page %d for '%s': %s", page, keyword, e)
                break

        logger.info("DreamJob found %d offers for '%s'", len(offers), keyword)
        return offers

    def _extract_company_from_title(self, title: str) -> str:
        """Heuristically extracts company name from Moroccan campaign titles."""
        patterns = [
            r'(?:chez|at)\s+([A-Za-z0-9\s.&_-]+?)(?:\s*[-–:]|\s+lance|\s+recrute|\s+au|\s+en|\s*$)',
            r'([A-Za-z0-9\s.&_-]+?)\s+(?:lance|recrute|ouvre|cherche|organise)\s+(?:des|sa|un|ses)',
            r'Rejoignez\s+([A-Za-z0-9.&_-]+(?:\s+[A-Za-z0-9.&_-]+)?)',
        ]
        for p in patterns:
            match = re.search(p, title, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip(" :,-–")
                if 2 < len(candidate) < 35:
                    return candidate
        return "Entreprise Maroc"

    def _fetch_article_details(self, article_url: str) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
        """
        Fetches the full campaign article page to discover HR contact emails,
        recruiter profiles, and full job descriptions.
        """
        desc_text = ""
        contact_email = None
        linkedin_url = None
        hr_linkedin_url = None

        try:
            time.sleep(0.2)
            res = self.session.get(article_url, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                content_elem = soup.select_one(".entry-content, .post-content, article")
                if content_elem:
                    desc_text = content_elem.get_text(" ", strip=True)

                    # Extract emails
                    emails = extract_emails(desc_text)
                    if emails:
                        contact_email = emails[0]

                    # Extract LinkedIn links (recruiter profile or campaign post)
                    li_urls = extract_linkedin_urls(desc_text)
                    if li_urls:
                        linkedin_url = li_urls[0]

                    hr_profile = extract_recruiter_profile(desc_text)
                    if hr_profile:
                        hr_linkedin_url = hr_profile

        except Exception as e:
            logger.debug("Failed to fetch DreamJob details for %s: %s", article_url, e)

        return desc_text, contact_email, linkedin_url, hr_linkedin_url

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        seen_urls = set()
        articles = soup.select("article, .post-item, div.post")

        for article in articles:
            title_elem = article.select_one("h2.entry-title a, h2 a, h3 a, a.entry-title-link")
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            raw_url = title_elem.get("href", "")
            url = clean_url(raw_url)

            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            company = self._extract_company_from_title(title)

            # Date
            date_elem = article.select_one("time, .post-date, .entry-date")
            posted_date = date_elem.get_text(strip=True) if date_elem else ""

            # Check relevance before fetching details to preserve latency & avoid useless requests
            detail_desc, contact_email, li_url, hr_url = "", None, None, None
            if self._is_relevant_title(title):
                detail_desc, contact_email, li_url, hr_url = self._fetch_article_details(url)

            full_desc = detail_desc if detail_desc else title

            offer = JobOffer(
                title=title,
                company=company,
                location="Casablanca, Maroc",
                url=url,
                description=full_desc,
                source=self.name,
                contact_email=contact_email,
                linkedin_url=li_url,
                hr_linkedin_url=hr_url,
                posted_date=posted_date,
            )
            offers.append(offer)

        return offers
