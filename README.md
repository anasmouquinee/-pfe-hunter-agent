# 🚀 Plateforme PFE 2026 : CV Haute Fidélité & Agent Autonome PFE Hunter

Ce dépôt regroupe l'écosystème complet de recherche de **Stage PFE 2026** (Casablanca & Maroc) pour **Anas Mouqine** (Élève-Ingénieur 5ème année à l'**EMSI Casablanca**, Spécialisation Intelligence Artificielle & Data Engineering).

Il est composé de deux briques synergiques :
1. **🤖 L'Agent Autonome PFE Hunter** : Pipeline Python automatisé avec GitHub Actions, scrapers multi-sources 0% ban-risk, scoring IA anti-faux-positifs, dispatching d'emails personnalisés (HTML & texte) avec CV ATS et notifications webhook temps réel (Telegram & Discord).
2. **📄 La Suite de CV Professionnels LaTeX** : CVs au format standard et ATS optimisés pour les recruteurs techniques et filtres automatiques.

---

## 🤖 1. Agent Autonome PFE Hunter

L'agent analyse en continu les opportunités de stages PFE au Maroc et filtre avec une stricte précision les offres d'Intelligence Artificielle et Data Engineering.

### 🌟 Fonctionnalités Clés
- **Scraping Multi-Plateformes (6 Sources 0% Ban Risk)** :
  - **DreamJob.ma** : Portail n°1 des campagnes PFE d'entreprises au Maroc (Capgemini, Orange, SQORUS, DATAPROTECT, etc.) avec extraction automatique des emails RH et posts LinkedIn.
  - **Talent.com Maroc** : Moteur d'agrégation des offres d'emploi et stages technologiques à Casablanca et au Maroc.
  - **LinkedIn Guest API** : Recherche publique avec rotation de session & User-Agent anti-429, extraction des fiches recruteurs sans risque de ban.
  - **ReKrute.ma** : Portail des multinationales et ESN majeures du marché marocain.
  - **MarocAnnonces** : Catégorie 309 (Offres d'emploi & stages Casablanca/National).
  - **Emploi.ma** : Scraper de secours avec contournement 403.
- **Scoring & Filtrage IA Rigoureux** : Analyse sémantique avancée excluant les faux-positifs de la langue française (*"j'ai"*) et valorisant les technologies clés (Python, RAG, Airflow, Kafka, Docker, LangChain).
- **Extraction RH & LinkedIn** : Détection des adresses emails recruteurs et profils personnels LinkedIn (`/in/...`) pour connexion en 1 clic.
- **Postulation Automatique (Gmail SMTP)** : Génération d'une lettre de motivation adaptative (HTML responsive & texte brut) avec attachement de [`cv_ats_pfe.pdf`](cv_ats_pfe.pdf).
- **Notifications Webhook (Telegram & Discord)** : Cartes interactives avec liens cliquables directs vers le recruteur et l'offre.
- **Persistance & Anti-Doublons** : Suivi fin séparant simulations et candidatures réelles dans [`data/applied_offers.json`](data/applied_offers.json).

### 🛠️ Commandes CLI Utiles
```powershell
# 1. Mode simulation sécurisé (dry-run)
python run_agent.py

# 2. Mode envoi réel de candidatures
python run_agent.py --live

# 3. Tester vos canaux de notification (Telegram & Discord)
python run_agent.py --test-notifications

# 4. Afficher le tableau de bord des statistiques
python run_agent.py --stats

# 5. Recherche ciblée sur un mot-clé précis
python run_agent.py --keyword "stage pfe data engineering" --limit 5

# 6. Exécuter l'ensemble de la suite de tests (27 tests)
pytest tests/ -v
```

> 📖 Pour la documentation complète de configuration GitHub Actions et secrets, consultez **[`README_AGENT.md`](README_AGENT.md)**.

---

## 📄 2. Suite de CVs LaTeX Professionnels

| Fichier | Format | Description |
| :--- | :--- | :--- |
| **[`cv_modern_pfe.tex`](cv_modern_pfe.tex)** | LaTeX | CV moderne et visuel avec mise en page élégante sur 1 page A4. |
| **[`cv_modern_pfe.pdf`](cv_modern_pfe.pdf)** | PDF | Rendu compilé haute fidélité du CV moderne. |
| **[`cv_ats_pfe.tex`](cv_ats_pfe.tex)** | LaTeX | Version ultra-optimisée pour les parseurs ATS (Applicant Tracking Systems). |
| **[`cv_ats_pfe.pdf`](cv_ats_pfe.pdf)** | PDF | Rendu compilé utilisé par l'agent pour les envois aux recruteurs. |
| **[`cv_preview.png`](cv_preview.png)** | Image | Aperçu haute définition (200 DPI). |

### 🛠️ Compilation Locale LaTeX
Votre système dispose de **MiKTeX** avec `pdflatex` :
```powershell
pdflatex -interaction=nonstopmode cv_modern_pfe.tex
pdflatex -interaction=nonstopmode cv_ats_pfe.tex
```

Pour rafraîchir l'aperçu image :
```powershell
python -c "import fitz; doc=fitz.open('cv_modern_pfe.pdf'); doc[0].get_pixmap(dpi=200).save('cv_preview.png')"
```

---

## 📂 Structure du Répertoire

```text
cv/
├── .github/workflows/
│   └── pfe_hunter_agent.yml      # Workflow GitHub Actions automatisé
├── data/
│   └── applied_offers.json       # Base d'état et historique des offres
├── docs/
│   ├── content_synthesis.md      # Synthèse profil, expériences et certifications
│   └── plans/                    # Plans d'architecture et de conception
├── src/
│   ├── config.py                 # Profil candidat & configuration globale
│   ├── mailer/
│   │   ├── cover_letter_generator.py # Lettre de motivation adaptative (HTML + texte)
│   │   └── email_sender.py       # Envoi SMTP sécurisé avec pièce jointe
│   ├── matcher/
│   │   └── evaluator.py          # Moteur de scoring & filtrage IA anti-faux-positifs
│   ├── models/
│   │   └── offer.py              # Modèle unifié JobOffer
│   ├── notifier/
│   │   ├── discord_notifier.py   # Alertes Discord Webhook avec embeds
│   │   └── telegram_notifier.py  # Alertes Telegram Bot en HTML sécurisé
│   ├── scrapers/
│   │   ├── base.py               # Classe de base HTTP et parsing
│   │   ├── emploima_scraper.py   # Scraper Emploi.ma avec gestion 403
│   │   ├── linkedin_guest_scraper.py # Scraper public LinkedIn Guest (0% ban risk)
│   │   └── rekrute_scraper.py    # Scraper ReKrute Casablanca
│   ├── storage/
│   │   └── state_manager.py      # Persistance et déduplication
│   └── utils/
│       ├── logger.py             # Logging centralisé standardisé
│       └── text_extractor.py     # Extraction DRY des emails, URLs et profils RH
├── tests/                        # 24 tests unitaires complets
├── cv_ats_pfe.pdf                # CV ATS officiel envoyé aux recruteurs
├── cv_modern_pfe.pdf             # CV visuel 1 page
├── run_agent.py                  # Point d'entrée orchestrateur CLI
└── requirements.txt              # Dépendances Python
```
