"""Telegram notification dispatcher with rich LinkedIn and application links."""

import requests
from typing import Optional
from src.config import config
from src.models.offer import JobOffer


class TelegramNotifier:
    """Sends real-time PFE alert cards to Anas via Telegram Bot."""

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or config.telegram_bot_token
        self.chat_id = chat_id or config.telegram_chat_id

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def format_message(self, offer: JobOffer, email_sent: bool = False) -> str:
        """Formats an offer into a clean markdown card with direct LinkedIn link."""
        remun_icon = "🟢 Rémunéré / Gratifié" if offer.is_remunerated else "⚪ Non précisé"
        
        if email_sent:
            action_text = f"✅ Email envoyé avec CV au RH : `{offer.contact_email}`"
        elif offer.contact_email:
            action_text = f"🧪 [Simulation] Email RH détecté : `{offer.contact_email}`"
        else:
            action_text = "⚠️ Email absent -> À postuler manuellement sur LinkedIn"

        skills_str = ", ".join(offer.matched_skills) if offer.matched_skills else "IA / Data"

        msg = (
            f"🎯 *NOUVELLE OPPORTUNITÉ STAGE PFE (Match: {offer.score}%)*\n\n"
            f"🏢 *Entreprise :* {offer.company}\n"
            f"📌 *Poste :* {offer.title}\n"
            f"📍 *Ville :* {offer.location}\n"
            f"💰 *Gratification :* {remun_icon}\n"
            f"🛠 *Stack :* {skills_str}\n"
            f"📤 *Statut Candidature :* {action_text}\n"
        )

        if offer.hr_linkedin_url:
            msg += f"\n👤 *Profil LinkedIn Recruteur RH :*\n👉 {offer.hr_linkedin_url}\n_(Connectez-vous ou envoyez un message direct)_\n"

        if offer.linkedin_url:
            msg += f"\n🔗 *Lien LinkedIn (Postuler Manuellement) :*\n👉 {offer.linkedin_url}\n"
        elif offer.url:
            msg += f"\n🌐 *Lien de l'offre :*\n👉 {offer.url}\n"

        return msg

    def send_alert(self, offer: JobOffer, email_sent: bool = False) -> bool:
        """Sends Telegram alert."""
        if not self.is_configured():
            print("[INFO] Telegram notifier not configured (skipping).")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": self.format_message(offer, email_sent),
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }

        try:
            res = requests.post(url, json=payload, timeout=10)
            return res.status_code == 200
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram alert: {e}")
            return False
