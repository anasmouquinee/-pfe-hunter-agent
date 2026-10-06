"""ReKrute scraper for Moroccan PFE offers."""

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer


class ReKruteScraper(BaseScraper):
    name: str = "rekrute"
    BASE_URL = "https://www.rekrute.com"

    def scrape(self, keyword: str = "stage pfe", location: str = "Casablanca") -> List[JobOffer]:
        offers: List[JobOffer] = []
        search_query = quote_plus(keyword)
        url = f"{self.BASE_URL}/offres-emploi-maroc.html?keyword={search_query}&region=casablanca"

        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                return offers
            
            soup = BeautifulSoup(response.text, "html.parser")
            return self.parse_html(soup)
        except Exception:
            return offers

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        # ReKrute offer cards generally have class 'post-id' or 'holder'
        cards = soup.select(".post-id, li.holder, div.section")

        for card in cards:
            title_elem = card.select_one(".titreJob, h2 a, h3 a, a.title")
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            href = title_elem.get("href", "")
            url = f"{self.BASE_URL}{href}" if href.startswith("/") else href

            company_elem = card.select_one(".company, .info a, img[alt]")
            company = "Entreprise Partenaire"
            if company_elem:
                if company_elem.name == "img" and company_elem.get("alt"):
                    company = company_elem["alt"].strip()
                elif company_elem.get_text(strip=True):
                    company = company_elem.get_text(strip=True)

            desc_elem = card.select_one(".info, .text, .blc, p")
            desc_text = desc_elem.get_text(" ", strip=True) if desc_elem else title

            date_elem = card.select_one(".date, em.date, span.date")
            posted_date = date_elem.get_text(strip=True) if date_elem else ""

            emails = self.extract_emails(desc_text)
            contact_email = emails[0] if emails else None
            linkedin_urls = self.extract_linkedin_urls(desc_text)
            linkedin_url = linkedin_urls[0] if linkedin_urls else None

            offer = JobOffer(
                title=title,
                company=company,
                location="Casablanca, Maroc",
                url=url,
                description=desc_text,
                source=self.name,
                contact_email=contact_email,
                linkedin_url=linkedin_url,
                posted_date=posted_date
            )
            offers.append(offer)

        return offers
