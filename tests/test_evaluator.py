"""Unit tests for OfferEvaluator with strict AI relevance verification."""

from src.models.offer import JobOffer
from src.matcher.evaluator import OfferEvaluator


def test_evaluator_pfe_and_remunerated():
    evaluator = OfferEvaluator()
    offer = JobOffer(
        title="Stage PFE -- Data Engineer & IA",
        company="Smart Analytics Casablanca",
        location="Casablanca, Maroc",
        url="https://example.com/pfe-data",
        description="Recherche stagiaire PFE pour projet IA et Big Data (Python, Apache Airflow, Kafka). Stage rémunéré avec gratification.",
        source="rekrute"
    )

    evaluated = evaluator.evaluate(offer)
    assert evaluator.is_ai_offer(evaluated) is True
    assert evaluator.is_pfe_offer(evaluated) is True
    assert evaluated.is_remunerated is True
    assert "Python" in evaluated.matched_skills
    assert "Apache Airflow" in evaluated.matched_skills
    assert evaluated.score >= 80


def test_evaluator_disqualify_cdi_senior():
    evaluator = OfferEvaluator()
    offer = JobOffer(
        title="Ingénieur Senior CDI (5 ans d'expérience)",
        company="OldCorp",
        location="Casablanca",
        url="https://example.com/senior-cdi",
        description="Poste CDI pour ingénieur confirmé avec au moins 5 ans d'expérience.",
        source="emploima"
    )

    assert evaluator.is_pfe_offer(offer) is False
    evaluated = evaluator.evaluate(offer)
    assert evaluated.score < 50


def test_evaluator_rejects_non_ai_offers():
    evaluator = OfferEvaluator()

    # Case 1: SAP Hybris
    offer_sap = JobOffer(
        title="Stagiaire PFE en SAP HYBRIS",
        company="Inetum",
        location="Casablanca",
        url="https://example.com/pfe-sap",
        description="Stage PFE pour intégration ERP et modules SAP Hybris e-commerce.",
        source="linkedin_guest"
    )
    assert evaluator.is_ai_offer(offer_sap) is False
    assert evaluator.is_pfe_offer(offer_sap) is False
    assert evaluator.evaluate(offer_sap).score < 50

    # Case 2: IT Support / Helpdesk
    offer_support = JobOffer(
        title="Stagiaire Support Technique & Helpdesk IT",
        company="TelecomCorp",
        location="Casablanca",
        url="https://example.com/stage-support",
        description="Support utilisateurs niveau 1, gestion de parc informatique et ticketing.",
        source="emploima"
    )
    assert evaluator.is_ai_offer(offer_support) is False
    assert evaluator.is_pfe_offer(offer_support) is False

    # Case 3: ServiceNow
    offer_servicenow = JobOffer(
        title="Stagiaire PFE – Reporting IT ServiceNow & Support",
        company="Inetum",
        location="Casablanca",
        url="https://example.com/pfe-servicenow",
        description="Conception de dashboards ServiceNow pour le suivi d'incidents IT.",
        source="linkedin_guest"
    )
    assert evaluator.is_ai_offer(offer_servicenow) is False


def test_evaluator_accepts_core_ai_topics():
    evaluator = OfferEvaluator()

    # Case 1: Generative AI & LLM / RAG
    offer_genai = JobOffer(
        title="Stage PFE: Agentic AI & LLMs",
        company="AI Innovation Lab Casablanca",
        location="Casablanca",
        url="https://example.com/pfe-llm",
        description="Développement d'agents intelligents basés sur LangChain, RAG et modèles d'IA générative.",
        source="linkedin_guest"
    )
    assert evaluator.is_ai_offer(offer_genai) is True
    assert evaluator.is_pfe_offer(offer_genai) is True
    assert evaluator.evaluate(offer_genai).score >= 70

    # Case 2: Computer Vision / Deep Learning
    offer_cv = JobOffer(
        title="Stage PFE - Computer Vision & Deep Learning",
        company="VisionTech Maroc",
        location="Casablanca",
        url="https://example.com/pfe-cv",
        description="Entraînement de modèles de détection d'objets avec PyTorch et OpenCV.",
        source="rekrute"
    )
    assert evaluator.is_ai_offer(offer_cv) is True
    assert evaluator.is_pfe_offer(offer_cv) is True
