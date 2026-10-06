"""Cover letter and email body generator tailored for Anas Mouqine."""

from src.config import config
from src.models.offer import JobOffer


class CoverLetterGenerator:
    """Generates personalized, high-converting application emails in French."""

    @staticmethod
    def generate_subject(offer: JobOffer) -> str:
        """Standardized professional email subject line."""
        return f"Candidature Stage PFE (4-6 mois) -- Ingénieur IA & Data Engineering -- {config.candidate.full_name}"

    @staticmethod
    def generate_body(offer: JobOffer) -> str:
        """Generates dynamic French email body tailored to the company and role."""
        company = offer.company if offer.company else "votre entreprise"
        title = offer.title if offer.title else "Stage PFE"
        
        # Format matched skills nicely
        skills_text = ""
        if offer.matched_skills:
            top_skills = ", ".join(offer.matched_skills[:4])
            skills_text = f"notamment autour de technologies clés telles que {top_skills}, "

        body = f"""Bonjour,

Je vous contacte afin de vous soumettre ma candidature pour l'opportunité de **{title}** au sein de **{company}**.

Actuellement élève-ingénieur en 5\u00e8me ann\u00e9e \u00e0 l'\u00c9cole Marocaine des Sciences de l'Ing\u00e9nieur (EMSI Casablanca), sp\u00e9cialis\u00e9 en **Intelligence Artificielle & Data Engineering**, je suis activement \u00e0 la recherche d'un **Stage de Projet de Fin d'\u00c9tudes (PFE) de 4 \u00e0 6 mois** disponible pour l'ann\u00e9e 2026 \u00e0 Casablanca (ou en mode hybride/remote).

Mon parcours m'a permis de d\u00e9velopper une solide expertise pratique {skills_text}consolid\u00e9e par deux exp\u00e9riences industrielles d'\u00e9lite :
- **COSUMAR** (Stage Ing\u00e9nieur Data) : Conception et automatisation de pipelines ETL sous Python et SQL pour le suivi des KPIs de production en temps r\u00e9el.
- **SEWS-CABINET** (Sumitomo Electric Group) : D\u00e9veloppement de la plateforme collaborative industrielle SEWS Connect sous Flutter, modules d'appels temps r\u00e9el WebRTC et architecture offline-first.

J'ai \u00e9galement con\u00e7u et d\u00e9ploy\u00e9 des projets d'ing\u00e9nierie avanc\u00e9s :
- **AI Multi-Agent Orchestrator** : Framework d'agents autonomes et RAG vectoriel sous LangChain et FastAPI.
- **Enterprise Media Lakehouse** : Plateforme de streaming et traitement Big Data distribu\u00e9e avec Apache Airflow, Kafka et Docker Compose.
- **Film-A** : Moteur de recommandation IA hybride couplant base graphe Neo4j et Gemini AI.

Int\u00e9grer {company} repr\u00e9sente pour moi l'opportunit\u00e9 id\u00e9ale d'apporter ma rigueur, mes comp\u00e9tences en ing\u00e9nierie des donn\u00e9es et de participer activement \u00e0 vos chantiers technologiques.

Vous trouverez ci-joint mon Curriculum Vitae d\u00e9taill\u00e9 pour compl\u00e9ment d'information. Je serais ravi d'\u00e9changer avec vous lors d'un entretien \u00e0 votre convenance.

Dans l'attente de votre retour, je vous prie d'agr\u00e9er mes salutations les plus respectueuses.

Cordialement,

**{config.candidate.full_name}**
\u00c9l\u00e8ve-Ing\u00e9nieur en 5\u00e8me Ann\u00e9e -- IA & Data Engineering (EMSI Casablanca)
T\u00e9l\u00e9phone : {config.candidate.phone} | Email : {config.candidate.email}
LinkedIn : {config.candidate.linkedin_url}
GitHub : {config.candidate.github_url}
Portfolio : {config.candidate.portfolio_url}
"""
        return body
