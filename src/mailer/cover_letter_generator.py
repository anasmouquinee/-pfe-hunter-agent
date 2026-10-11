"""Cover letter and email body generator dynamically tailored to the offer's tech stack."""

import html
from src.config import config
from src.models.offer import JobOffer


class CoverLetterGenerator:
    """Generates personalized, high-converting application emails in French."""

    @staticmethod
    def generate_subject(offer: JobOffer) -> str:
        """Standardized professional email subject line."""
        role_label = offer.title if "pfe" in offer.title.lower() else f"Stage PFE -- {offer.title}"
        return f"Candidature {role_label} -- {config.candidate.full_name}"

    @staticmethod
    def _select_highlighted_projects(offer: JobOffer) -> list[tuple[str, str]]:
        """
        Dynamically selects the top 3 most relevant projects based on the offer's domain.
        Always includes the two flagship industrial experiences (COSUMAR, SEWS-CABINET)
        and tailors the leading engineering project (Lakehouse or Multi-Agent).
        """
        text = f"{offer.title} {offer.description}".lower()
        projects: list[tuple[str, str]] = []

        is_data_focused = any(kw in text for kw in ("data", "etl", "airflow", "kafka", "pipeline", "lakehouse", "sql"))

        if is_data_focused:
            projects.append((
                "Enterprise Media Lakehouse",
                "Plateforme distribuée de streaming et pipelines ETL avec Apache Airflow, Kafka, Docker Compose et architecture Medallion."
            ))
        else:
            projects.append((
                "AI Multi-Agent Orchestrator",
                "Framework d'agents autonomes, Vector Search RAG, intégration LangChain et API REST sous FastAPI."
            ))

        # Always highlight both industrial internships
        projects.append((
            "COSUMAR",
            "Stage ingénieur Data : Automatisation des flux de production, pipelines Python/SQL et dashboards de KPIs opérationnels."
        ))
        projects.append((
            "SEWS-CABINET",
            "Sumitomo Electric Group : Application industrielle SEWS Connect, modules temps réel WebRTC et architecture offline-first."
        ))

        return projects

    @classmethod
    def generate_body(cls, offer: JobOffer) -> str:
        """Generates dynamic French plain-text email body tailored to the company and role."""
        company = offer.company if offer.company else "votre entreprise"
        title = offer.title if offer.title else "Stage PFE"
        cand = config.candidate

        skills_text = ""
        if offer.matched_skills:
            top_skills = ", ".join(offer.matched_skills[:4])
            skills_text = f"notamment autour de technologies telles que {top_skills}, "

        projects = cls._select_highlighted_projects(offer)
        projects_str = "\n".join(f"- **{name}** : {desc}" for name, desc in projects)

        body = f"""Bonjour,

Je vous contacte afin de vous soumettre ma candidature pour l'opportunité de **{title}** au sein de **{company}**.

Actuellement élève-ingénieur en 5ème année à l'{cand.school}, spécialisé en **{cand.specialization}**, je suis activement à la recherche d'un **Stage de Projet de Fin d'Études (PFE) de 4 à 6 mois** disponible pour l'année 2026 à Casablanca (ou en mode hybride/remote).

Mon parcours m'a permis de développer une solide expertise pratique {skills_text}consolidée par mes réalisations et projets d'ingénierie :
{projects_str}

Intégrer {company} représente pour moi l'opportunité idéale d'apporter ma rigueur, mes compétences techniques et de m'investir pleinement au sein de vos chantiers technologiques.

Vous trouverez ci-joint mon Curriculum Vitae détaillé pour complément d'information. Je serais ravi d'échanger avec vous lors d'un entretien à votre convenance.

Dans l'attente de votre retour, je vous prie d'agréer mes salutations les plus respectueuses.

Cordialement,

{cand.full_name}
Élève-Ingénieur en 5ème Année -- {cand.specialization} ({cand.school})
Téléphone : {cand.phone} | Email : {cand.email}
LinkedIn : {cand.linkedin_url}
GitHub : {cand.github_url}
Portfolio : {cand.portfolio_url}
"""
        return body

    @classmethod
    def generate_html_body(cls, offer: JobOffer) -> str:
        """Generates a beautifully styled, mobile-responsive HTML email body."""
        company = html.escape(offer.company if offer.company else "votre entreprise")
        title = html.escape(offer.title if offer.title else "Stage PFE")
        cand = config.candidate

        skills_text = ""
        if offer.matched_skills:
            top_skills = ", ".join(offer.matched_skills[:4])
            skills_text = f"notamment autour de technologies clés telles que <strong>{html.escape(top_skills)}</strong>, "

        projects = cls._select_highlighted_projects(offer)
        projects_li = "\n".join(
            f"<li style='margin-bottom: 8px;'><strong style='color: #1e3a8a;'>{html.escape(name)}</strong> : {html.escape(desc)}</li>"
            for name, desc in projects
        )

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1f2937; background-color: #ffffff; padding: 20px;">
  <p>Bonjour,</p>

  <p>Je vous contacte afin de vous soumettre ma candidature pour l'opportunité de <strong>{title}</strong> au sein de <strong>{company}</strong>.</p>

  <p>Actuellement élève-ingénieur en 5ème année à l'<strong>{html.escape(cand.school)}</strong>, spécialisé en <strong>{html.escape(cand.specialization)}</strong>, je suis activement à la recherche d'un <strong>Stage de Projet de Fin d'Études (PFE) de 4 à 6 mois</strong> disponible pour l'année 2026 à Casablanca (ou en mode hybride/remote).</p>

  <p>Mon parcours m'a permis de développer une solide expertise pratique {skills_text}consolidée par des réalisations concrètes :</p>

  <ul style="padding-left: 20px; color: #374151;">
    {projects_li}
  </ul>

  <p>Intégrer <strong>{company}</strong> représente pour moi l'opportunité idéale d'apporter ma rigueur et de participer activement à vos chantiers technologiques.</p>

  <p>Vous trouverez ci-joint mon <strong>Curriculum Vitae détaillé</strong> pour complément d'information. Je serais ravi d'échanger avec vous lors d'un entretien à votre convenance.</p>

  <p>Dans l'attente de votre retour, je vous prie d'agréer mes salutations les plus respectueuses.</p>

  <br>
  <div style="border-top: 2px solid #e5e7eb; padding-top: 14px; margin-top: 20px;">
    <p style="margin: 0; font-size: 16px; font-weight: bold; color: #111827;">{html.escape(cand.full_name)}</p>
    <p style="margin: 2px 0; font-size: 13px; color: #4b5563;">Élève-Ingénieur en 5ème Année -- {html.escape(cand.specialization)}</p>
    <p style="margin: 2px 0; font-size: 13px; color: #6b7280;">{html.escape(cand.school)}</p>
    <p style="margin: 6px 0 0 0; font-size: 13px;">
      📞 {html.escape(cand.phone)} &nbsp;|&nbsp; ✉️ <a href="mailto:{html.escape(cand.email)}" style="color: #2563eb;">{html.escape(cand.email)}</a>
    </p>
    <p style="margin: 4px 0 0 0; font-size: 13px;">
      🔗 <a href="{html.escape(cand.linkedin_url)}" style="color: #2563eb;">LinkedIn</a> &nbsp;|&nbsp;
      💻 <a href="{html.escape(cand.github_url)}" style="color: #2563eb;">GitHub</a> &nbsp;|&nbsp;
      🌐 <a href="{html.escape(cand.portfolio_url)}" style="color: #2563eb;">Portfolio</a>
    </p>
  </div>
</body>
</html>"""
