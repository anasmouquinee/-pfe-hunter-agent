"""Emploi.ma scraper for Moroccan PFE opportunities."""

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer
from src.utils.logger import logger


class EmploiMaScraper(BaseScraper):
    name: str = "emploima"
    BASE_URL = "https://www.emploi.ma"

    def scrape(self, keyword: str = "pfe", location: str = "Casablanca") -> List[JobOffer]:
        offers: List[JobOffer] = []
        search_query = quote_plus(keyword)
        url = f"{self.BASE_URL}/recherche-jobs-maroc?keyword={search_query}&f%5B0%5D=im_field_offre_contrat%3Astage"

        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 403:
                logger.warning("Emploi.ma returned HTTP 403 (Cloudflare/WAF protection enabled) - skipping gracefully")
                return offers
            elif response.status_code != 200:
                logger.warning("Emploi.ma returned HTTP %s for query '%s'", response.status_code, keyword)
                return offers

            soup = BeautifulSoup(response.text, "html.parser")
            parsed_offers = self.parse_html(soup)
            logger.info("Emploi.ma found %d offers for '%s'", len(parsed_offers), keyword)
            return parsed_offers
        except Exception as e:
            logger.error("Error scraping Emploi.ma for '%s': %s", keyword, e)
            return offers

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        seen_urls = set()
        cards = soup.select("article.job-ad, .views-row, .job-description-wrapper")

        for card in cards:
            title_elem = card.select_one("h5 a, h3 a, a.job-title")
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            href = title_elem.get("href", "")
            url = f"{self.BASE_URL}{href}" if href.startswith("/") else href

            if url in seen_urls:
                continue
            seen_urls.add(url)

            company_elem = card.select_one(".company-name, .job-company, a.company")
            company = company_elem.get_text(strip=True) if company_elem else "Entreprise Casablanca"

            location_elem = card.select_one(".job-location, .location")
            loc_text = location_elem.get_text(strip=True) if location_elem else "Casablanca, Maroc"

            desc_elem = card.select_one(".job-description, p.text")
            desc_text = desc_elem.get_text(" ", strip=True) if desc_elem else title

            emails = self.extract_emails(desc_text)
            contact_email = emails[0] if emails else None
            linkedin_urls = self.extract_linkedin_urls(desc_text)
            linkedin_url = linkedin_urls[0] if linkedin_urls else None

            offer = JobOffer(
                title=title,
                company=company,
                location=loc_text,
                url=url,
                description=desc_text,
                source=self.name,
                contact_email=contact_email,
                linkedin_url=linkedin_url,
            )
            offers.append(offer)

        return offers
