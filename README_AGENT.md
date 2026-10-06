# 🤖 Agent GitHub Actions : PFE Hunter & Postulation Automatique

Bienvenue dans votre agent autonome de recherche et postulation de **Stage PFE 2026** (Casablanca & Maroc), conçu spécialement pour **Anas Mouqine** (Élève-Ingénieur 5ème année à l'**EMSI**, Spécialité IA & Data Engineering).

---

## 🎯 Fonctionnalités Clés

1. **Scraping Multi-Plateformes Sans Risque de Ban (0% Ban Risk)** :
   - **LinkedIn Guest API** : Interroge les endpoints publics de LinkedIn sans aucune connexion de compte ni cookie de session. Aucun risque de bannissement de compte personnel.
   - **ReKrute Maroc** : Offres de stages PFE à Casablanca.
   - **Emploi.ma** : Offres de stages pré-embauche et PFE.

2. **Extraction RH & LinkedIn Avancée** :
   - Analyse le descriptif complet de chaque offre.
   - **Si un e-mail RH est trouvé** : Génère automatiquement un e-mail de motivation personnalisé en français et y joint votre CV optimisé ATS ([`cv_ats_pfe.pdf`](cv_ats_pfe.pdf)).
   - **Envoi sur votre Webhook (Telegram / Discord)** : Transmet systématiquement le **lien direct LinkedIn de l'offre** ainsi que le **profil LinkedIn personnel du recruteur RH** (ex: `linkedin.com/in/...`) pour que vous puissiez :
     - Postuler manuellement en un clic.
     - Envoyer un message ou une demande de connexion directe au recruteur.

3. **Détection de Rémunération & Scoring** :
   - Détecte les mentions de gratification (`rémunéré`, `gratification`, `indemnité`, `DH/mois`).
   - Calcule un score de pertinence (0 à 100%) basé sur vos technologies clés (Python, RAG, Airflow, Docker, LangChain, Kafka, SQL, etc.).

4. **Persistance & Anti-Doublons** :
   - Chaque offre traitée est enregistrée dans [`data/applied_offers.json`](data/applied_offers.json).
   - GitHub Actions commite automatiquement ce fichier avec `[skip ci]` pour ne jamais postuler deux fois à la même offre.

---

## 📱 Aperçu des Notifications Webhook

### Telegram Bot
```text
🎯 NOUVELLE OPPORTUNITÉ STAGE PFE (Match: 85%)

🏢 Entreprise : Sofrecom Maroc
📌 Poste : Stagiaire en Data (F/H) - Disponible immédiatement
📍 Ville : Casablanca et périphérie
💰 Gratification : ⚪ Non précisé
🛠 Stack : IA, Python, LangChain, RAG, Docker
📤 Statut Candidature : ⚠️ Email absent -> À postuler manuellement sur LinkedIn

👤 Profil LinkedIn Recruteur RH :
👉 https://ma.linkedin.com/in/oumaima-el-malety-a07219176
(Connectez-vous ou envoyez un message direct)

🔗 Lien LinkedIn (Postuler Manuellement) :
👉 https://ma.linkedin.com/jobs/view/stagiaire-en-data-f-h-disponible-immédiatement-at-sofrecom-maroc-4473902342
```

### Discord Webhook
Un embed coloré (vert si rémunéré, bleu sinon) contenant :
- Bouton cliquable direct vers le **profil du recruteur RH**.
- Bouton cliquable direct pour **postuler manuellement sur LinkedIn**.
- Résumé des technologies et statut de l'e-mail envoyé.

---

## ⚙️ Configuration sur GitHub

Pour activer l'agent sur GitHub Actions :

1. Allez sur votre dépôt GitHub : **Settings > Secrets and variables > Actions > New repository secret**.
2. Ajoutez les secrets suivants :

| Secret | Obligatoire | Description |
| :--- | :--- | :--- |
| `GMAIL_USER` | Oui | Votre adresse Gmail (ex: `anas.mouqine@gmail.com`) |
| `GMAIL_APP_PASSWORD` | Oui | Votre mot de passe d'application Google (16 lettres, généré sur [Google Account Security](https://myaccount.google.com/apppasswords)) |
| `DRY_RUN` | Optionnel | Mettre `false` pour envoyer réellement les e-mails (`true` par défaut pour tester en simulation) |
| `TELEGRAM_BOT_TOKEN` | Optionnel | Token de votre bot Telegram (obtenu via `@BotFather`) |
| `TELEGRAM_CHAT_ID` | Optionnel | Votre ID de chat Telegram (obtenu via `@userinfobot`) |
| `DISCORD_WEBHOOK_URL`| Optionnel | URL de webhook Discord d'un canal privé |

---

## 🚀 Exécution Locale (Sur votre Machine)

### 1. Mode Simulation (Dry-Run / Sécurisé)
Exécute tout le scraping, l'analyse et la préparation des e-mails **sans envoyer aucun e-mail** :
```powershell
python run_agent.py
```

### 2. Mode Envoi Réel (Live)
Envoie réellement les candidatures par e-mail aux adresses RH détectées et notifie le webhook :
```powershell
python run_agent.py --live
```

### 3. Exécuter les Tests
```powershell
pytest tests/ -v
```

---

## ⏰ Fréquence d'Exécution sur GitHub Actions

L'agent est configuré dans [`.github/workflows/pfe_hunter_agent.yml`](.github/workflows/pfe_hunter_agent.yml) :
- **Automatique** : Du lundi au vendredi, deux fois par jour (09h00 et 14h00 heure marocaine).
- **Manuel** : Vous pouvez cliquer sur **Actions > PFE Hunter & Auto-Applicant Agent > Run workflow** à n'importe quel moment.
