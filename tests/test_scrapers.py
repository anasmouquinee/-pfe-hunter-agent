"""Unit tests for scrapers and HTML parsing."""

from bs4 import BeautifulSoup
from src.scrapers.rekrute_scraper import ReKruteScraper
from src.scrapers.emploima_scraper import EmploiMaScraper
from src.scrapers.linkedin_guest_scraper import LinkedInGuestScraper


MOCK_REKRUTE_HTML = """
<div class="holder">
    <div class="section post-id">
        <h2><a class="titreJob" href="/offre-stage-pfe-data-casablanca.html">Stage PFE -- Data Engineer (Rémunéré)</a></h2>
        <a class="company" href="/company/tech-maroc">Tech Solutions Maroc</a>
        <em class="date">05/01/2026</em>
        <div class="info">
            Recherche stagiaire PFE pour conception de pipelines ETL sous Apache Airflow et Kafka.
            Stage rémunéré avec gratification mensuelle. Envoyez votre CV à rh@techmaroc.ma ou contactez-nous sur https://linkedin.com/in/rh-techmaroc.
        </div>
    </div>
</div>
"""

MOCK_EMPLOIMA_HTML = """
<div class="job-description-wrapper">
    <article class="job-ad">
        <h5><a class="job-title" href="/job/stage-pfe-ia-machine-learning-123">Stagiaire PFE en Intelligence Artificielle</a></h5>
        <div class="company-name">DataCorp Casablanca</div>
        <div class="job-location">Casablanca, Maroc</div>
        <div class="job-description">
            Projet de fin d'études autour des modèles LLM et agents autonomes.
            Contact direct : recrutement@datacorp.ma
        </div>
    </article>
</div>
"""

MOCK_LINKEDIN_HTML = """
<ul class="jobs-search__results-list">
    <li>
        <div class="base-card">
            <h3 class="base-search-card__title">Stage PFE Data & Cloud Architecture</h3>
            <h4 class="base-search-card__subtitle">Cloud Maroc SA</h4>
            <span class="job-search-card__location">Casablanca-Settat, Morocco</span>
            <a class="base-card__full-link" href="https://ma.linkedin.com/jobs/view/stage-pfe-data-123456?refId=abc"></a>
        </div>
    </li>
</ul>
"""


def test_rekrute_parsing():
    scraper = ReKruteScraper()
    soup = BeautifulSoup(MOCK_REKRUTE_HTML, "html.parser")
    offers = scraper.parse_html(soup)

    assert len(offers) == 1
    offer = offers[0]
    assert "Data Engineer" in offer.title
    assert offer.company == "Tech Solutions Maroc"
    assert offer.contact_email == "rh@techmaroc.ma"
    assert offer.linkedin_url == "https://linkedin.com/in/rh-techmaroc"
    assert "rekrute.com" in offer.url


def test_emploima_parsing():
    scraper = EmploiMaScraper()
    soup = BeautifulSoup(MOCK_EMPLOIMA_HTML, "html.parser")
    offers = scraper.parse_html(soup)

    assert len(offers) == 1
    offer = offers[0]
    assert "Intelligence Artificielle" in offer.title
    assert offer.company == "DataCorp Casablanca"
    assert offer.contact_email == "recrutement@datacorp.ma"


def test_linkedin_guest_parsing():
    scraper = LinkedInGuestScraper()
    soup = BeautifulSoup(MOCK_LINKEDIN_HTML, "html.parser")
    offers = scraper.parse_html(soup)

    assert len(offers) == 1
    offer = offers[0]
    assert "Stage PFE" in offer.title
    assert offer.company == "Cloud Maroc SA"
    assert "linkedin.com/jobs/view/stage-pfe-data-123456" in offer.linkedin_url
    assert "?" not in offer.linkedin_url  # Tracking params stripped


def test_linkedin_guest_detail_extraction(monkeypatch):
    scraper = LinkedInGuestScraper()
    mock_detail_html = """
    <div class="decorated-job-posting__details">
        <div class="show-more-less-html__markup">
            Stage PFE Data Engineer. Envoyez votre CV directement à notre équipe RH: stages.maroc@cloudcorp.com.
            Rémunération: 3500 DH/mois.
        </div>
        <div class="message-the-recruiter">
            <a href="https://ma.linkedin.com/in/sarah-recruteur-rh?trk=job_posting">Sarah Alami</a>
        </div>
    </div>
    """

    class MockResponse:
        status_code = 200
        text = mock_detail_html

    monkeypatch.setattr(scraper.session, "get", lambda url, timeout: MockResponse())

    desc, email, hr_link, hr_name = scraper._fetch_job_details(
        "https://ma.linkedin.com/jobs/view/123456", "Stage PFE Data"
    )

    assert email == "stages.maroc@cloudcorp.com"
    assert hr_link == "https://ma.linkedin.com/in/sarah-recruteur-rh"
    assert hr_name == "Sarah Alami"
    assert "3500 DH/mois" in desc

