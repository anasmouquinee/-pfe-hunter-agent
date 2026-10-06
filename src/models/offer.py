"""Unified JobOffer model for scraped PFE opportunities."""

import hashlib
import re
from typing import Optional
from pydantic import BaseModel, Field


class JobOffer(BaseModel):
    id: str = ""
    title: str
    company: str
    location: str = "Casablanca, Maroc"
    url: str
    description: str = ""
    source: str  # "rekrute", "emploima", "linkedin_guest", "linkedin_post"
    contact_email: Optional[str] = None
    linkedin_url: Optional[str] = None  # Direct LinkedIn offer or post URL
    hr_name: Optional[str] = None
    hr_linkedin_url: Optional[str] = None  # Direct Recruiter / HR LinkedIn profile URL
    is_remunerated: Optional[bool] = None
    posted_date: Optional[str] = None
    score: int = 0
    matched_skills: list[str] = Field(default_factory=list)
    applied: bool = False
    notified: bool = False

    def model_post_init(self, __context):
        if not self.id:
            # Deterministic unique hash based on source, company, and title or URL
            hash_input = f"{self.source}:{self.company.lower()}:{self.title.lower()}:{self.url}"
            self.id = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Auto-detect LinkedIn URL if the main URL points to LinkedIn
        if not self.linkedin_url and "linkedin.com" in self.url:
            self.linkedin_url = self.url.split("?")[0]

        if self.description:
            # Auto-extract email from description if present
            if not self.contact_email:
                emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', self.description)
                if emails:
                    valid_emails = [
                        e.rstrip(".,;:)") for e in emails 
                        if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))
                    ]
                    if valid_emails:
                        self.contact_email = valid_emails[0]

            # Auto-extract direct recruiter/HR LinkedIn profile (/in/...)
            if not self.hr_linkedin_url:
                hr_matches = re.findall(r'https?://[a-zA-Z0-9.-]*linkedin\.com/in/[a-zA-Z0-9_-]+', self.description)
                if hr_matches:
                    self.hr_linkedin_url = hr_matches[0].rstrip(".,;:)")
