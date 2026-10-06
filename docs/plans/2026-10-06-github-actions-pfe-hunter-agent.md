# GitHub Actions PFE Auto-Hunter & Application Agent Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an autonomous GitHub Actions agent that scans Moroccan job boards (ReKrute, Emploi.ma, LinkedIn) for 2026 PFE (Projet de Fin d'Études) internship offers in Casablanca (with paid/remunerated preference in AI & Data Engineering), filters and scores them against Anas Mouqine's profile, and automatically (or semi-automatically) dispatches tailored applications with `cv_ats_pfe.pdf`.

**Architecture:** A modular Python pipeline executed via GitHub Actions cron triggers (e.g., twice daily). It features a multi-source web scraper, an LLM-driven filtering & match scoring engine, a JSON state database to guarantee zero duplicate submissions, a secure SMTP mailer attaching `cv_ats_pfe.pdf`, and an optional Telegram/Discord notification webhook for real-time monitoring and human-in-the-loop validation.

**Tech Stack:** Python 3.11, BeautifulSoup4, Requests, Pydantic, Google Gemini API (free tier for offer parsing & cover letter personalization), SMTP (Gmail App Password) / Resend, GitHub Actions (Ubuntu runner, scheduled cron, workflow_dispatch).

---

### Task 1: Environment & Pre-configured Profile Setup

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `src/config.py` (pre-populated with Anas Mouqine's profile, EMSI, IA/Data keywords, and `cv_ats_pfe.pdf` path)
- Create: `tests/test_config.py`

**Step 1: Write test for configuration loading and validation**
- Test environment variables (`GMAIL_USER`, `GMAIL_APP_PASSWORD`, `GEMINI_API_KEY`, `DRY_RUN`).
- Verify pre-configured candidate profile defaults:
  - Name: `Anas Mouqine`
  - School: `EMSI Casablanca` (5ème année - PFE 2026)
  - Domains: `Intelligence Artificielle (IA) & Data Engineering`
  - CV Path: `cv_ats_pfe.pdf`
  - Cities: `["Casablanca", "Casablanca-Settat", "Remote", "Télétravail"]`
  - Target: PFE stage, priority to remunerated (*"rémunéré", "gratification", "indemnité"*).

**Step 2: Implement configuration module**
- Set `DRY_RUN = True` by default for safe local development.

**Step 3: Run test and commit**
- Run: `pytest tests/test_config.py`

---

### Task 2: Moroccan Job Boards & Ban-Proof LinkedIn Scrapers

> **CRITICAL SECURITY NOTE:** Never log in with Anas's personal LinkedIn account or session cookies on GitHub Actions! LinkedIn blocks datacenter IPs and bans accounts. Instead, we use 100% ban-proof methods with ZERO login required:
> 1. Public LinkedIn Guest API (`/jobs-guest/jobs/api/seeMoreJobPostings/search`) - no account needed.
> 2. Google Dorking (`site:linkedin.com/posts "stage pfe" "casablanca" ("data" OR "ia")`) - scrapes public search engines, zero LinkedIn account exposure.
> 3. Native Moroccan Portals (ReKrute & Emploi.ma) - direct access to local enterprise offers with recruiter emails.

**Files:**
- Create: `src/scrapers/base.py`
- Create: `src/scrapers/rekrute_scraper.py`
- Create: `src/scrapers/emploima_scraper.py`
- Create: `src/scrapers/linkedin_guest_scraper.py`
- Create: `src/models/offer.py`
- Create: `tests/test_scrapers.py`
- Create: `src/models/offer.py`
- Create: `tests/test_scrapers.py`

**Step 1: Define the unified JobOffer model**
```python
class JobOffer(BaseModel):
    id: str  # Hash or URL slug
    title: str
    company: str
    location: str
    url: str
    description: str
    source: str  # "rekrute", "emploima", "linkedin"
    is_remunerated: bool | None
    contact_email: str | None
    posted_date: str
```

**Step 2: Implement ReKrute scraper**
- Query URL: `https://www.rekrute.com/offres-emploi-maroc.html?keyword=stage+pfe&region=casablanca`
- Parse HTML: extract title, company, location, full description, and publication date.
- Search description for emails using regex (`r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'`).

**Step 3: Implement Emploi.ma scraper**
- Query URL: `https://www.emploi.ma/recherche-jobs-maroc?f%5B0%5D=im_field_offre_contrat%3Astage&f%5B1%5D=im_field_offre_ville%3A18`
- Extract job listings matching PFE criteria.

**Step 4: Run tests on mock HTML fixtures and commit**
- Verify parsers handle pagination, missing fields, and rate limits gracefully.

---

### Task 3: Offer Scoring & PFE/Remuneration Filtering Engine

**Files:**
- Create: `src/matcher/evaluator.py`
- Create: `tests/test_evaluator.py`

**Step 1: Write test for PFE qualification & remuneration detection**
- Detect keywords: *"rémunéré"*, *"gratification"*, *"indemnité"*, *"bourse de stage"*, *"payé"*.
- Disqualify irrelevant offers (e.g. CDI/CDD 5+ years experience, non-tech positions).

**Step 2: Implement scoring algorithm**
- Score based on tech stack match with Anas Mouqine:
  - High points: AI, Data Engineering, Python, RAG, Airflow, Kafka, Docker, Flutter.
  - Priority boost (+20 points) if explicitly *rémunéré / gratification*.
  - Disqualifier: Mandatory on-site outside Casablanca/Mohammedia.
- Optional Gemini API integration to parse complex unstructured descriptions and extract recruiter emails.

**Step 3: Run test and commit**
- Run: `pytest tests/test_evaluator.py`
- Git commit.

---

### Task 4: Deduplication & State Tracking Engine

**Files:**
- Create: `src/storage/state_manager.py`
- Create: `data/applied_offers.json`
- Create: `tests/test_state_manager.py`

**Step 1: Write state persistence logic**
- Load existing offers from `data/applied_offers.json`.
- Check if `offer.id` was already scraped, notified, or applied to.
- Record submission timestamp, company, status (`"scraped"`, `"notified"`, `"applied"`).
- Save updated state cleanly with indentation.

**Step 2: Run test and commit**
- Ensure idempotency: running the workflow twice consecutively produces 0 duplicate actions.

---

### Task 5: Tailored Email Dispatcher & CV Attachment

**Files:**
- Create: `src/mailer/email_sender.py`
- Create: `src/mailer/cover_letter_generator.py`
- Create: `tests/test_mailer.py`

**Step 1: Implement dynamic cover letter generator**
- Generate professional, concise French application email tailored to the targeted company:
  - Subject: `Candidature Stage PFE (4-6 mois) -- Ingénieur IA & Data Engineering -- Anas Mouqine`
  - Body: Reference the company name, specific project/stack mentioned in their offer, Anas's background at EMSI & internships (COSUMAR, SEWS-CABINET), and availability for 2026.

**Step 2: Implement SMTP mailer with PDF attachment**
- Use Python `smtplib` and `email.mime` with SSL/TLS.
- Attach [`cv_ats_pfe.pdf`](file:///c:/Users/anasm/Documents/cv/cv_ats_pfe.pdf).
- Add safety checks:
  - If `DRY_RUN=True`, do not send email, log output to console and artifact.
  - Maximum 5 emails per execution run (rate limiter against spam/abuse).
  - Whitelist/Blacklist filter for domains.

**Step 3: Run test with dry-run mode and commit**
- Run: `pytest tests/test_mailer.py`

---

### Task 6: Notification Webhook (Telegram / Discord Digest with 1-Click LinkedIn Links)

**Files:**
- Create: `src/notifier/telegram_notifier.py`
- Create: `src/notifier/discord_notifier.py`
- Create: `tests/test_notifier.py`

**Step 1: Implement instant alert service with dual action**
- For every matched offer, send rich notification to Anas's phone via Telegram/Discord:
  - **Company & Title:** e.g. `Stage PFE Data Engineer (Rémunéré) - Tech Corp`
  - **Match Score & Location:** `Score: 94% | Casablanca`
  - **Email Action:** `Candidature envoyée par email à rh@techcorp.ma avec cv_ats_pfe.pdf` (or `Email non trouvé`)
  - **Direct LinkedIn Link:** Clickable button or URL `[Voir le post/profil RH sur LinkedIn]` so Anas can immediately open LinkedIn, connect with the recruiter, and follow up or apply manually.
  - **Remuneration Status:** `🟢 Rémunéré / Gratification mentionnée`

**Step 2: Run test with mock webhook and commit**

---

### Task 7: GitHub Actions Workflow Integration

**Files:**
- Create: `.github/workflows/pfe_hunter_agent.yml`
- Create: `run_agent.py`

**Step 1: Implement main entry point `run_agent.py`**
- Coordinate: Scrape -> Filter & Score -> Deduplicate -> Dispatch / Notify -> Save state.

**Step 2: Create GitHub Actions workflow `.github/workflows/pfe_hunter_agent.yml`**
- Scheduled cron: Run Monday to Friday at 09:00 UTC and 14:00 UTC (`cron: '0 9,14 * * 1-5'`).
- Manual trigger: `workflow_dispatch` with dry-run toggle input.
- Steps:
  1. Checkout repository with full history.
  2. Set up Python 3.11.
  3. Install dependencies (`pip install -r requirements.txt`).
  4. Run `python run_agent.py`.
  5. Auto-commit and push updated `data/applied_offers.json` to the repo to maintain state across runs.

**Step 3: Documentation in `README_AGENT.md`**
- Setup guide for GitHub Secrets:
  - `GMAIL_USER`
  - `GMAIL_APP_PASSWORD`
  - `GEMINI_API_KEY` (optional)
  - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID` (optional)

---

### Task 8: Local Dry-Run & End-to-End Simulation

**Files:**
- Execute dry run: `python run_agent.py --dry-run`

**Step 1: Execute local dry-run**
- Verify scraping returns actual live PFE offers in Casablanca.
- Verify filtering identifies remunerated/AI/Data keywords.
- Verify email drafting formats correctly with `cv_ats_pfe.pdf` attached.
- Verify state updates without errors.
