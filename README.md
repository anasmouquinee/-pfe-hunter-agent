# CV Moderne pour Stage PFE – Intelligence Artificielle & Data Engineering

Ce dossier contient votre CV professionnel au format **LaTeX**, conçu et optimisé spécifiquement pour décrocher un **Stage PFE (Projet de Fin d'Études)** d'excellence en tant qu'élève-ingénieur en 5ème année à l'**EMSI Casablanca**.

---

## 📄 Fichiers Inclus

1. **[`cv_modern_pfe.tex`](cv_modern_pfe.tex)** : Code source LaTeX moderne, modulaire et hautement lisible.
2. **[`cv_modern_pfe.pdf`](cv_modern_pfe.pdf)** : Le CV compilé en PDF haute fidélité (exactement **1 page A4**).
3. **[`cv_preview.png`](cv_preview.png)** : Aperçu haute définition (200 DPI) du rendu final.
4. **[`docs/content_synthesis.md`](docs/content_synthesis.md)** : Synthèse détaillée des données extraites de votre portfolio et de vos certifications.
5. **[`docs/plans/2026-10-05-modern-cv-pfe-ai-data.md`](docs/plans/2026-10-05-modern-cv-pfe-ai-data.md)** : Plan d'implémentation du projet.

---

## 🎯 Points Forts & Optimisations pour le PFE

### 1. Intégration de vos Expériences Industrielles
- **COSUMAR (Compagnie Sucrière Marocaine)** : Mise en valeur du rôle en traitement de données de flux industriels, pipelines ETL sous Python/SQL, automatisation des indicateurs de performance (KPIs) et dashboards opérationnels.
- **SEWS-CABINET (Sumitomo Electric Group)** : Application industrielle *SEWS Connect*, intégration WebRTC/Agora RTC pour la communication d'atelier, scan QR code pour l'attribution des tâches, architecture offline-first avec Hive et Firebase.

### 2. Sélection des 3 Projets Phares (Alignement IA & Data)
- **AI Multi-Agent Orchestrator** : Framework d'agents autonomes (Research, Code, QA), Vector Search RAG, LangChain, FastAPI et benchmarks d'évaluation. *(Démontre une maîtrise des dernières tendances LLMs et Agents).*
- **Enterprise Media Lakehouse & Real-Time Big Data** : Architecture Medallion (Bronze/Silver/Gold), DAGs Apache Airflow, streaming Kafka, conteneurisation Docker Compose. *(Prouve une compétence industrielle en Data Engineering).*
- **Film-A (Recommandation par Graphes)** : Combinaison innovante Neo4j (Graph DB) et Gemini AI pour des recommandations explicables, avec client React Native et backend Node.js.

### 3. Sélection des Certifications les Plus Prestigieuses
Parmi vos 11 certifications vérifiées Coursera, 5 ont été sélectionnées pour maximiser l'impact auprès des recruteurs techniques et managers de projet :
- **Google** : *Agile Project Management* (Scrum, Sprints, Roadmaps)
- **HKUST** : *Software Engineering: Architecture & Management* (UML, Design Patterns, SDLC)
- **University of Michigan** : *Using Python to Access Web Data & APIs* (Web Scraping, REST APIs, JSON/XML)
- **EPFL (Lausanne)** : *Programmation Orientée Objet en C++* (Gestion mémoire, pointeurs, complexité algorithmique)
- **Meta** : *Advanced React & State Architecture* (Hooks, Context, Jest)

*Chaque certification dispose d'un lien cliquable direct avec son identifiant d'accréditation officiel.*

---

## 🛠️ Compilation Locale

Votre machine dispose déjà de **MiKTeX 25.12** avec `pdflatex`. Pour recompiler votre CV à tout moment :

```powershell
pdflatex -interaction=nonstopmode cv_modern_pfe.tex
```

Pour générer un aperçu image avec Python (`PyMuPDF`) :
```powershell
python -c "import fitz; doc=fitz.open('cv_modern_pfe.pdf'); doc[0].get_pixmap(dpi=200).save('cv_preview.png')"
```

---

## ✏️ Personnalisation Rapide

- **Modifier la date du stage COSUMAR :** Modifiez la ligne `\hfill {\scriptsize\color{textmuted}\faCalendar*\ Été 2024}` dans [`cv_modern_pfe.tex`](cv_modern_pfe.tex).
- **Modifier vos coordonnées :** Dans le bloc `EN-TÊTE DU CV`, vous pouvez mettre à jour le téléphone, l'email ou les liens vers votre profil.
