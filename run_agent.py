"""Main orchestrator for PFE Auto-Hunter & Application Agent."""

import argparse
import sys

# Ensure UTF-8 output encoding across Windows shells and GitHub Actions runners
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from typing import List
from src.config import config
from src.models.offer import JobOffer
from src.scrapers.rekrute_scraper import ReKruteScraper
from src.scrapers.emploima_scraper import EmploiMaScraper
from src.scrapers.linkedin_guest_scraper import LinkedInGuestScraper
from src.matcher.evaluator import OfferEvaluator
from src.storage.state_manager import StateManager
from src.mailer.email_sender import EmailSender
from src.notifier.telegram_notifier import TelegramNotifier
from src.notifier.discord_notifier import DiscordNotifier


def run_agent(dry_run: bool = True) -> int:
    """Executes full scraping, evaluation, dispatching, and alerting pipeline."""
    config.dry_run = dry_run
    print("=" * 70)
    print(f"🚀 PFE HUNTER AGENT STARTING FOR {config.candidate.full_name.upper()}")
    print(f"📍 Cible : {config.candidate.specialization} ({config.candidate.school})")
    print(f"🛡 Mode Sécurité (DRY_RUN) : {'ACTIVÉ (Simulation - Aucun email envoyé)' if config.dry_run else 'DÉSACTIVÉ (Envois Réels)'}")
    print("=" * 70)

    # 1. Initialize Components
    state_manager = StateManager()
    evaluator = OfferEvaluator()
    mailer = EmailSender()
    telegram = TelegramNotifier()
    discord = DiscordNotifier()

    print(f"📡 Statut des Canaux & Secrets :")
    print(f"   - Telegram : {'✅ Configuré (Actif)' if telegram.is_configured() else '⚠️ Non configuré (TELEGRAM_BOT_TOKEN / CHAT_ID manquant)'}")
    print(f"   - Discord  : {'✅ Configuré (Actif)' if discord.is_configured() else '⚠️ Non configuré (DISCORD_WEBHOOK_URL manquant)'}")
    print(f"   - Gmail SMTP : {'✅ Mot de passe détecté' if bool(config.gmail_app_password) else '⚠️ GMAIL_APP_PASSWORD non renseigné'}")
    print("-" * 70)

    scrapers = [
        ReKruteScraper(),
        EmploiMaScraper(),
        LinkedInGuestScraper()
    ]

    all_raw_offers: List[JobOffer] = []

    # 2. Scrape Job Boards for AI & Data PFE Opportunities
    ai_keywords = [
        "stage pfe intelligence artificielle",
        "stage pfe machine learning",
        "stage pfe data"
    ]
    seen_scraped_urls = set()

    for scraper in scrapers:
        print(f"\n🔍 Scraping source : {scraper.name.upper()}...")
        for kw in ai_keywords:
            try:
                offers = scraper.scrape(keyword=kw, location="Casablanca")
                for off in offers:
                    if off.url not in seen_scraped_urls:
                        seen_scraped_urls.add(off.url)
                        all_raw_offers.append(off)
            except Exception as e:
                print(f"   -> [WARNING] Erreur scraper {scraper.name} sur '{kw}': {e}")
        print(f"   -> {len(all_raw_offers)} offres cumulées uniques.")

    # 3. Evaluate & Filter strictly for AI PFE
    print(f"\n🧠 Évaluation et filtrage IA de {len(all_raw_offers)} offres...")
    qualified_offers: List[JobOffer] = []

    for offer in all_raw_offers:
        evaluated = evaluator.evaluate(offer)
        # Strictly require genuine AI domain and student PFE internship
        if evaluator.is_pfe_offer(evaluated) and evaluator.is_ai_offer(evaluated) and evaluated.score >= 50:
            qualified_offers.append(evaluated)

    # Sort: highest score and remunerated first
    qualified_offers.sort(key=lambda o: (o.is_remunerated or False, o.score), reverse=True)
    print(f"   -> {len(qualified_offers)} offres PFE IA qualifiées retenues.")

    # 4. Process each qualified offer
    new_offers_count = 0
    emails_sent_count = 0

    for offer in qualified_offers:
        if state_manager.is_already_seen(offer.id):
            continue

        new_offers_count += 1
        print(f"\n✨ NOUVELLE OFFRE DÉTECTÉE : {offer.title} @ {offer.company} (Score: {offer.score}%)")
        print(f"   📍 Lieu : {offer.location} | Rémunéré : {'OUI' if offer.is_remunerated else 'Non spécifié'}")

        # A. Automated Email if Recruiter / HR email is found
        email_sent = False
        if offer.contact_email:
            print(f"   ✉️ Contact RH identifié : {offer.contact_email}")
            if emails_sent_count < config.max_emails_per_run:
                email_sent = mailer.send_application(offer)
                if email_sent:
                    emails_sent_count += 1
            else:
                print(f"   ⚠️ Limite d'envois atteinte pour cette session ({config.max_emails_per_run})")
        else:
            print("   ℹ️ Aucun email RH public dans la description -> Postulation manuelle requise.")

        # B. LinkedIn Links for Anas to apply/connect manually
        if offer.hr_linkedin_url:
            print(f"   👤 Recruteur RH LinkedIn : {offer.hr_linkedin_url}")
        if offer.linkedin_url:
            print(f"   🔗 Lien LinkedIn pour postuler manuellement : {offer.linkedin_url}")

        # C. Webhook Dispatch (Telegram / Discord)
        telegram.send_alert(offer, email_sent=email_sent)
        discord.send_alert(offer, email_sent=email_sent)

        # D. Save State
        state_manager.record_offer(offer, applied=email_sent, notified=True)

    # 5. Summary
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE L'EXÉCUTION :")
    print(f"   - Total offres brutes analysées : {len(all_raw_offers)}")
    print(f"   - Offres qualifiées PFE retenues : {len(qualified_offers)}")
    print(f"   - Nouvelles offres traitées : {new_offers_count}")
    print(f"   - Candidatures email transmises : {emails_sent_count}")
    print(f"   - Historique total en base : {len(state_manager.data.get('offers', {}))}")
    print("=" * 70 + "\n")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PFE Auto-Hunter Agent")
    parser.add_argument("--live", action="store_true", help="Run in LIVE mode (actually send emails)")
    args = parser.parse_args()

    sys.exit(run_agent(dry_run=not args.live))
