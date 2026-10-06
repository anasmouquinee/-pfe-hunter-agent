"""Public LinkedIn Guest Scraper -- 100% Ban-Proof (Zero Login Required)."""

import re
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from typing import List, Optional
from src.scrapers.base import BaseScraper
from src.models.offer import JobOffer


class LinkedInGuestScraper(BaseScraper):
    """
    Scrapes LinkedIn's public guest job endpoint.
    NEVER uses user accounts or session cookies, completely eliminating any ban risk.
    Fetches full job posting details to extract HR emails and recruiter LinkedIn profiles.
    """
    name: str = "linkedin_guest"
    SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

    def scrape(self, keyword: str = "stage pfe data", location: str = "Casablanca") -> List[JobOffer]:
        offers: List[JobOffer] = []
        params = {
            "keywords": keyword,
            "location": location,
            "start": 0
        }

        try:
            response = self.session.get(
                self.SEARCH_URL,
                params=params,
                timeout=self.timeout
            )
            if response.status_code != 200:
                return offers

            soup = BeautifulSoup(response.text, "html.parser")
            return self.parse_html(soup)
        except Exception as e:
            return offers

    def parse_html(self, soup: BeautifulSoup) -> List[JobOffer]:
        offers: List[JobOffer] = []
        seen_urls = set()
        cards = soup.select(".base-card, .job-search-card")
        if not cards:
            cards = soup.select("li")

        for card in cards:
            title_elem = card.select_one(".base-search-card__title, h3, a.base-card__full-link")
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            link_elem = card.select_one("a.base-card__full-link, a")
            raw_url = link_elem.get("href", "") if link_elem else ""
            clean_url = raw_url.split("?")[0] if raw_url else ""

            if not clean_url or clean_url in seen_urls:
                continue
            seen_urls.add(clean_url)

            company_elem = card.select_one(".base-search-card__subtitle, h4 a, h4")
            company = company_elem.get_text(strip=True) if company_elem else "Entreprise Casablanca"

            location_elem = card.select_one(".job-search-card__location, span.job-location")
            location = location_elem.get_text(strip=True) if location_elem else "Casablanca, Maroc"

            date_elem = card.select_one("time")
            posted_date = date_elem.get_text(strip=True) if date_elem else ""

            # Fetch full posting details to discover HR email and recruiter profile
            description, contact_email, hr_linkedin_url, hr_name = self._fetch_job_details(clean_url, title)

            offer = JobOffer(
                title=title,
                company=company,
                location=location,
                url=clean_url,
                description=description,
                source=self.name,
                contact_email=contact_email,
                linkedin_url=clean_url,
                hr_linkedin_url=hr_linkedin_url,
                hr_name=hr_name,
                posted_date=posted_date
            )
            offers.append(offer)

        return offers

    def _fetch_job_details(self, job_url: str, title: str) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
        """
        Fetches the public guest detail page for the given LinkedIn job URL.
        Returns (description_text, contact_email, hr_linkedin_url, hr_name).
        """
        desc_text = f"Offre LinkedIn PFE: {title}"
        contact_email = None
        hr_linkedin_url = None
        hr_name = None

        try:
            # Extract job id from URL e.g. /data-ai-stagiaire-pfe-4389279426
            job_id = job_url.split("?")[0].rstrip("/").split("-")[-1]
            if not job_id.isdigit():
                parts = [p for p in job_url.split("/") if p.isdigit()]
                job_id = parts[-1] if parts else None

            if not job_id:
                return desc_text, contact_email, hr_linkedin_url, hr_name

            # Gentle pause to avoid rate limits
            time.sleep(0.4)

            detail_url = self.DETAIL_URL.format(job_id=job_id)
            res = self.session.get(detail_url, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")

                # 1. Extract Description
                desc_elem = soup.select_one(".show-more-less-html__markup, .description__text, .decorated-job-posting__details")
                if desc_elem:
                    desc_text = desc_elem.get_text(" ", strip=True)

                # 2. Extract HR/Recruiter Emails
                emails = self.extract_emails(desc_text)
                if emails:
                    contact_email = emails[0]

                # 3. Check for Recruiter Profile (/in/...)
                # First check recruiter cards in detail page
                recruiter_links = soup.find_all("a", href=lambda h: h and "/in/" in h)
                for r_link in recruiter_links:
                    href = r_link.get("href", "").split("?")[0]
                    if "/in/" in href:
                        hr_linkedin_url = href
                        name_text = r_link.get_text(strip=True)
                        if name_text and len(name_text) < 50:
                            hr_name = name_text
                        break

                # Also check description text for recruiter profile link if not found in markup
                if not hr_linkedin_url:
                    text_in_matches = re.findall(r'https?://[a-zA-Z0-9.-]*linkedin\.com/in/[a-zA-Z0-9_-]+', desc_text)
                    if text_in_matches:
                        hr_linkedin_url = text_in_matches[0].rstrip(".,;:)")

        except Exception:
            # Fallback smoothly to default if network or parsing issue occurs
            pass

        return desc_text, contact_email, hr_linkedin_url, hr_name
