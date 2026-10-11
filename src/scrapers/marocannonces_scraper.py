"""MarocAnnonces scraper for Moroccan PFE and internship offers."""

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer
from src.utils.text_extractor import clean_url
from src.utils.logger import logger


class MarocAnnoncesScraper(BaseScraper):
    name: str = "marocannonces"
    BASE_URL = "https://www.marocannonces.com"

    def scrape(self, keyword: str = "stage", location: str = "Casablanca") -> List[JobOffer]:
        offers: List[JobOffer] = []
        search_query = quote_plus(keyword)
        # Category 309 corresponds to 'Offres d'emploi' (enterprise job postings)
        url = f"{self.BASE_URL}/maroc/offres-emploi-casablanca-b309.html?kw={search_query}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.warning("MarocAnnonces returned HTTP %s for query '%s'", response.status_code, keyword)
                return offers

            soup = BeautifulSoup(response.text, "html.parser")
            parsed_offers = self.parse_html(soup)
            logger.info("MarocAnnonces found %d offers for '%s'", len(parsed_offers), keyword)
            return parsed_offers
        except Exception as e:
            logger.error("Error scraping MarocAnnonces for '%s': %s", keyword, e)
            return offers

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        seen_urls = set()
        cards = soup.select("ul.cars-list li")

        for card in cards:
            a_elem = card.find("a")
            if not a_elem:
                continue

            h3_elem = a_elem.find("h3")
            title = h3_elem.get_text(strip=True) if h3_elem else a_elem.get_text(strip=True)
            if not title:
                continue

            raw_href = a_elem.get("href", "")
            if not raw_href:
                continue

            full_url = f"{self.BASE_URL}/{raw_href.lstrip('/')}"
            url = clean_url(full_url)

            if url in seen_urls:
                continue
            seen_urls.add(url)

            # Location / City
            loc_elem = card.select_one(".location, .used-car-city, span.city")
            location_text = loc_elem.get_text(strip=True) if loc_elem else "Casablanca, Maroc"

            # Date
            date_elem = card.select_one(".date, span.date")
            posted_date = date_elem.get_text(strip=True) if date_elem else ""

            # Description snippet
            desc_elem = card.select_one("p, .desc")
            desc_text = desc_elem.get_text(" ", strip=True) if desc_elem else title

            emails = self.extract_emails(desc_text)
            contact_email = emails[0] if emails else None

            offer = JobOffer(
                title=title,
                company="Entreprise Partenaire (MarocAnnonces)",
                location=location_text,
                url=url,
                description=desc_text,
                source=self.name,
                contact_email=contact_email,
                posted_date=posted_date,
            )
            offers.append(offer)

        return offers
