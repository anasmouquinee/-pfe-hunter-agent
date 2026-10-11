"""Talent.com Morocco scraper for IT, Data, and internship listings."""

import re
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Optional
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer
from src.utils.text_extractor import clean_url, extract_emails
from src.utils.logger import logger


class TalentScraper(BaseScraper):
    """
    Scrapes Talent.com Morocco (ma.talent.com), which aggregates tech jobs and
    internships from top employers across Casablanca and Morocco.
    """
    name: str = "talent"
    BASE_URL = "https://ma.talent.com"

    def scrape(self, keyword: str = "stage pfe data", location: str = "Casablanca") -> List[JobOffer]:
        offers: List[JobOffer] = []
        loc = "Casablanca" if "casa" in location.lower() else location
        url = f"{self.BASE_URL}/jobs?k={quote_plus(keyword)}&l={quote_plus(loc)}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.warning("Talent.com returned HTTP %s for query '%s'", response.status_code, keyword)
                return offers

            soup = BeautifulSoup(response.text, "html.parser")
            parsed_offers = self.parse_html(soup)
            logger.info("Talent.com found %d offers for '%s'", len(parsed_offers), keyword)
            return parsed_offers
        except Exception as e:
            logger.error("Error scraping Talent.com for '%s': %s", keyword, e)
            return offers

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        seen_urls = set()

        cards = soup.select('article[class*="JobCard_card"]')
        for card in cards:
            title_el = card.select_one('[class*="JobCard_title"]')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)

            link_el = card.find("a", href=True)
            if not link_el:
                continue
            raw_url = link_el["href"]
            if raw_url.startswith("/"):
                raw_url = f"{self.BASE_URL}{raw_url}"
            url = clean_url(raw_url)

            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            comp_el = card.select_one('[class*="JobCard_company"]')
            company = comp_el.get_text(strip=True) if comp_el else "Entreprise (Talent.com)"

            loc_el = card.select_one('[class*="JobCard_location"]')
            location = loc_el.get_text(strip=True) if loc_el else "Casablanca, Maroc"

            desc_el = card.select_one('p, [class*="JobCard_description"], [class*="JobCard_snippet"]')
            snippet = desc_el.get_text(" ", strip=True) if desc_el else title
            # Clean trailing navigation text
            snippet = re.sub(r'\s*Voir plus\s*$', '', snippet, flags=re.IGNORECASE).strip()

            emails = extract_emails(snippet)
            contact_email = emails[0] if emails else None

            offer = JobOffer(
                title=title,
                company=company,
                location=location,
                url=url,
                description=f"{title} - {snippet}",
                source=self.name,
                contact_email=contact_email,
            )
            offers.append(offer)

        return offers
