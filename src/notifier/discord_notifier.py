"""Discord webhook notification dispatcher with rich embeds and direct LinkedIn links."""

import requests
from typing import Optional
from src.config import config
from src.models.offer import JobOffer


class DiscordNotifier:
    """Sends real-time PFE alert cards to Anas via Discord Webhook."""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or config.discord_webhook_url

    def is_configured(self) -> bool:
        return bool(self.webhook_url)

    def send_alert(self, offer: JobOffer, email_sent: bool = False) -> bool:
        """Sends rich Discord embed alert."""
        if not self.is_configured():
            return False

        color = 0x22C55E if offer.is_remunerated else 0x3B82F6  # Green if remunerated, Blue otherwise
        remun_text = "🟢 Rémunéré / Gratifié" if offer.is_remunerated else "⚪ Non précisé"
        
        if email_sent:
            action_text = f"✅ Email envoyé avec CV au RH : `{offer.contact_email}`"
        elif offer.contact_email:
            action_text = f"🧪 [Simulation] Email RH détecté : `{offer.contact_email}`"
        else:
            action_text = "⚠️ Email absent -> Postuler manuellement sur LinkedIn"

        fields = [
            {"name": "Entreprise", "value": offer.company, "inline": True},
            {"name": "Localisation", "value": offer.location, "inline": True},
            {"name": "Gratification", "value": remun_text, "inline": True},
            {"name": "Match Score", "value": f"{offer.score}%", "inline": True},
            {"name": "Action RH", "value": action_text, "inline": True},
        ]

        if offer.matched_skills:
            fields.append({"name": "Stack Détectée", "value": ", ".join(offer.matched_skills), "inline": False})

        if offer.hr_linkedin_url:
            hr_label = f"👤 Recruteur RH : {offer.hr_name}" if offer.hr_name else "👤 Recruteur RH LinkedIn"
            fields.append({
                "name": hr_label,
                "value": f"[Ouvrir le Profil du Recruteur]({offer.hr_linkedin_url}) *(Connectez-vous ou envoyez un message direct)*",
                "inline": False
            })

        if offer.linkedin_url:
            fields.append({
                "name": "🔗 Postuler Manuellement sur LinkedIn",
                "value": f"[Accéder directement à l'offre LinkedIn]({offer.linkedin_url})",
                "inline": False
            })
        elif offer.url:
            fields.append({
                "name": "🌐 Lien de l'offre",
                "value": f"[Ouvrir l'offre]({offer.url})",
                "inline": False
            })

        embed = {
            "title": f"🎯 {offer.title}",
            "url": offer.linkedin_url or offer.url,
            "description": f"Nouvelle opportunité de Stage PFE détectée pour Anas Mouqine.",
            "color": color,
            "fields": fields,
            "footer": {"text": f"Source: {offer.source.upper()} | PFE Hunter Agent"}
        }

        try:
            res = requests.post(self.webhook_url, json={"embeds": [embed]}, timeout=10)
            return res.status_code in (200, 204)
        except Exception as e:
            print(f"[ERROR] Failed to send Discord alert: {e}")
            return False
